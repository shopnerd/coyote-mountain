"""Publish the Centro Equino pack in ONE command (13 Oct 2026, Will: "save locally, push sparingly; whoever is in charge
publishes"). Does, in order, what was done by hand ten times on 12 Oct:

  1. fetch both repos (coyote-studio, will-os) and show what the other person pushed; merge it (stops on a conflict)
  2. stop if someone else published the web pack in the last --quiet minutes (default 10), unless --yes
  3. stop if pack sources have uncommitted edits, unless --commit-all (then they are committed with the note)
  4. number the build one past the version that is LIVE on the site, never past the local file
  5. pull the editor's saved layout (pull_layout.py), build (pack.py), check: no missing photos, page count, PDF exists
  6. fetch again; stop without pushing if anything new arrived during the build
  7. copy the PDF over the shared name in Drive, commit both repos, push each once
  8. wait until the live site shows the new version, then report

    python publish_pack.py "what changed"            # the real thing
    python publish_pack.py "what changed" --dry-run  # everything up to the build, into a scratch folder; pushes nothing
    options: --yes (publish even if the other person just did) · --commit-all (commit pending source edits) · --quiet N
"""
import argparse, datetime as dt, json, os, re, shutil, subprocess, sys, tempfile, time, urllib.request

HERE = os.path.dirname(os.path.abspath(__file__)); COYOTE = os.path.dirname(HERE)
WILLOS = os.path.abspath(os.path.join(COYOTE, '..', 'will-os'))
SITE = os.environ.get('EQUINO_SITE', 'https://will.100xbtr.com')
OUTDIR = os.environ.get('EQUINO_PACK_DIR', 'G:/My Drive/MEXICO/Chichihaus/2026-09-23 Centro Equino pack')
SHARED = 'Centro-Equino-pack-11x17-2026-09-23.pdf'          # the name everyone's Drive link points at
SOURCES = ('projects/',)                                     # coyote paths the pack is built from
OUTPUTS = ('projects/pack.py', 'projects/pack_layout.json', 'projects/pack_photo_report.txt')
IGNORE = ('projects/renders/model/', 'projects/renders/check/', 'projects/prev-', 'projects/_')   # model shots, checks, previews, backups: not pack sources
CO = 'Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>'

try: sys.stdout.reconfigure(encoding='utf-8', errors='replace')
except Exception: pass
def say(*a): print(*a, flush=True)
def stop(msg, code=2): say('\nSTOPPED: ' + msg); report('warn' if code == 2 else 'fail', msg); sys.exit(code)
def git(repo, *a, check=True, raw=False):
    p = subprocess.run(['git', '-C', repo, *a], capture_output=True, text=True, encoding='utf-8', errors='replace')
    if check and p.returncode: stop(f'git {" ".join(a)} in {os.path.basename(repo)} failed:\n{p.stderr.strip()[-800:]}', 1)
    return p.stdout if raw else p.stdout.strip()
def live():
    with urllib.request.urlopen(f'{SITE}/equino/pack/pages.json?x={time.time():.0f}', timeout=30) as r: return json.load(r)
def vnum(name): m = re.search(r'-v(\d+)\.pdf', name or ''); return int(m.group(1)) if m else 0
def report(status, note):                                    # every automation reports its own run (will-os/report-status.js), best effort
    rs = os.path.join(WILLOS, 'report-status.js')
    if os.path.exists(rs): subprocess.run(['node', rs, 'equino-publish', status, note[:180]], capture_output=True, cwd=WILLOS)

def incoming(repo, paths=()):
    git(repo, 'fetch', '-q')
    return git(repo, 'log', '--format=%h|%an|%ar|%s', 'HEAD..@{u}', *(['--'] + list(paths) if paths else []))

def main():
    ap = argparse.ArgumentParser(); ap.add_argument('note'); ap.add_argument('--dry-run', action='store_true')
    ap.add_argument('--yes', action='store_true'); ap.add_argument('--commit-all', action='store_true'); ap.add_argument('--quiet', type=int, default=10)
    a = ap.parse_args()

    say('1 · what the other side pushed')
    for repo in (COYOTE, WILLOS):
        new = incoming(repo)
        for line in new.splitlines(): h, who, when, msg = line.split('|', 3); say(f'   {os.path.basename(repo)}: {when:>14}  {who:<13} {msg[:100]}')
        if new:
            p = subprocess.run(['git', '-C', repo, 'pull', '-q', '--no-rebase'], capture_output=True, text=True)
            if p.returncode: stop(f'merging {os.path.basename(repo)} hit a conflict; nothing was published. Resolve it, then run again.\n{p.stdout[-500:]}{p.stderr[-500:]}', 1)
    say('   up to date')

    say('2 · has anyone just published?')
    last = git(WILLOS, 'log', '-1', '--format=%ct|%an|%s', '--', 'equino/pack')
    if last:
        ts, who, msg = last.split('|', 2); mins = (time.time() - int(ts)) / 60
        me = git(WILLOS, 'config', 'user.name', check=False)
        say(f'   last web publish {mins:.0f} min ago by {who}: {msg[:90]}')
        if who != me and mins < a.quiet and not a.yes: stop(f'{who} published {mins:.0f} min ago. Check with them, then run again with --yes.')

    say('3 · uncommitted edits to the pack sources')
    dirty = [l[3:] for l in git(COYOTE, 'status', '--porcelain', '--', *SOURCES, raw=True).splitlines() if l[:2].strip() and not l.startswith('??')]
    dirty = [f for f in dirty if f not in OUTPUTS and not f.startswith(IGNORE)]
    for f in dirty: say('   ' + f)
    if dirty and not a.commit_all and not a.dry_run: stop('these edits would be published but not saved in git. Commit them, or run again with --commit-all.')

    say('4 · version')
    L = live(); lv = vnum(L.get('version')); src = open(os.path.join(HERE, 'pack.py'), encoding='utf-8').read()
    lo = vnum(re.search(r"Centro-Equino-pack-11x17-[\d-]+-v\d+\.pdf", src).group(0)); nv = max(lv, lo) + 1
    name = f'Centro-Equino-pack-11x17-{dt.date.today().isoformat()}-v{nv}.pdf'
    say(f'   live v{lv} ({L.get("pages")} pages) · local file v{lo} → building v{nv}')
    src2 = re.sub(r"Centro-Equino-pack-11x17-[\d-]+-v\d+\.pdf", name, src, count=1)
    if not a.dry_run: open(os.path.join(HERE, 'pack.py'), 'w', encoding='utf-8', newline='\n').write(src2)

    say('5 · build')
    env = dict(os.environ)
    if a.dry_run:
        tmp = tempfile.mkdtemp(prefix='equino-dry-'); env.update(EQUINO_OUT_DIR=tmp, EQUINO_WEB_DIR=os.path.join(tmp, 'web'))
    else:
        p = subprocess.run([sys.executable, 'pull_layout.py'], cwd=HERE, capture_output=True, text=True); say('   ' + (p.stdout.strip().splitlines() or ['layout pulled'])[0][:120])
    t0 = time.time()
    p = subprocess.run([sys.executable, 'pack.py'], cwd=HERE, capture_output=True, text=True, env=env, encoding='utf-8', errors='replace')
    if p.returncode: stop('the build failed:\n' + (p.stderr or p.stdout)[-1500:], 1)
    built = re.search(r"Centro-Equino-pack-11x17-[\d-]+-v\d+\.pdf", open(os.path.join(HERE, 'pack.py'), encoding='utf-8').read()).group(0)   # the dry run builds under the local file's name
    pdf = os.path.join(env.get('EQUINO_OUT_DIR', OUTDIR), built)
    if not os.path.exists(pdf): stop(f'the build ran but {pdf} is missing.', 1)
    rep = open(os.path.join(HERE, 'pack_photo_report.txt'), encoding='utf-8').read(); miss = rep.count('MISSING')
    import pymupdf; pages = len(pymupdf.open(pdf))
    say(f'   built in {(time.time() - t0) / 60:.1f} min · {pages} pages · missing photos: {miss}')
    if miss: stop(f'{miss} photo(s) are missing (see pack_photo_report.txt); nothing was pushed.')
    if a.dry_run: say(f'\nDRY RUN done: {pdf}\nNothing was pushed. Run without --dry-run to publish.'); return

    say('6 · anything new while building?')
    late = [(r, incoming(r)) for r in (COYOTE, WILLOS)]
    if any(n for _, n in late): stop('new pushes arrived during the build:\n' + '\n'.join(f'   {os.path.basename(r)}: {n}' for r, n in late if n) + '\nRun again to include them; nothing was pushed.')

    say('7 · publish')
    shutil.copyfile(pdf, os.path.join(OUTDIR, SHARED)); say(f'   shared PDF updated: {SHARED}')
    if dirty: git(COYOTE, 'add', '--', *dirty)
    git(COYOTE, 'add', '--', *OUTPUTS); git(WILLOS, 'add', '--', 'equino/pack')
    msg = f'Centro Equino pack v{nv}: {a.note}\n\n{CO}'
    for repo in (COYOTE, WILLOS):
        if git(repo, 'diff', '--cached', '--name-only'): git(repo, 'commit', '-q', '-m', msg)
        git(repo, 'push', '-q')
    say('   pushed both repos once')

    say('8 · waiting for the live site')
    for _ in range(30):
        time.sleep(20)
        try: L = live()
        except Exception: continue
        if vnum(L.get('version')) == nv:
            say(f'\nLIVE: v{nv}, {L.get("pages")} pages · {SITE}/equino/pack/'); report('ok', f'v{nv} live, {pages} pages: {a.note}'); return
    stop(f'pushed v{nv}, but the site still shows v{vnum(L.get("version"))} after 10 min. Check the Netlify deploy.', 1)

if __name__ == '__main__':
    main()
