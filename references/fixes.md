# Standard fix for each failure

## Red-vs-green series in a chart

1. Recolour to `#0072b2` (blue) and `#d55e00` (vermillion).
2. Add a second channel: solid vs dashed for lines, or hatching for fills.
3. Replace the legend with direct labels at the end of each series.

Step 3 does more for comprehension than steps 1 and 2 combined. A legend forces
a colour-matching task; a direct label removes it.

## Light grey body text

Grey text is almost always a designer reflex, not a decision. Replace with a
darker grey at the required ratio rather than reducing size or weight.

| On white, need | Use |
|---|---|
| 4.5:1 | `#767676` |
| 7:1 | `#595959` |
| 10:1 | `#454545` |

## Text over a photograph

In order of preference:

1. Move the text off the image into a solid panel.
2. Add a solid plate behind the text (85%+ opacity), not a gradient.
3. Darken or blur the whole image heavily, then place text.

A drop shadow is not a fix. It raises measured contrast slightly and perceived
legibility barely, and it fails completely on a busy background.

## Text too small

Do not shrink the font to fit the content. Cut the content.

If a slide needs 12 pt to fit, it is not a slide — it is a handout. Split it,
move the detail to an appendix, or say the sentence out loud instead of writing
it.

## Traffic-light table

Replace the colour-only cell fill with:

- an icon or symbol in the cell (`✓` / `!` / `✗`), plus
- a luminance step, not a hue step, if fills are kept

Colour then becomes redundant reinforcement rather than the signal.

## Thin strokes and hairlines

Contrast requirements assume a stroke wide enough to be sampled by the visual
system at that distance. Below about 2 px per metre of viewing distance a line
loses effective contrast regardless of its colour. Thicken lines before
recolouring them.

## Rainbow / jet colormap

Replace with viridis or cividis. If the figure is already published and cannot
be regenerated, say so explicitly rather than recolouring an image and
introducing errors.

## When the deck cannot be fixed in time

Rank by cost of failure, not by count:

1. Anything where a wrong reading changes a decision (a result, a number, a
   recommendation).
2. Body text below the contrast floor.
3. Everything else.

Fix 1 and 2 and stop. A deck with two real fixes shipped beats a full audit
delivered after the talk.
