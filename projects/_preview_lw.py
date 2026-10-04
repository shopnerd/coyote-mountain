# quick preview of the line-work drawings without the whole pack
import matplotlib; matplotlib.use('Agg'); import matplotlib.pyplot as plt, numpy as np, glob, os, sys
import matplotlib.font_manager as fm
for f in glob.glob('fonts/PJS-*.ttf'): fm.fontManager.addfont(f)
plt.rcParams['font.family'] = ['Plus Jakarta Sans', 'DejaVu Sans']
INK, MUTED, CLAY, PAPER = '#2a2824', '#6a655a', '#b5602e', '#faf8f3'
STONE2, STAKE2, STEEL2, CONC2, DIRT2 = '#cdb892', '#8a6a48', '#3a3f44', '#d7d3cb', '#e7d8bd'
PAGES = []
def newpage():
    f = plt.figure(figsize=(17, 11)); f.patch.set_facecolor(PAPER); return f
def heading(fig, es, en): fig.text(.02, .945, es, fontsize=30, weight='bold')
def para(fig, x, y, es, en, w=80, fs=10): return y
def tblock(*a, **k): pass
def nxt(): return 1
exec(open('stable_pages_0928.py', encoding='utf-8').read())
which = sys.argv[1]
if which == 'plan': barn_plan()
else: truss_page()
PAGES[-1].savefig(sys.argv[2], dpi=int(sys.argv[3]) if len(sys.argv) > 3 else 110); print('saved')
