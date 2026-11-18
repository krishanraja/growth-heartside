"""Timestamped contact sheet: sheet.py <in.mp4> <out.jpg> [step=0.5]"""
import subprocess, sys, io
from PIL import Image, ImageDraw, ImageFont
src, out = sys.argv[1], sys.argv[2]
step = float(sys.argv[3]) if len(sys.argv) > 3 else 0.5
dur = float(subprocess.check_output(['ffprobe','-v','error','-show_entries','format=duration','-of','csv=p=0',src]).decode())
times = [round(i*step,2) for i in range(int(dur/step)+1) if i*step < dur-0.05]
W = 270
tiles = []
for t in times:
    png = subprocess.check_output(['ffmpeg','-v','error','-ss',str(t),'-i',src,'-frames:v','1','-vf',f'scale={W}:-2','-f','image2pipe','-vcodec','png','-'])
    im = Image.open(io.BytesIO(png)).convert('RGB')
    d = ImageDraw.Draw(im)
    try: f = ImageFont.truetype('arial.ttf', 22)
    except Exception: f = ImageFont.load_default()
    d.rectangle([0,0,70,30], fill=(0,0,0)); d.text((6,3), f'{t:.1f}s', fill=(255,255,0), font=f)
    tiles.append(im)
cols = 5; H = tiles[0].height; rows = (len(tiles)+cols-1)//cols
sheet = Image.new('RGB', (W*cols, H*rows), 'white')
for i, im in enumerate(tiles): sheet.paste(im, ((i%cols)*W, (i//cols)*H))
sheet.save(out, quality=82)
print(out, len(tiles))
