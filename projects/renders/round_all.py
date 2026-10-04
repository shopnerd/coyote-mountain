"""One round of fresh options for every rendering in the pack (4 Oct 2026, Will: "one round of updating all current renders, maybe five
options per render"). Each view gets five, from the current model:
  photo views:  golden (Gemini + OpenAI), dawn, storm, blue (Gemini)      -> light fans
  site models:  left, right, high, closer, wider (Gemini)                 -> camera fans (studio shots have no weather)
Results land in the gallery's "Abanico de cámaras · Camera fan" section, one block per view.

    python round_all.py            (needs the viewer served on 127.0.0.1:8792)
"""
import subprocess, sys, os
HERE = os.path.dirname(os.path.abspath(__file__))
PHOTO = ['el-west-horse', 'el-north', 'el-south', 'el-east', '1-hero-sw', '5-corridor-out', '2-corridor', '8-stable', '10-stable-aisle',
         '14-bleachers-high', '23-picnic-side', 'p4-site-ne', '4-hill-s']   # 4 Oct: + the hill view (pack p5, E-1)
BLOCK = ['b3-sw', 'b4-nw']
def run(*a):
    p = subprocess.run([sys.executable, 'fan.py', *a], cwd=HERE, capture_output=True, text=True)
    print(f"--- fan.py {' '.join(a)}"); print('\n'.join(l for l in (p.stdout + p.stderr).splitlines() if 'ok' in l or 'FAIL' in l or 'published' in l or 'Error' in l)[-1500:], flush=True)
for v in PHOTO:
    run(v, '--light', '--tags', 'golden,dawn,storm,blue', '--engines', 'google')
    run(v, '--light', '--tags', 'golden', '--engines', 'openai')
for v in BLOCK:
    run(v, '--tags', 'left,right,high,closer,wider', '--engines', 'google')
print('ROUND DONE', flush=True)
