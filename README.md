# Accessible Slides

**A coding-agent skill that checks slides, posters and figures against how vision
actually works — not against how they looked on your monitor.**

![Before: a red/green line chart, simulated for colour-vision deficiency](assets/hero_before.png)

Same slide, four ways of seeing it. Under deuteranopia the two lines are the
same colour and the legend is useless. About 8% of men in your audience are
looking at the bottom-left panel.

Two changes — a CVD-safe palette and direct labels instead of a legend — and it
survives every simulation:

![After: blue/orange, dashed, directly labelled](assets/hero_after.png)

---

## What this does

Point it at a deck, a poster or a figure. It reports, per slide:

- **Colour-vision failures** — pairs of meaning-bearing colours that collapse
  under protanopia or deuteranopia, measured as ΔE2000 after simulation
- **Contrast failures** — with a threshold raised for projection, because
  ambient light lifts the black level and WCAG's numbers assume a monitor
- **Text too small** — converted from real room geometry into a minimum font
  size, instead of the folk "30-point rule"

Then it gives you the fix, not just the score.

## Why this exists

Accessibility tooling is written for websites, by web developers, against a
checklist. Slides are different: they are seen once, briefly, from 15 metres,
through a projector, by an audience whose median age is 45.

This skill is built on the vision science instead — dichromat simulation from
Viénot & Brettel, colour difference from CIEDE2000, and reading-size targets
from the critical-print-size literature. Every threshold in it says where it
came from.

## Installation

### Claude Code — marketplace

```
/plugin marketplace add moecui22/accessible-slides
/plugin install accessible-slides@accessible-slides
```

### Claude Code — manual

```bash
git clone https://github.com/moecui22/accessible-slides.git
mkdir -p ~/.claude/skills
cp -R accessible-slides ~/.claude/skills/accessible-slides
```

### Other coding agents

Point your agent at `SKILL.md` in this repo, or clone it into whatever
directory your agent reads skills from. The skill is plain Markdown plus two
Python scripts; nothing is Claude-specific.

## Usage

Just describe what you want:

```
Audit my talk deck for accessibility. Back row is about 12 m from a 2 m screen.
```

```
Check whether these figure colours work for colour-blind readers:
#d62728 #2ca02c #1f77b4
```

```
Make this poster readable from 3 m for someone with early cataract.
```

The skill will ask for the viewing geometry if you have not given it, because
the text-size answer is meaningless without it.

## The scripts, standalone

Both run on their own, no agent required.

```bash
# Which of these colours become confusable?
python3 scripts/audit.py --colors "#d62728,#2ca02c,#0072b2,#d55e00"

# Is this text contrast good enough, and what should it be?
python3 scripts/audit.py --contrast "#8a8a8a" "#ffffff"

# How big must body text be in this room?
python3 scripts/audit.py --room --distance 15 --screen-height 2.0 --font 24

# See a rendered slide as a dichromat sees it
python3 scripts/simulate_cvd.py slide.png --sheet sheet.png
```

`audit.py` uses the standard library only. `simulate_cvd.py` needs `numpy` and
`Pillow`.

Sample output:

```
  FAIL  #d62728 vs #2ca02c   normal  71.8 | protan  27.3 | deutan   5.0 | tritan  70.6
  PASS  #0072b2 vs #d55e00   normal  49.6 | protan  55.2 | deutan  62.4 | tritan  78.4

Contrast #8a8a8a on #ffffff = 3.45:1
  projected, lit room (body)       need  7.0:1  FAIL
  nearest passing neutral at 7.0:1 -> #595959 (7.00:1)

  Your 24 pt text = 10.6 arcmin at the back row  [FAIL, need 41 pt]
```

## Design principles

**Hue is never the only channel.** A CVD-safe palette with a colour-only legend
is less accessible than an unsafe palette with dashed lines and direct labels.
Redundant encoding beats colour choice.

**Compute, don't recite.** The "30-point rule" is roughly right for a mid-sized
room and wrong at both ends. This tool derives the number from the room.

**Projection is not a monitor.** WCAG's 4.5:1 was set for a controlled,
self-luminous display at reading distance. Defaulting to it for a projector is
a category error.

**Rank by cost of failure.** A deck with the two changes that matter, shipped
before the talk, beats a complete audit delivered after it.

## What this does not do

Stated plainly, because accessibility tools that overclaim are worse than none:

- It does not check screen-reader compatibility, alt text, reading order or
  keyboard navigation. Those matter and are covered well elsewhere.
- The WCAG contrast ratio is a poor model of perceived contrast for light-on-dark
  text and for thin strokes. Where that matters, compute APCA as well.
- Dichromat simulation is a model of *dichromacy*. Most colour-vision deficiency
  is anomalous trichromacy, which is milder and more variable. Treat the
  simulation as a worst case, not a prediction.
- The ΔE2000 ≥ 15 threshold is a design heuristic chosen for briefly-viewed,
  spatially-separated slide elements. It is not a psychophysical constant.
- It cannot tell you whether the slide is worth showing.

## Credits

- Brettel, Viénot & Mollon (1997), *JOSA A* 14(10) — dichromat simulation
- Viénot, Brettel & Mollon (1999), *Color Res. Appl.* 24(4) — linear-RGB simulation
- Sharma, Wu & Dalal (2005), *Color Res. Appl.* 30(1) — CIEDE2000
- Legge & Bigelow (2011), *Journal of Vision* 11(5):8 — critical print size
- Okabe & Ito (2008) — colour universal design palette
- W3C — WCAG 2.2

## License

MIT
