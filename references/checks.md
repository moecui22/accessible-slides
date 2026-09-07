# The checks: thresholds, sources, arithmetic

## 1. Contrast

Ratio is the WCAG 2.x relative-luminance ratio:

```
L = 0.2126 R + 0.7152 G + 0.0722 B      (R,G,B linearised from sRGB)
ratio = (Lmax + 0.05) / (Lmin + 0.05)
```

| Context | Body | Large (≥ 2× body) | Source |
|---|---|---|---|
| Projected, lit room | 7:1 | 4.5:1 | WCAG AAA used as the projection default |
| Projected, dark room | 4.5:1 | 3:1 | WCAG AA |
| Screen share / webinar | 4.5:1 | 3:1 | WCAG 2.2 AA, its intended context |

Why raise it for projection: WCAG's levels were set for self-luminous displays
viewed at reading distance under controlled light. A projector adds ambient
light to the black level, so the delivered ratio is strictly lower than the
authored one — often by a large factor. Treating AAA as the projection floor is
a deliberate, stated choice, not a misreading of the standard.

Known limitation, state it if asked: the WCAG ratio is a poor model of perceived
contrast for light text on dark backgrounds and for thin strokes. Where a second
opinion matters, compute APCA Lc as well and report both. Do not silently
substitute one for the other.

## 2. Colour-vision separability

1. Simulate each colour under protanopia and deuteranopia (Viénot et al. 1999;
   Brettel et al. 1997).
2. Convert both simulated colours to CIELAB (D65).
3. Compute ΔE2000 (Sharma, Wu & Dalal 2005).

| ΔE2000 after simulation | Verdict |
|---|---|
| < 5 | fail — effectively the same colour |
| 5–15 | fail for non-adjacent elements; marginal even when adjacent |
| ≥ 15 | pass |

The 15 threshold is a design heuristic, not a psychophysical constant. It is set
above the "clearly different when compared side by side" range because slide
elements are usually separated in space and time, seen briefly, and at low
retinal illuminance — all of which raise the discrimination threshold.

## 3. Text size from room geometry

Given target x-height angle `theta` (arcmin), back-row distance `D`, screen
height `H`, x-height ratio `r` (0.52 for common sans faces), and authored slide
height `S`:

```
x_height_m = 2 * D * tan(theta_rad / 2)      ~= D * theta_rad
font_m     = x_height_m / r
fraction   = font_m / H
font_units = fraction * S
```

Target `theta` = 16–20 arcmin of x-height.

Anchor: critical print size for maximum reading speed in normal vision is about
0.2° (12 arcmin) of x-height (Legge & Bigelow 2011). 16–20 arcmin is 1.3–1.7×
that, which is the headroom for age-related acuity loss, uncorrected refractive
error, and brief exposure.

Worked values, 16:9 slide authored at 7.5 in = 540 pt, `r` = 0.52,
`theta` = 18 arcmin:

| Screen height | Back row | Minimum body text |
|---|---|---|
| 1.5 m | 8 m | 29 pt |
| 2.0 m | 10 m | 27 pt |
| 2.0 m | 15 m | 41 pt |
| 3.0 m | 20 m | 36 pt |
| 4.0 m | 25 m | 34 pt |

This is where the folk "30-point rule" comes from — it is roughly right for a
mid-sized room and wrong at both ends. Compute it, do not recite it.

## 4. Greyscale survival

Convert the slide to luminance only. Every distinction that carried meaning must
still be visible. This single check catches most Rule 1 violations without any
simulation at all, and it is the one to run first when time is short.

## References

- Brettel, H., Viénot, F., & Mollon, J. D. (1997). Computerized simulation of
  color appearance for dichromats. *JOSA A*, 14(10), 2647–2655.
- Viénot, F., Brettel, H., & Mollon, J. D. (1999). Digital video colourmaps for
  checking the legibility of displays by dichromats. *Color Research &
  Application*, 24(4), 243–252.
- Sharma, G., Wu, W., & Dalal, E. N. (2005). The CIEDE2000 color-difference
  formula. *Color Research & Application*, 30(1), 21–30.
- Legge, G. E., & Bigelow, C. A. (2011). Does print size matter for reading?
  *Journal of Vision*, 11(5):8.
- Okabe, M., & Ito, K. (2008). Color universal design.
- W3C. Web Content Accessibility Guidelines (WCAG) 2.2.
