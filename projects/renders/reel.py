"""Centro Equino reel (5 Oct 2026, Will: 'make a reel'): starred finalist paintings animated with Veo 3.1 (animate.py),
a day at the centre from dawn to the lantern-lit night, crossfaded with their own ambient sound, title cards front and back.

    python reel.py            (clips already in anim/ are kept; delete one to remake it)
"""
import os, subprocess, sys, concurrent.futures as cf
from PIL import Image, ImageDraw, ImageFont
HERE = os.path.dirname(os.path.abspath(__file__)); IMG = os.path.join(HERE, '..', '..', '..', 'will-os', 'equino', 'img')
A = os.path.join(HERE, os.environ.get('REEL_DIR', 'anim-full'))   # 5 Oct: first cut (fast model) kept in anim/
os.makedirs(A, exist_ok=True)
import animate as AN
MODEL = os.environ.get('REEL_MODEL', 'veo-3.1-generate-preview')   # 5 Oct (Will: some animation weird, use a better model): the full Veo 3.1

# 5 Oct: calmer motion than the first cut; small natural movements, a slow steady camera
SCENES = [   # (clip, painting, motion)
 ('01-dawn', 'p4-site-ne-fan-dawn-google', 'Just after sunrise over a ranch in the dry hills of Baja California. A very slow, steady, high drone glide forward over the whole site; low sun raking across the land, a little haze in the valley; the horses graze quietly in place, the morning light slowly warms.'),
 ('02-fog', '4-hill-s-fan-fog-openai', 'Early morning marine fog slowly lifting off the valley below the hill; the camera drifts very slowly sideways along the hillside; the mist thins and drifts; the horses stand and graze, the soft light slowly brightens.'),
 ('03-stalls', '1-hero-sw-oct4o', 'Golden afternoon. The camera slowly and steadily orbits a little to the left over the covered stalls; the horses in the runs stand, swish their tails and lower their heads; long shadows, warm light, the clouds drift slowly.'),
 ('04-aisle', '10-stable-aisle-fresh', 'Inside the stable aisle, a calm still moment. The camera is almost still, only a very slight slow push forward. Nobody walks: any person in the picture stays exactly where they are, far away and small, standing still. The horses look out over their stall doors and slowly turn their heads; dust motes float in the shafts of warm sunlight; the light shifts very slightly.'),
 ('05-farrier', 'wash-farrier-fan-left-google', 'At the wash pad under the grapevine trellis. The camera pushes in very slowly; the farrier stays bent at the hoof, working with small movements; the horse stands still and flicks its ears and tail; grape leaves stir in a light breeze, warm late light.'),
 ('06-picnic', '23-picnic-side-oct4o', 'Families picnicking on the stone-stepped platforms beside the small caf\u00e9. The camera drifts very slowly sideways; the seated people stay seated and talk with small gestures; the rider in the far arena only walks very slowly at a calm walk, no trotting, no dust kicked up; a light breeze, golden hour.'),
 ('07-cafe', 'cafe-end-fan-high-google', 'The caf\u00e9 end with its stone bar wall and trough. A very slow, steady drone drift forward; the horse by the trough lowers its head to drink, the reeds sway gently, the people stay where they are, warm evening light.'),
 ('08-blue', '1-hero-sw-fan-blue-google', 'Blue hour just after sunset. A very slow, steady drone glide toward the stable; warm lights glow steadily inside, the sky slowly deepens from orange to blue, the horses stand calmly in the runs.'),
 ('09-lantern', '16-stable-sw-lantern-fan-right-google', 'Moody deep twilight. The camera drifts very slowly forward toward the glowing stable. Warm amber light glows steadily from inside between the thin wall sticks. The horses stand calmly and only shift their weight or swish their tails; the sky slowly darkens.'),
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
    AN.animate(os.path.join(IMG, src + '.jpg'), out, motion, MODEL); return out

if __name__ == '__main__':
    with cf.ThreadPoolExecutor(int(os.environ.get('REEL_JOBS', '1'))) as ex: clips = list(ex.map(make, SCENES))   # 5 Oct: one at a time for the full model's rate limit
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
