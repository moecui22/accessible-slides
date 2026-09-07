# Agent instructions

This repo holds one skill: **accessible-slides**.

Read `SKILL.md` for the operating procedure. It is short by design. The four
files in `references/` carry the detail and should be read only when the
relevant step needs them:

| File | Read when |
|---|---|
| `references/palettes.md` | picking or replacing colours |
| `references/fixes.md` | writing the fix for a specific failure |
| `references/checks.md` | you need a threshold's source or the size formula |
| `references/vision-loss.md` | explaining why something fails |

Two scripts do the measuring. Do not reimplement them and do not estimate
contrast or colour difference by eye:

- `scripts/audit.py` contrast, colour separability, text size. Standard library.
- `scripts/simulate_cvd.py` image simulation and comparison sheets. Needs
  `numpy` and `Pillow`.

Always ask for the viewing distance and screen height before answering a
text-size question. The answer is meaningless without them.
