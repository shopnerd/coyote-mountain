"""Centro Equino reel (5 Oct 2026, Will: 'make a reel'): starred finalist paintings animated with Veo 3.1 (animate.py),
a day at the centre from dawn to the lantern-lit night, crossfaded with their own ambient sound, title cards front and back.

    python reel.py            (clips already in anim/ are kept; delete one to remake it)
"""
import os, subprocess, sys, concurrent.futures as cf
from PIL import Image, ImageDraw, ImageFont
HERE = os.path.dirname(os.path.abspath(__file__)); IMG = os.path.join(HERE, '..', '..', '..', 'will-os', 'equino', 'img'); A = os.path.join(HERE, 'anim')
os.makedirs(A, exist_ok=True)
import animate as AN

SCENES = [   # (clip, painting, motion)
 ('01-dawn', 'p4-site-ne-fan-dawn-google', 'Just after sunrise over a ranch in the dry hills of Baja California. A very slow, high drone glide forward over the whole site, low sun raking across the land, a little haze in the valley; horses graze, a rider moves along the road, morning light warms.'),
 ('02-fog', '4-hill-s-fan-fog-openai', 'Early morning marine fog slowly lifting off the valley below the hill; the camera drifts slowly sideways along the hillside; the mist thins and drifts, horses move quietly in the paddocks, soft light brightens.'),
 ('03-stalls', '1-hero-sw-oct4o', 'Golden afternoon. The camera slowly orbits a little to the left over the covered stalls; horses walk and swish their tails in the runs, a person leads a horse along the path, long shadows, warm light, a few clouds drift.'),
 ('04-aisle', '10-stable-aisle-fresh', 'Inside the stable aisle. The camera walks slowly forward down the aisle at eye level; horses look out over their stall doors and turn their heads, dust motes float in shafts of warm sunlight, a person walks at the far end.'),
 ('05-farrier', 'wash-farrier-fan-left-google', 'At the wash pad under the grapevine trellis. The camera slowly pushes in; the farrier works on the horse\u2019s hoof, the horse shifts its weight and flicks its ears and tail, grape leaves stir in a light breeze, warm late light.'),
 ('06-picnic', '23-picnic-side-oct4o', 'Families picnicking on the stone-stepped platforms beside the small caf\u00e9. The camera drifts slowly sideways; people talk, eat and laugh, children move about, a rider passes in the arena, a light breeze, golden hour.'),
 ('07-cafe', 'cafe-end-fan-high-google', 'The caf\u00e9 end with its stone bar wall and trough. A slow high drone drift forward; a horse walks up and drinks at the trough, reeds sway, people at the bar wall, warm evening light.'),
 ('08-blue', '1-hero-sw-fan-blue-google', 'Blue hour just after sunset. A slow drone glide over the covered stalls toward the stable; warm lights glow inside, the sky deepens from orange to blue, horses settle in the runs.'),
 ('09-lantern', '16-stable-sw-lantern-fan-right-google', None),   # the test clip, stable-lantern.mp4
]
FADE, FPS, W, H = 1.0, 24, 1920, 1080

def title(path, big, small):
    im = Image.new('RGB', (W, H), (22, 19, 15)); d = ImageDraw.Draw(im)
    f1 = ImageFont.truetype('C:/Windows/Fonts/georgia.ttf', 96); f2 = ImageFont.truetype('C:/Windows/Fonts/georgiai.ttf', 44)
    for txt, f, y, c in ((big, f1, H / 2 - 70, (241, 231, 214)), (small, f2, H / 2 + 50, (227, 167, 90))):
        w = d.textlength(txt, font=f); d.text(((W - w) / 2, y), txt, font=f, fill=c)
    png = path[:-4] + '.png'; im.save(png)
    subprocess.run(['ffmpeg', '-loglevel', 'error', '-y', '-loop', '1', '-t', '3', '-i', png, '-f', 'lavfi', '-t', '3', '-i', 'anullsrc=r=48000:cl=stereo',
                    '-vf', f'fps={FPS},format=yuv420p', '-c:v', 'libx264', '-c:a', 'aac', '-shortest', path], check=True)

def make(sc):
    clip, src, motion = sc; out = os.path.join(A, clip + '.mp4')
    if os.path.exists(out): return out
    if motion is None: os.replace(os.path.join(A, 'stable-lantern.mp4'), out); return out
    AN.animate(os.path.join(IMG, src + '.jpg'), out, motion); return out

if __name__ == '__main__':
    with cf.ThreadPoolExecutor(3) as ex: clips = list(ex.map(make, SCENES))
    t0, t1 = os.path.join(A, '00-title.mp4'), os.path.join(A, '99-end.mp4')
    title(t0, 'Centro Equino', 'Chichihuas \u00b7 Baja California'); title(t1, 'Centro Equino', 'dise\u00f1o preliminar \u00b7 preliminary design \u00b7 2026')
    parts = [t0] + clips + [t1]
    # normalise every part to 1920x1080 / 24 fps / 48 kHz stereo, then chain xfade + acrossfade
    norm = []
    for p in parts:
        q = p[:-4] + '.n.mp4'; norm.append(q)
        subprocess.run(['ffmpeg', '-loglevel', 'error', '-y', '-i', p, '-vf', f'scale={W}:{H}:force_original_aspect_ratio=increase,crop={W}:{H},fps={FPS},format=yuv420p',
                        '-af', 'aresample=48000,aformat=channel_layouts=stereo', '-c:v', 'libx264', '-crf', '18', '-c:a', 'aac', q], check=True)
    dur = [float(subprocess.run(['ffprobe', '-v', 'error', '-show_entries', 'format=duration', '-of', 'csv=p=0', q], capture_output=True, text=True).stdout) for q in norm]
    fc, v, a, off = [], '0:v', '0:a', dur[0]
    for i in range(1, len(norm)):
        off -= FADE
        fc.append(f'[{v}][{i}:v]xfade=transition=fade:duration={FADE}:offset={off:.3f}[v{i}]'); fc.append(f'[{a}][{i}:a]acrossfade=d={FADE}[a{i}]')
        v, a = f'v{i}', f'a{i}'; off += dur[i]
    cmd = ['ffmpeg', '-loglevel', 'error', '-y'] + sum([['-i', q] for q in norm], []) + ['-filter_complex', ';'.join(fc), '-map', f'[{v}]', '-map', f'[{a}]',
           '-c:v', 'libx264', '-crf', '20', '-preset', 'slow', '-movflags', '+faststart', '-c:a', 'aac', '-b:a', '160k', os.path.join(A, 'centro-equino-reel.mp4')]
    subprocess.run(cmd, check=True); print('reel:', os.path.join(A, 'centro-equino-reel.mp4'), f'{off:.1f}s')
