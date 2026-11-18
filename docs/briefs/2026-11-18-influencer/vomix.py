import subprocess, re, json, sys
ROOT='C:/Users/krish/dev/growth-heartside/local'
F={
 'obsessed':dict(film='ip-obsessed',limit=31.3,starts=[0.299,3.371,6.016,9.685,11.179,14.471,17.372,20.999,23.346,25.18],end=28.026,
   targets=[0.0,3.0,6.5,10.5,12.3,16.3,18.8,22.8,25.8,27.8]),
 'day':dict(film='ip-day',limit=29.1,starts=[0.299,2.859,5.333,8.533,11.52,15.387,17.222,19.313,22.726,24.22,25.457,28.102],end=29.912,
   targets=[0.0,3.0,5.0,8.0,10.6,13.1,15.6,17.8,20.3,22.1,24.6,26.6]),
 'couple':dict(film='ip-couple',limit=28.6,starts=[0.256,3.797,6.741,10.197,12.8,14.421,17.174,20.843,23.702],end=26.935,
   targets=[0.0,3.2,5.7,9.2,11.8,13.7,17.7,21.1,24.1]),
}
def silences(wav):
    out=subprocess.run(['ffmpeg','-hide_banner','-i',wav,'-af','silencedetect=n=-40dB:d=0.12','-f','null','-'],capture_output=True,text=True).stderr
    s=[float(x) for x in re.findall(r'silence_start: ([\d.]+)',out)]
    return s
GAP=0.12
for k,c in F.items():
    wav=f'{ROOT}/footage/voice/vo-{k}.wav'
    sil=silences(wav)
    segs=[]
    st=c['starts']+[c['end']]
    for i in range(len(c['starts'])):
        a=max(0,st[i]-0.04); b=st[i+1]
        cands=[x for x in sil if a+0.5<x<b]
        e=(max(cands)+0.06) if cands else b
        segs.append((a,min(e,b)))
    best=None
    for t100 in range(100,131):
        t=t100/100; pos=0; plan=[]
        for (a,b),tg in zip(segs,c['targets']):
            d=(b-a)/t; s=max(tg,pos+GAP if plan else tg); plan.append((s,d)); pos=s+d
        if pos<=c['limit']: best=(t,plan); break
    if not best: print(k,'DOES NOT FIT even at 1.30, end',round(pos,2)); best=(t,plan)
    t,plan=best
    print(k,'tempo',t,'end',round(plan[-1][0]+plan[-1][1],2),'starts',[round(s,2) for s,_ in plan],'drift',[round(s-tg,2) for (s,_),tg in zip(plan,c['targets'])])
    fc=[];labels=[]
    for i,((a,b),(s,d)) in enumerate(zip(segs,plan)):
        fc.append(f'[0:a]atrim={a:.3f}:{b:.3f},asetpts=PTS-STARTPTS,atempo={t},afade=t=in:d=0.02,afade=t=out:st={max(0,d-0.04):.3f}:d=0.04,adelay={int(s*1000)}|{int(s*1000)}[s{i}]')
        labels.append(f'[s{i}]')
    fc.append(''.join(labels)+f'amix=inputs={len(labels)}:normalize=0,highpass=f=80,acompressor=threshold=-18dB:ratio=3:attack=5:release=80,loudnorm=I=-16:TP=-1.5:LRA=7,apad[vo]')
    film=c['film']; out=f'{ROOT}/media/studio/{film}/{film}_vo.mp4'
    cmd=['ffmpeg','-v','error','-y','-i',wav,'-i',f'{ROOT}/media/studio/{film}/{film}.mp4','-filter_complex',';'.join(fc),'-map','1:v','-map','[vo]','-c:v','copy','-c:a','aac','-b:a','192k','-ar','48000','-t',str({'ip-obsessed':33.8,'ip-day':34.6,'ip-couple':31.6}[film]),'-af','apad' if False else 'anull',out]
    cmd=[x for x in cmd if x not in ('-af','anull')]
    r=subprocess.run(cmd,capture_output=True,text=True); print(film,'mix',r.returncode,r.stderr[-400:])
