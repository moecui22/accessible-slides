"""Build the before/after demo slides used in the README."""
import matplotlib; matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np

W, H, DPI = 1600, 900, 100
x = np.linspace(0, 10, 60)
rng = np.random.default_rng(7)
ya = 62 + 3.1 * x + rng.normal(0, 2.2, x.size)
yb = 60 + 1.4 * x + rng.normal(0, 2.2, x.size)

def frame(bad):
    fig = plt.figure(figsize=(W / DPI, H / DPI), dpi=DPI, facecolor='white')
    tsz, bsz = (26, 15) if bad else (40, 28)
    tcol, bcol = ('#333333', '#9a9a9a') if bad else ('#111111', '#454545')
    fig.text(0.06, 0.88, 'Accuracy improves with training', fontsize=tsz,
             color=tcol, weight='bold' if not bad else 'normal')
    fig.text(0.06, 0.08, 'Older and younger adults, 60 sessions'
             if bad else 'Older and younger adults, 60 sessions',
             fontsize=bsz, color=bcol)
    ax = fig.add_axes([0.10, 0.22, 0.82, 0.58])
    if bad:
        ax.plot(x, ya, color='#d62728', lw=2, label='Younger')
        ax.plot(x, yb, color='#2ca02c', lw=2, label='Older')
        ax.legend(fontsize=13, frameon=False)
    else:
        ax.plot(x, ya, color='#0072b2', lw=4, ls='-')
        ax.plot(x, yb, color='#d55e00', lw=4, ls=(0, (5, 3)))
        ax.text(x[-1] + 0.2, ya[-1], 'Younger', color='#0072b2', fontsize=24,
                va='center', weight='bold')
        ax.text(x[-1] + 0.2, yb[-1], 'Older', color='#d55e00', fontsize=24,
                va='center', weight='bold')
        ax.set_xlim(0, 12.4)
    ax.set_xlabel('Session', fontsize=bsz, color=bcol)
    ax.set_ylabel('Accuracy (%)', fontsize=bsz, color=bcol)
    ax.tick_params(labelsize=bsz - 2, colors=bcol)
    for s in ('top', 'right'):
        ax.spines[s].set_visible(False)
    for s in ('left', 'bottom'):
        ax.spines[s].set_color('#999999' if bad else '#454545')
    return fig

for name, bad in (('demo_before', True), ('demo_after', False)):
    f = frame(bad)
    f.savefig('assets/%s.png' % name, dpi=DPI, facecolor='white')
    plt.close(f)
    print('wrote assets/%s.png' % name)
