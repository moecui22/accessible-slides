---
name: accessible-slides
description: "Audit and fix slides, posters and figures so people with vision loss can actually read them - colour-vision deficiency, reduced contrast sensitivity, and text too small to resolve from the back of the room. Use when making, reviewing or fixing a presentation, conference poster or chart, and whenever accessibility, colour blindness, contrast, readability, WCAG, Section 508 or AODA come up."
license: MIT
---

# Accessible Slides

Most decks are checked on a laptop, 60 cm from a young pair of eyes, in a dark
room. They are then shown on a washed-out projector, 15 m from an audience whose
median age is 45 and 8% of whose men cannot separate the red line from the green
one.

This skill checks a deck against how vision actually works, not against how it
looked on the author's monitor.

## The three failures, in order of how often they matter

1. **Meaning carried by hue alone.** Red-vs-green lines, a red "bad" cell and a
   green "good" cell, a legend that differs only in colour. Lost to ~8% of men
   and ~0.5% of women.
2. **Contrast that survives a monitor but not a projector.** Ambient light
   raises the black level, so an authored 10:1 can arrive as 3:1. Age-related
   loss of contrast sensitivity sits on top of that.
3. **Text sized by eye instead of by visual angle.** "It looks fine on my
   laptop" is not a claim about the back row.

## Operating procedure

**When creating new slides:** apply the rules as you build. Do not generate a
deck and audit it afterwards - the fixes get structural fast.

**When auditing an existing deck:**

1. Establish the room. Ask, or assume:
   - default: 2.0 m screen height, back row at 15 m
   - screen share / webinar: a 0.3 m display at 0.6 m - plain WCAG applies
2. Extract the palette and the text sizes.
   - `.pptx` → `python-pptx`
   - HTML deck → read the CSS
   - PDF or images only → render pages to PNG, then use `scripts/simulate_cvd.py`
3. Run `scripts/audit.py` for the numbers. Never judge contrast by eye - that is
   the exact judgement the author already got wrong.
4. Run `scripts/simulate_cvd.py` on at least one rendered slide and actually look
   at the output.
5. Report failures with the fix, not just the score.

## The rules

### Rule 1 - Hue is never the only channel

Every distinction must survive being converted to greyscale. Add a second,
redundant channel:

- lines → dash pattern, marker shape, direct end-of-line labels
- categorical fills → hatching or a luminance step
- status → an icon or a word, not a colour alone

When colour must carry category, use a CVD-safe palette. Okabe–Ito is the
default. See `references/palettes.md`.

### Rule 2 - Projection contrast sits above the WCAG floor

| Context | Body text | Large text (≥ 2× body) |
|---|---|---|
| Projected, lit room | **7:1** | 4.5:1 |
| Projected, dark room | 4.5:1 | 3:1 |
| Screen share / webinar | 4.5:1 (WCAG 2.2 AA) | 3:1 |

WCAG's 4.5:1 assumes a controlled, self-luminous display at reading distance. A
projector in a lit room does not meet that assumption. Default to 7:1 and relax
only when the room is known to be dark.

Never set body text directly on a photograph. Use a solid or heavily blurred
plate.

### Rule 3 - Size text by visual angle, not by taste

Target **16–20 arcmin of x-height at the back row.**

That is roughly 1.5–2× the critical print size for maximum reading speed in
normal vision (~12 arcmin), leaving headroom for age-related acuity loss and for
a viewer who is not perfectly corrected.

`scripts/audit.py --room` converts this into a minimum font size for the actual
room. For a 2 m screen with a back row at 15 m it lands near 6% of slide height,
which is where the folk "30-point rule" comes from. This tool derives that
number instead of asserting it, and moves it when the room changes.

### Rule 4 - Colour pairs stay separable after simulation

Any two colours carrying different meanings must remain distinguishable when
simulated as protanopia and deuteranopia. Target **ΔE2000 ≥ 15** between every
meaning-bearing pair in every simulation.

## Reporting format

Per slide, worst failure first:

```
Slide 4  FAIL  contrast   2.8:1  #8a8a8a on #ffffff, body text
                          fix: #595959 (7.0:1)
Slide 7  FAIL  CVD        #d62728 vs #2ca02c → dE2000 5.0 under deuteranopia
                          fix: #d55e00 / #0072b2, plus dashed vs solid
Slide 9  WARN  text size  22 pt = 12 arcmin at 15 m; need 34 pt
```

End with the single highest-impact change. Not a list of twelve.

## References

Read these only on reaching the relevant step:

- `references/vision-loss.md` - what each condition does, and who has it
- `references/palettes.md` - CVD-safe palettes, and what to stop using
- `references/checks.md` - thresholds, their sources, how to apply them
- `references/fixes.md` - the standard fix for each failure mode

## Scripts

- `scripts/audit.py` - contrast ratios, CVD confusability (ΔE2000), and minimum
  text size from room geometry. Standard library only.
- `scripts/simulate_cvd.py` - render an image as protan / deutan / tritan and
  build a labelled contact sheet. Needs `numpy` and `Pillow`.

## Credits

Colour-vision simulation follows Viénot, Brettel & Mollon (1999) and Brettel,
Viénot & Mollon (1997). Colour difference is CIEDE2000 (Sharma, Wu & Dalal,
2005). Reading-size targets follow the critical-print-size literature (Legge &
Bigelow, 2011). Categorical palette is Okabe & Ito (2008).
