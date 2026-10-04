"""Hand a view to Will's own ChatGPT and Gemini apps (4 Oct 2026). Claude drives his logged-in Chrome (Claude in Chrome):

    python apprender.py prep <view>          -> scratch/apps/<view>.jpg + <view>.txt  (model shot + the exact brief, one paste)
    ... Claude in Chrome: chatgpt.com: attach the jpg, paste the txt, send; gemini.google.com: Upload & tools > Create image,
        attach, aspect 16:9, paste, send. Save: ChatGPT = fetch the 'Generated image 1' blob and download it as <view>-chatgpt.png;
        Gemini = its download button (Gemini_Generated_Image_*.jpg) or Will downloads it.
    python apprender.py import <view> [chatgpt file] [gemini file]   -> gallery (tags gptapp / gemapp), Drive renderings/apps/

Files default to the newest matching ones in Downloads. The gallery lists them in the 3 Oct section when the view is there.
"""
import os, sys, glob, shutil
from PIL import Image
HERE = os.path.dirname(os.path.abspath(__file__)); sys.argv_saved = list(sys.argv); sys.argv = [sys.argv[0], 'google']
import gallery3 as G
sys.argv = sys.argv_saved
WEB = os.path.join(HERE, '..', '..', '..', 'will-os', 'equino', 'img')
DRIVE = os.path.join(os.environ.get('EQUINO_PACK_DIR', 'G:/My Drive/MEXICO/Chichihaus/2026-09-23 Centro Equino pack'), 'renderings', 'apps')
APPS = os.path.join(HERE, 'apps'); DL = os.path.join(os.path.expanduser('~'), 'Downloads')
cmd, view = sys.argv[1], sys.argv[2]
if cmd == 'prep':
    os.makedirs(APPS, exist_ok=True)
    src = next((p for p in (os.path.join(HERE, 'model', f'model-{view}.png'), os.path.join(HERE, 'fans', 'model', f'model-{view}.png')) if os.path.exists(p)), None)
    if not src: sys.exit('no model shot for ' + view)
    Image.open(src).convert('RGB').save(os.path.join(APPS, f'{view}.jpg'), quality=92)
    brief = (G.BLOCK3 if view.startswith('b') else G.BRIEF) + G.EXTRA.get(view, G.EXTRA.get(view.split('-fan-')[0], ''))
    open(os.path.join(APPS, f'{view}.txt'), 'w', encoding='utf-8').write('Turn the attached 3D model render into a photograph, same camera, framing and aspect. ' + brief)
    print(os.path.join(APPS, f'{view}.jpg')); print(os.path.join(APPS, f'{view}.txt'))
elif cmd == 'import':
    newest = lambda pats: max((f for p in pats for f in glob.glob(os.path.join(DL, p))), key=os.path.getmtime, default=None)
    gpt = sys.argv[3] if len(sys.argv) > 3 else newest([f'{view}-chatgpt*.png', 'ChatGPT Image*.png'])
    gem = sys.argv[4] if len(sys.argv) > 4 else newest(['Gemini_Generated_Image_*'])
    os.makedirs(DRIVE, exist_ok=True)
    for tag, f in (('gptapp', gpt), ('gemapp', gem)):
        if not f: print('no file for', tag); continue
        im = Image.open(f).convert('RGB'); shutil.copy(f, os.path.join(DRIVE, f'{view}-{tag}{os.path.splitext(f)[1]}'))
        w = im.copy(); w.thumbnail((1536, 1536)); w.save(os.path.join(WEB, f'{view}-{tag}.jpg'), quality=85)
        print(tag, os.path.basename(f), im.size, '-> gallery + Drive')
