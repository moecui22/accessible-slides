# Palettes

## Default: Okabe–Ito (8 colours, CVD-safe)

| Name | Hex |
|---|---|
| Black | `#000000` |
| Orange | `#e69f00` |
| Sky blue | `#56b4e9` |
| Bluish green | `#009e73` |
| Yellow | `#f0e442` |
| Blue | `#0072b2` |
| Vermillion | `#d55e00` |
| Reddish purple | `#cc79a7` |

Use in this order for categorical series. The first four are separable under
both deutan and protan simulation. Yellow (`#f0e442`) has very high luminance —
use it for fills, not for text or thin lines on white.

## Safe two-colour contrasts

When you need exactly two categories, use blue vs orange, not red vs green:

- `#0072b2` / `#d55e00` — highest separation, works in every simulation
- `#000000` / `#d55e00` — when one series should read as the reference

## Sequential and diverging

- Sequential: vary **luminance monotonically**. Viridis, cividis, and any
  single-hue light-to-dark ramp are safe. Cividis is explicitly optimised for
  CVD.
- Diverging: use blue–white–orange or blue–white–brown. Never red–white–green.
  Check that the two ends differ in luminance as well as hue, so the map still
  reads in greyscale.

## Stop using

- **Jet / rainbow.** Non-monotonic luminance, invents banding that is not in the
  data, and collapses under CVD.
- **matplotlib `tab10` defaults for red/green pairs.** `#d62728` and `#2ca02c`
  simulate to nearly the same colour under deuteranopia (ΔE2000 = 5.0).
- **Red = bad / green = good** as the only signal, anywhere.
- **Traffic-light conditional formatting** in tables without an icon or value.

## Rule that outranks the palette

A CVD-safe palette does not make a chart accessible on its own. Redundant
encoding does. A deck using `tab10` with dashed-vs-solid lines and direct labels
is more accessible than one using Okabe–Ito with a colour-only legend.
