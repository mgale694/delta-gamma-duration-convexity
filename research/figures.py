"""Render the research figures from make evidence CSV outputs."""
import csv
from collections import defaultdict
from pathlib import Path

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

output = Path('outputs')
cases = defaultdict(list)
with (output / 'scenarios.csv').open() as stream:
    for row in csv.DictReader(stream):
        cases[row['case']].append(row)

styles = {'exact': ('#172e45', '-'), 'linear': ('#b45022', '--'), 'second': ('#087b74', '-.')}
plt.rcParams.update({'font.size': 11, 'axes.spines.top': False, 'axes.spines.right': False,
                     'figure.facecolor': 'white', 'axes.titlelocation': 'left'})


def panel(ax, case, xlabel, ylabel, labels, error=False):
    rows = cases[case]
    for key, label in labels.items():
        field = key + '_error_pct' if error else key
        y = [float(r[field]) if r[field] else float('nan') for r in rows]
        color, style = styles[key]
        ax.plot([float(r['shock']) for r in rows], y, style, color=color, lw=2.2, label=label)
    ax.axhline(0, lw=.7, color='#82909c', zorder=0)
    ax.grid(axis='y', lw=.5, alpha=.3)
    ax.set(xlabel=xlabel, ylabel=ylabel)
    ax.legend(frameon=False, fontsize=9)


bond = dict(exact='Repriced', linear='DV01', second='DV01 + convexity')
call = dict(exact='Repriced', linear='Delta', second='Delta + gamma')
fig, axes = plt.subplots(2, 2, figsize=(11, 7.5), layout='constrained')
for j, (case, xlabel, ylabel, labels, title) in enumerate([
    ('bond-5y-zero', 'Yield move (bp)', 'P&L per £1,000 face (£)', bond, 'Five-year zero-coupon bond'),
    ('call-1y', 'Spot move (%)', 'P&L per share (£)', call, 'One-year European call')]):
    panel(axes[0, j], case, xlabel, ylabel, labels)
    axes[0, j].set_title(title, fontweight='bold')
    panel(axes[1, j], case, xlabel, 'Absolute error (% of exact P&L)',
          {k: v for k, v in labels.items() if k != 'exact'}, error=True)
fig.suptitle('How far does the starting slope take you?', fontsize=19)
fig.savefig(output / 'bond-and-call.png', dpi=180)
plt.close(fig)

fig, axes = plt.subplots(1, 2, figsize=(11, 4.4), layout='constrained')
for ax, case, title in zip(axes, ('call-1y', 'call-7d'), ('One year remaining', 'Seven days remaining')):
    panel(ax, case, 'Spot move (%)', 'P&L per share (£)', call)
    ax.set_title(title, fontweight='bold')
    ax.set_ylim(-13, 42)
axes[1].annotate('A £2.00 gain predicted\nfor a £1.15 loss', xy=(-10, 2.00016), xytext=(-17, 23),
                 fontsize=10, arrowprops={'arrowstyle': '->', 'color': '#506070'})
fig.suptitle('Same spot shock, different time to expiry', fontsize=19)
fig.savefig(output / 'expiry-stress.png', dpi=180)
