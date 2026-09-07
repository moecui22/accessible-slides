# What each condition does, and who has it

## Colour-vision deficiency (CVD)

| Type | Missing / shifted | Prevalence (men) | Prevalence (women) | What breaks |
|---|---|---|---|---|
| Deuteranomaly / deuteranopia | M cone | ~6% | ~0.4% | red vs green, orange vs yellow-green |
| Protanomaly / protanopia | L cone | ~2% | ~0.03% | red vs green, plus red appears dark |
| Tritanopia | S cone | <0.01% | <0.01% | blue vs green, yellow vs pink |

Deutan and protan together account for essentially all of it. Design for those
two and tritan follows almost for free.

Protanopia has a second effect people forget: reds lose luminance as well as
hue. A red on black that looks fine to you can be near-invisible to a protanope,
because for them it is dark-on-dark, not just a different colour.

## Reduced contrast sensitivity

This is the one that matters for the largest number of people and gets the least
attention. Contrast sensitivity declines steadily from roughly the fourth decade
and the loss is largest at middle and high spatial frequencies - exactly the band
that carries letter shapes.

Contributing causes, all common: lens yellowing and light scatter (early
cataract), smaller pupil (senile miosis, reducing retinal illuminance), and
neural losses. The practical result is that an audience member of 65 may need
2–3× the contrast a 25-year-old needs for the same task.

Cataract and other media opacities add veiling glare, which raises the black
level across the whole field. Fine light-grey text on white is the first thing
to disappear.

## Acuity and the back of the room

Normal acuity (6/6, 20/20) resolves a 1 arcmin gap; the standard letter subtends
5 arcmin. But threshold is not reading. Maximum reading speed needs print well
above threshold - a critical print size of roughly 0.2° (12 arcmin) of x-height
for normally sighted readers, larger for older readers and much larger for
anyone with low vision.

Design target here is 16–20 arcmin of x-height at the back row. See
`checks.md` for the arithmetic.

## Environment, which is part of the visual system

- Projector contrast in a lit room is often below 20:1 sequential, and ambient
  light adds a constant to the black level. Authored ratios are an upper bound,
  never a delivered value.
- Blue-on-black and red-on-black suffer from chromatic aberration and, at low
  light levels, from the eye's poor sensitivity to short wavelengths.
- A viewer at 15 m with uncorrected 0.5 D of astigmatism is a normal audience
  member, not an edge case.
