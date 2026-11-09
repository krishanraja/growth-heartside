"""Build and serve an exact-file local review; no external media dependencies.

Only manifest-selected media and generated posters are served on loopback.
This never writes social posts, changes releases, or makes media public.
"""
import argparse
import hashlib
import html
import json
import mimetypes
import re
import subprocess
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import unquote, urlsplit

TITLES = {'F01':'Becoming the mug','F03':'The Christmas heist','F04':'Me vs my golden',
          'F05':'Court of the couch','F07':'The art critic','F12':'Head of security',
          'F06-lab':'What your lab really thinks','F06-dachshund':'What your dachshund really thinks',
          'F19':'The family reunion','F20':'Family drama','F21':'No debates at dinner',
          'F22':'Nobody feeds me','F23':'The turkey timer','F24':'His chair now'}

def build(folder, port=8767):
    folder=Path(folder).resolve()
    files=json.loads((folder/'library-release/manifest.json').read_text(encoding='utf-8'))
    packet=json.loads((folder/'replacement-packet.json').read_text(encoding='utf-8'))
    release_path=Path(__file__).resolve().parents[1]/'library/editions/2026-11-06-ui.json'
    badge='Drafts held'
    if release_path.exists():
        release=json.loads(release_path.read_text(encoding='utf-8'))
        approved_hash=release.get('approval',{}).get('packet_sha256')
        actual_hash=hashlib.sha256((folder/'replacement-packet.json').read_bytes()).hexdigest()
        if approved_hash==actual_hash and release.get('schedule_verification',{}).get('result')=='pass':
            badge='Creative approved · Organic scheduled'
    output=folder/'board';output.mkdir(exist_ok=True)
    routes={}
    for row in files:
        source=Path(row['path']).resolve()
        if hashlib.sha256(source.read_bytes()).hexdigest()!=row['sha256']:
            raise ValueError('release checksum mismatch: '+row['file'])
        routes['/media/'+row['file']]=source
        if row['role']=='video':
            poster=output/(row['post']+'-poster.jpg')
            subprocess.run(['ffmpeg','-v','error','-y','-ss','1','-i',str(source),'-frames:v','1','-vf','scale=540:-1',str(poster)],check=True)
            routes['/posters/'+poster.name]=poster
    sections=[];nav=[]
    for concept in dict.fromkeys(x['post'] for x in files):
        name=html.escape(TITLES.get(concept,concept));nav.append(f'<a href="#{concept}">{name}</a>')
        cards=[]
        for row in (x for x in files if x['post']==concept and x['role']!='cover'):
            url='/media/'+row['file']
            if row['role']=='video':
                media=f'<video id="video-{concept}" aria-label="{name}" controls playsinline preload="metadata" poster="/posters/{concept}-poster.jpg" src="{url}"></video>'
                label='Reel · original audio'
                play=f'<button class="play" data-video="video-{concept}">Play {name}</button>'
            else:
                media=f'<img src="{url}" alt="{html.escape(row.get("alt",name))}">'
                label='TikTok photo' if row.get('platform')=='tiktok' else ('Instagram / Facebook' if row.get('platform')=='feed' else f'Slide {row["index"]+1}')
                play=''
            cards.append(f'<figure>{media}<figcaption><strong>{label}</strong>{play}<a href="{url}" target="_blank">Open full size</a><span class="error" hidden>Could not load. Use the full-size link.</span></figcaption></figure>')
        copy=[]
        for post in packet['posts']:
            ids=post['concept'] if isinstance(post['concept'],list) else [post['concept']]
            if concept in ids:
                copy.append(f'<details><summary>{post["platform"].capitalize()} caption</summary><p class="copy">{html.escape(post["text"])}</p></details>')
        layout_class = 'single' if len(cards) == 1 else 'gallery'
        sections.append(f'<section class="{layout_class}" id="{concept}"><header><span class="code">{concept}</span><h2>{name}</h2></header><div class="media">'+''.join(cards)+'</div><div class="captions">'+''.join(copy)+'</div></section>')
    css='''*{box-sizing:border-box}html{scroll-behavior:smooth}body{font:16px/1.5 system-ui;background:#f6f1e7;color:#24201b;margin:0}main{max-width:1200px;margin:auto;padding:32px 24px}h1{font-size:clamp(30px,5vw,48px);line-height:1.12;letter-spacing:-1px;margin:12px 0}h2{font-size:26px;line-height:1.2;margin:4px 0 20px}.intro{max-width:740px;color:#625b50}.badge,.code{font-size:12px;font-weight:700;letter-spacing:1px;text-transform:uppercase}.badge{color:#7c382d}nav{display:flex;flex-wrap:wrap;gap:8px;margin:24px 0 36px}nav a{padding:8px 12px;background:#fffaf1;border:1px solid #cfc6b7;border-radius:20px;font-size:13px;text-decoration:none;color:inherit}section{border-top:1px solid #cfc6b7;padding:28px 0;scroll-margin-top:15px}.media{display:grid;grid-template-columns:repeat(auto-fit,minmax(min(100%,280px),1fr));gap:20px;align-items:start}figure{margin:0;min-width:0;max-width:360px}video,img{display:block;width:100%;height:auto;max-height:580px;object-fit:contain;background:#24201b;border-radius:8px}video{aspect-ratio:9/16}figcaption{display:grid;gap:8px;padding:12px 0;font-size:14px}a{color:#843c2f}button{font:inherit;cursor:pointer;background:#24201b;color:#fffaf1;border:0;border-radius:6px;padding:10px 14px;text-align:left}button:focus-visible,a:focus-visible,summary:focus-visible{outline:3px solid #bb6b28;outline-offset:3px}.single{display:grid;grid-template-columns:minmax(280px,360px) 1fr;gap:0 32px}.single>header{grid-column:1/-1}.single .captions{margin-top:0}.captions{max-width:760px;margin-top:18px}details{padding:12px 0;border-top:1px solid #ddd4c6}summary{cursor:pointer;font-weight:600}.copy{white-space:pre-wrap;overflow-wrap:anywhere}.error{color:#ae2424}@media(max-width:600px){.single{display:block}main{padding:24px 16px}.media{grid-template-columns:1fr}figure{max-width:none}video,img{max-height:70vh}h2{font-size:24px}}'''
    script='''document.querySelectorAll('.play').forEach(b=>b.onclick=()=>{const v=document.getElementById(b.dataset.video);if(v.paused){document.querySelectorAll('video').forEach(o=>{if(o!==v)o.pause()});v.play().catch(()=>{v.closest('figure').querySelector('.error').hidden=false})}else v.pause()});document.querySelectorAll('video').forEach(v=>{v.onplay=()=>v.closest('figure').querySelector('button').textContent='Pause video';v.onpause=()=>v.closest('figure').querySelector('button').textContent='Play video';});document.querySelectorAll('img,video').forEach(m=>m.addEventListener('error',()=>m.closest('figure').querySelector('.error').hidden=false));'''
    page='<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Heartside · Creative review</title><style>'+css+'</style></head><body><main><div class="badge">Heartside · 6 November · Drafts held</div><h1>See every post. Hear every reel.</h1><p class="intro">Eight reels, two five-slide carousels and six photo concepts, with their platform captions. Tap Play for sound. The media below is the exact corrected delivery batch.</p><nav aria-label="Jump to concept">'+''.join(nav)+'</nav>'+''.join(sections)+'</main><script>'+script+'</script></body></html>'
    page=page.replace('Heartside · 6 November · Drafts held','Heartside · 6 November · '+html.escape(badge))
    target=output/'index.html';target.write_text(page,encoding='utf-8');routes['/']=target
    # File previews cannot reliably load remote or sibling media. Give an explicit
    # working entry point instead of another grid of silently broken assets.
    (folder/'review.html').write_text(f'<!doctype html><meta charset="utf-8"><title>Heartside review</title><h1>Heartside creative review</h1><p><a href="http://127.0.0.1:{port}/">Open the working review board</a></p><p>Opens on this computer, with all media served locally.</p>',encoding='utf-8')
    return routes

def serve(routes,port):
    class Handler(BaseHTTPRequestHandler):
        def do_HEAD(self):self.respond(False)
        def do_GET(self):self.respond(True)
        def respond(self,body):
            source=routes.get(unquote(urlsplit(self.path).path))
            if not source:return self.send_error(404)
            size=source.stat().st_size;start,end=0,size-1;status=200
            range_header=self.headers.get('Range')
            if range_header:
                match=re.fullmatch(r'bytes=(\d+)-(\d*)',range_header)
                if not match:return self.send_error(416)
                start=int(match[1]);end=min(int(match[2]) if match[2] else end,end)
                if start>end:return self.send_error(416)
                status=206
            self.send_response(status)
            self.send_header('Content-Type',mimetypes.guess_type(source.name)[0] or 'application/octet-stream')
            self.send_header('Content-Length',str(end-start+1));self.send_header('Accept-Ranges','bytes')
            self.send_header('Cache-Control','no-cache')
            if status==206:self.send_header('Content-Range',f'bytes {start}-{end}/{size}')
            self.end_headers()
            if body:
                try:
                    with source.open('rb') as f:
                        f.seek(start);remaining=end-start+1
                        while remaining:
                            data=f.read(min(262144,remaining));self.wfile.write(data);remaining-=len(data)
                except (BrokenPipeError,ConnectionResetError,ConnectionAbortedError):pass
        def log_message(self,*args):pass
    print(f'Review board: http://127.0.0.1:{port}/; {len(routes)} selected routes',flush=True)
    ThreadingHTTPServer(('127.0.0.1',port),Handler).serve_forever()

if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('folder');parser.add_argument('--port',type=int,default=8767);parser.add_argument('--serve',action='store_true')
    args=parser.parse_args();routes=build(args.folder,args.port)
    if args.serve:serve(routes,args.port)
