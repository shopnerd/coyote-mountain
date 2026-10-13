"""Centro Equino's publish = the general tool with this project's settings (13 Oct 2026). Same command as before:

    python publish_pack.py "what changed"            (add --dry-run to test; --yes, --commit-all, --quiet N as in tools/publish_pack.py)

Any other project: write its own <name>.publish.json beside its build and run  python tools/publish_pack.py <that file> "note".
"""
import os, subprocess, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.exit(subprocess.call([sys.executable, os.path.join(HERE, '..', 'tools', 'publish_pack.py'), os.path.join(HERE, 'equino.publish.json'), *sys.argv[1:]]))
