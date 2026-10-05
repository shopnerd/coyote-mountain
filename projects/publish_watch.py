"""The editor's Publish button, PC side (5 Oct 2026, Will). Run every few minutes by Windows Task Scheduler ("Equino pack publish").

When someone presses Publicar · Publish at will.100xbtr.com/equino/pack/edit/, the layout API records publish.state = 'requested'.
This script sees it, reports 'building', runs pull_layout.py + pack.py, copies the PDF over the shared name on Drive, commits and
pushes will-os (ONE Netlify deploy) and coyote-studio, then reports 'done' (or 'failed' with the reason). No request: it exits at once.

    python publish_watch.py          (from projects/)
"""
import json, os, shutil, subprocess, sys, urllib.request, datetime
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.dirname(HERE); WILLOS = os.path.join(os.path.dirname(ROOT), 'will-os')
API = 'https://will.100xbtr.com/equino/api/layout'
OUTDIR = os.environ.get('EQUINO_PACK_DIR', 'G:/My Drive/MEXICO/Chichihaus/2026-09-23 Centro Equino pack')
LOG = os.path.join(HERE, 'publish_watch.log')

def log(msg):
    with open(LOG, 'a', encoding='utf-8') as f: f.write(f'{datetime.datetime.now():%Y-%m-%d %H:%M:%S}  {msg}\n')
def api(body=None):
    req = urllib.request.Request(API, data=json.dumps(body).encode() if body else None, headers={'content-type': 'application/json', 'User-Agent': 'publish_watch'})
    with urllib.request.urlopen(req, timeout=60) as r: return json.loads(r.read())
def run(cmd, cwd, timeout=1800):
    env = {**os.environ, 'PYTHONUTF8': '1'}
    p = subprocess.run(cmd, cwd=cwd, env=env, capture_output=True, text=True, timeout=timeout)
    if p.returncode: raise RuntimeError(f'{" ".join(cmd[:2])} failed: {(p.stderr or p.stdout).strip()[-240:]}')
    return p.stdout

def main():
    pub = (api() or {}).get('publish') or {}
    if pub.get('state') != 'requested': return
    who = pub.get('by') or '?'; log(f'publish requested by {who}')
    api({'op': 'publish-status', 'state': 'building', 'note': ''})
    try:
        run([sys.executable, 'pull_layout.py'], HERE, 300)
        out = run([sys.executable, 'pack.py'], HERE)
        src = sorted((f for f in os.listdir(OUTDIR) if f.startswith('Centro-Equino-pack-11x17-2026-10') and f.endswith('.pdf')), key=lambda f: os.path.getmtime(os.path.join(OUTDIR, f)))[-1]
        shutil.copy(os.path.join(OUTDIR, src), os.path.join(OUTDIR, 'Centro-Equino-pack-11x17-2026-09-23.pdf'))
        msg = f'Pack published from the layout editor (by {who})'
        for repo, paths in ((ROOT, ['projects/pack_layout.json', 'projects/_pack_build.log', 'projects/pack_photo_report.txt']), (WILLOS, ['equino/pack'])):
            run(['git', 'add', '-A', '--', *[q for q in paths if os.path.exists(os.path.join(repo, q))]], repo, 120)
            if subprocess.run(['git', 'diff', '--cached', '--quiet'], cwd=repo).returncode:
                run(['git', 'commit', '-q', '-m', msg], repo, 120)
            run(['git', 'pull', '-q', '--rebase', '--autostash'], repo, 300)
            run(['git', 'push', '-q'], repo, 300)
        api({'op': 'publish-status', 'state': 'done', 'note': src})
        log(f'done: {src}')
    except Exception as e:
        log(f'FAILED: {e}')
        api({'op': 'publish-status', 'state': 'failed', 'note': str(e)[:280]})

if __name__ == '__main__':
    try: main()
    except Exception as e: log(f'watch error: {e}')
