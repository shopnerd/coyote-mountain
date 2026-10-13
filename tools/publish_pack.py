"""Publish any project's presentation pack in ONE command (13 Oct 2026, Will: "this is for a broader application, not just the
Equine Center"; "save locally, push sparingly; whoever is in charge publishes"). Each project keeps a small settings file,
<project>.publish.json, naming its repos, its build and its live site (Centro Equino's: projects/equino.publish.json).

  1. fetch the source and web repos, show what the other person pushed, merge it (stops on a conflict)
  2. stop if someone else published the web pack in the last --quiet minutes (default 10), unless --yes
  3. stop if pack sources have uncommitted edits, unless --commit-all (then they are committed with the note)
  4. number the build one past the version that is LIVE on the site, never past the local file
  5. run the build's pre-steps (e.g. pull the editor's saved layout), build, check: no missing photos, pages, PDF exists
  6. fetch again; stop without pushing if anything new arrived during the build
  7. copy the PDF over the shared name, commit both repos, push each once
  8. wait until the live site shows the new version, then report

    python tools/publish_pack.py projects/equino.publish.json "what changed"            # publish
    python tools/publish_pack.py projects/equino.publish.json "what changed" --dry-run  # build into a scratch folder, push nothing
    options: --yes · --commit-all · --quiet N
"""
import argparse, datetime as dt, json, os, re, shutil, subprocess, sys, tempfile, time, urllib.request

try: sys.stdout.reconfigure(encoding='utf-8', errors='replace')
except Exception: pass
CO = 'Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>'
C = {}                                                      # the project's settings, filled in main()

def say(*a): print(*a, flush=True)
def stop(msg, code=2): say('\nSTOPPED: ' + msg); report('warn' if code == 2 else 'fail', msg); sys.exit(code)
def git(repo, *a, check=True, raw=False):
    p = subprocess.run(['git', '-C', repo, *a], capture_output=True, text=True, encoding='utf-8', errors='replace')
    if check and p.returncode: stop(f'git {" ".join(a)} in {os.path.basename(repo)} failed:\n{p.stderr.strip()[-800:]}', 1)
    return p.stdout if raw else p.stdout.strip()
def live():
    with urllib.request.urlopen(f'{C["live_pages_json"]}?x={time.time():.0f}', timeout=30) as r: return json.load(r)
def vnum(name): m = re.search(r'-v(\d+)\.pdf', name or ''); return int(m.group(1)) if m else 0
def report(status, note):                                   # every automation reports its own run (will-os/report-status.js), best effort
    rs = os.path.join(C.get('web_repo', ''), 'report-status.js')
    if C and os.path.exists(rs): subprocess.run(['node', rs, C['report_task'], status, note[:180]], capture_output=True, cwd=C['web_repo'])
def incoming(repo):
    git(repo, 'fetch', '-q'); return git(repo, 'log', '--format=%h|%an|%ar|%s', 'HEAD..@{u}')

def load(path):
    base = os.path.dirname(os.path.abspath(path)); c = json.load(open(path, encoding='utf-8'))
    rel = lambda p: os.path.abspath(os.path.join(base, p))
    c['source_repo'], c['web_repo'], c['build_dir'] = rel(c['source_repo']), rel(c['web_repo']), rel(c['build']['dir'])
    c['version_file'] = rel(c['build']['version_file']); c['out_dir'] = os.environ.get(c.get('out_dir_env', ''), c['out_dir'])
    return c

def main():
    ap = argparse.ArgumentParser(); ap.add_argument('project'); ap.add_argument('note'); ap.add_argument('--dry-run', action='store_true')
    ap.add_argument('--yes', action='store_true'); ap.add_argument('--commit-all', action='store_true'); ap.add_argument('--quiet', type=int, default=10)
    a = ap.parse_args(); C.update(load(a.project)); S, Wb, B = C['source_repo'], C['web_repo'], C['build']
    say(f'{C["name"]} · publish{" (dry run)" if a.dry_run else ""}')

    say('1 · what the other side pushed')
    for repo in (S, Wb):
        new = incoming(repo)
        for line in new.splitlines(): h, who, when, msg = line.split('|', 3); say(f'   {os.path.basename(repo)}: {when:>14}  {who:<13} {msg[:100]}')
        if new:
            p = subprocess.run(['git', '-C', repo, 'pull', '-q', '--no-rebase'], capture_output=True, text=True)
            if p.returncode: stop(f'merging {os.path.basename(repo)} hit a conflict; nothing was published. Resolve it, then run again.\n{p.stdout[-500:]}{p.stderr[-500:]}', 1)
    say('   up to date')

    say('2 · has anyone just published?')
    last = git(Wb, 'log', '-1', '--format=%ct|%an|%s', '--', C['web_path'])
    if last:
        ts, who, msg = last.split('|', 2); mins = (time.time() - int(ts)) / 60; me = git(Wb, 'config', 'user.name', check=False)
        say(f'   last web publish {mins:.0f} min ago by {who}: {msg[:90]}')
        if who != me and mins < a.quiet and not a.yes: stop(f'{who} published {mins:.0f} min ago. Check with them, then run again with --yes.')

    say('3 · uncommitted edits to the pack sources')
    dirty = [l[3:] for l in git(S, 'status', '--porcelain', '--', *C['source_paths'], raw=True).splitlines() if l[:2].strip() and not l.startswith('??')]
    dirty = [f for f in dirty if f not in C['outputs'] and not f.startswith(tuple(C.get('ignore', [])))]
    for f in dirty: say('   ' + f)
    if dirty and not a.commit_all and not a.dry_run: stop('these edits would be published but not saved in git. Commit them, or run again with --commit-all.')

    say('4 · version')
    L = live(); lv = vnum(L.get('version')); src = open(C['version_file'], encoding='utf-8').read(); pat = B['version_pattern']
    lo = vnum(re.search(pat, src).group(0)); nv = max(lv, lo) + 1
    name = B['name_template'].format(date=dt.date.today().isoformat(), n=nv)
    say(f'   live v{lv} ({L.get("pages")} pages) · local file v{lo} → building v{nv}')
    if not a.dry_run: open(C['version_file'], 'w', encoding='utf-8', newline='\n').write(re.sub(pat, name, src, count=1))

    say('5 · build')
    env = dict(os.environ)
    if a.dry_run:
        tmp = tempfile.mkdtemp(prefix='pack-dry-'); env.update({B['test_out_env']: tmp, B['test_web_env']: os.path.join(tmp, 'web')})
    else:
        for cmd in B.get('pre', []):
            p = subprocess.run(cmd, cwd=C['build_dir'], shell=True, capture_output=True, text=True)
            if p.returncode: stop(f'pre-step "{cmd}" failed:\n{(p.stderr or p.stdout)[-800:]}', 1)
            say(f'   {cmd}: ok')
    t0 = time.time()
    p = subprocess.run(B['cmd'].replace('{python}', f'"{sys.executable}"'), cwd=C['build_dir'], shell=True, capture_output=True, text=True, env=env, encoding='utf-8', errors='replace')
    if p.returncode: stop('the build failed:\n' + (p.stderr or p.stdout)[-1500:], 1)
    built = re.search(pat, open(C['version_file'], encoding='utf-8').read()).group(0)
    pdf = os.path.join(env.get(B['test_out_env'], C['out_dir']) if a.dry_run else C['out_dir'], built)
    if not os.path.exists(pdf): stop(f'the build ran but {pdf} is missing.', 1)
    miss = 0
    if B.get('photo_report'):
        rp = os.path.join(C['build_dir'], B['photo_report']); miss = open(rp, encoding='utf-8').read().count('MISSING') if os.path.exists(rp) else 0
    try:
        import pymupdf; pages = len(pymupdf.open(pdf))
    except Exception: pages = '?'
    say(f'   built in {(time.time() - t0) / 60:.1f} min · {pages} pages · missing photos: {miss}')
    if miss: stop(f'{miss} photo(s) are missing (see {B["photo_report"]}); nothing was pushed.')
    if a.dry_run: say(f'\nDRY RUN done: {pdf}\nNothing was pushed. Run without --dry-run to publish.'); return

    say('6 · anything new while building?')
    late = [(r, incoming(r)) for r in (S, Wb)]
    if any(n for _, n in late): stop('new pushes arrived during the build:\n' + '\n'.join(f'   {os.path.basename(r)}: {n}' for r, n in late if n) + '\nRun again to include them; nothing was pushed.')

    say('7 · publish')
    if C.get('shared_pdf'): shutil.copyfile(pdf, os.path.join(C['out_dir'], C['shared_pdf'])); say(f'   shared PDF updated: {C["shared_pdf"]}')
    if dirty: git(S, 'add', '--', *dirty)
    git(S, 'add', '--', *[o for o in C['outputs'] if os.path.exists(os.path.join(S, o))]); git(Wb, 'add', '--', C['web_path'])
    msg = f'{C["name"]} pack v{nv}: {a.note}\n\n{CO}'
    for repo in (S, Wb):
        if git(repo, 'diff', '--cached', '--name-only'): git(repo, 'commit', '-q', '-m', msg)
        git(repo, 'push', '-q')
    say('   pushed both repos once')

    say('8 · waiting for the live site')
    for _ in range(30):
        time.sleep(20)
        try: L = live()
        except Exception: continue
        if vnum(L.get('version')) == nv:
            say(f'\nLIVE: v{nv}, {L.get("pages")} pages · {C["live_url"]}'); report('ok', f'v{nv} live, {pages} pages: {a.note}'); return
    stop(f'pushed v{nv}, but the site still shows v{vnum(L.get("version"))} after 10 min. Check the deploy.', 1)

if __name__ == '__main__':
    main()
