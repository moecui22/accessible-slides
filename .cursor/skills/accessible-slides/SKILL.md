---
name: accessible-slides
description: "Audit and fix slides, posters and figures so people with vision loss can actually read them: colour blindness, low contrast, and text too small to read from the back of the room. Use when making, reviewing or fixing a presentation, conference poster or chart, and whenever accessibility, colour blindness, contrast, readability, WCAG, Section 508 or AODA come up."
license: MIT
metadata:
  author: moecui22
  version: "0.2.0"
compatibility: "Requires Python 3. simulate_cvd.py also needs numpy and Pillow."
---

# Accessible Slides

Check slides, posters and figures for readers with vision loss: colour
blindness, low contrast, and text too small to read from the back of the room.

## Procedure

1. Get the room. Ask if it is not stated. Default: 2 m screen, back row at 15 m.
   Screen share or webinar: treat as a monitor at reading distance.
2. Get the colours and the font sizes.
   `.pptx` use python-pptx | HTML read the CSS | PDF or image render to PNG.
3. Run `scripts/audit.py` for the numbers. Never judge contrast by eye.
4. Run `scripts/simulate_cvd.py` on one rendered slide and look at the output.
5. Report the worst failure first, each with its fix.

Building new slides: apply the rules as you go. Do not build first and audit
after; the fixes turn structural.

## Rules

**1. Colour is never the only signal.** Every distinction must survive
greyscale. Lines get dash patterns and labels at the end; fills get hatching or
a lightness step; status gets a word or an icon. Default palette is Okabe-Ito.

**2. Contrast targets.**

| Where | Body text | Large text |
|---|---|---|
| Projector, lit room | 7:1 | 4.5:1 |
| Projector, dark room | 4.5:1 | 3:1 |
| Screen share | 4.5:1 | 3:1 |

A projector is not a monitor: room light washes out the blacks, so what the
audience gets is always worse than what you authored. Never put body text
straight onto a photo.

**3. Text size comes from the room, not from taste.** Target 16-20 arcmin of
x-height at the back row. `audit.py --room` turns that into a font size.

**4. Colour pairs must survive simulation.** Two colours that mean different
things need dE2000 of 15 or more under both protanopia and deuteranopia.

## Report format

```
Slide 4  FAIL  contrast   2.8:1  #8a8a8a on #ffffff, body text
                          fix: #595959 (7.0:1)
Slide 7  FAIL  CVD        #d62728 vs #2ca02c -> dE2000 5.0 under deuteranopia
                          fix: #d55e00 / #0072b2, plus dashed vs solid
Slide 9  WARN  text size  22 pt = 12 arcmin at 15 m; need 34 pt
```

Close with the single highest-impact change, not a list of twelve.

## Load these only when needed

| File | Read it when |
|---|---|
| `references/palettes.md` | picking or replacing colours |
| `references/fixes.md` | writing the fix for a specific failure |
| `references/checks.md` | you need a threshold's source or the size formula |
| `references/vision-loss.md` | explaining why something fails |

## Scripts

- `scripts/audit.py` contrast, colour separability, text size. Standard library only.
- `scripts/simulate_cvd.py` simulate an image, build a comparison sheet. Needs numpy and Pillow.
