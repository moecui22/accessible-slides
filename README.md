# Accessible Slides

**Checks your slides the way your audience will actually see them: colour
blind, in a bright room, from the back row.**

![A red and green line chart, shown four ways: normal vision, protanopia, deuteranopia, and greyscale](assets/hero_before.png)

Same slide, four ways of seeing it. In the bottom-left panel both lines are the
same colour and the legend is useless. That is roughly 1 in 12 men in your
audience.

Two changes fix it: colours that stay apart, and labels on the lines instead of
a legend.

![The fixed version in blue and orange, with dashed lines and direct labels](assets/hero_after.png)

---

## Who this is for

- Anyone giving a **conference talk** or **lecture** who has never checked what
  the back row sees
- **Poster presenters**, where the viewing distance problem is worst
- Anyone making **figures for a paper**, especially with default matplotlib or
  ggplot colours
- People who have to **sign off on decks** for accessibility at work or school

You do not need to know anything about vision science. The skill does that part.

## What it checks

**Colour.** Simulates how each colour looks to someone who is colour blind,
then measures whether two colours that mean different things still look
different. Red vs green almost never survives.

**Contrast.** Measures text against its background, using a stricter target for
projectors than for screens. Room light washes out blacks, so a slide always
arrives worse than it looked on your laptop.

**Text size.** Takes the size of the screen and the distance to the back row,
and tells you the smallest font that is actually readable from there. This is
where "use 30 point" comes from, except it is calculated rather than guessed.

Then it tells you what to change. Not just a score.

## Install

**Fastest:**

```bash
npx skills add moecui22/accessible-slides
```

**Claude Code plugin:**

```
/plugin marketplace add moecui22/accessible-slides
/plugin install accessible-slides@accessible-slides
```

**Manual:**

```bash
git clone https://github.com/moecui22/accessible-slides.git
mkdir -p ~/.claude/skills
cp -R accessible-slides ~/.claude/skills/accessible-slides
```

**Other agents:** point yours at `SKILL.md`. It is plain Markdown and two Python
scripts, nothing Claude-specific.

## How to use it

Just say what you want:

> Check my talk deck for accessibility. The back row is about 12 m from a 2 m screen.

> Will these figure colours work for colour blind readers? #d62728 #2ca02c #1f77b4

> Is the text on this poster big enough to read from 3 m?

> Fix the colours in this chart so they work in greyscale.

If you do not say how big the room is, it will ask. The text size answer means
nothing without it.

## Using the scripts on their own

No agent needed.

```bash
# Which of these colours become confusable?
python3 scripts/audit.py --colors "#d62728,#2ca02c,#0072b2,#d55e00"

# Is this text readable, and what should it be?
python3 scripts/audit.py --contrast "#8a8a8a" "#ffffff"

# How big does text need to be in this room?
python3 scripts/audit.py --room --distance 15 --screen-height 2.0 --font 24

# See a slide the way a colour blind viewer sees it
python3 scripts/simulate_cvd.py slide.png --sheet sheet.png
```

`audit.py` needs nothing but Python. `simulate_cvd.py` needs `numpy` and `Pillow`.

What it prints:

```
FAIL  #d62728 vs #2ca02c   normal 71.8 | protan 27.3 | deutan  5.0 | tritan 70.6
PASS  #0072b2 vs #d55e00   normal 49.6 | protan 55.2 | deutan 62.4 | tritan 78.4

Contrast #8a8a8a on #ffffff = 3.45:1
  projected, lit room (body)   need 7.0:1  FAIL
  nearest passing neutral      #595959 (7.00:1)

Your 24 pt text = 10.6 arcmin at the back row  [FAIL, need 41 pt]
```

## How this differs from other accessibility tools

| Tool | Made for | Does not cover |
|---|---|---|
| axe, WAVE, Lighthouse | websites and web apps | slides, posters, figures |
| Colour blindness simulators | showing you a picture | measuring it, or telling you the fix |
| PowerPoint's built-in checker | alt text and reading order | colour, contrast, or size for the room |
| **Accessible Slides** | slides, posters, figures | screen readers, alt text, reading order |

## What it does not do

Worth being clear, because an accessibility tool that overpromises is worse than
none:

- No screen reader checks, alt text, reading order or keyboard navigation. Those
  matter and other tools cover them well.
- The contrast formula it uses is the standard web one, which is known to be a
  poor fit for light text on dark backgrounds and for thin lines.
- Colour blindness comes in degrees. The simulation shows the strongest form, so
  treat it as a worst case rather than a prediction.
- The colour separation threshold is a design choice, not a law of nature.
- It cannot tell you whether the slide was worth showing.

## Relevant publications and further reading

The thresholds used here draw on the work below, which is also a good starting
point if you would like to read further. Links point to freely available pages
where possible, with DOIs listed for the paywalled ones.

- **Colour blindness simulation:** Brettel, Viénot & Mollon (1997),
  [*JOSA A* 14(10), 2647](https://opg.optica.org/josaa/abstract.cfm?uri=josaa-14-10-2647)
  (doi:10.1364/JOSAA.14.002647), and Viénot, Brettel & Mollon (1999),
  [*Color Research & Application* 24(4), 243](https://onlinelibrary.wiley.com/doi/10.1002/%28SICI%291520-6378%28199908%2924:4%3C243::AID-COL5%3E3.0.CO;2-3)
- **Colour difference (CIEDE2000):** Sharma, Wu & Dalal (2005),
  *Color Research & Application* 30(1), 21 (doi:10.1002/col.20070).
  [Author's page, with the reference implementation and test data](https://www.ece.rochester.edu/~gsharma/ciede2000/)
- **Readable text size:** Legge & Bigelow (2011),
  [*Journal of Vision* 11(5):8, free full text](https://jov.arvojournals.org/article.aspx?articleid=2191906)
  (doi:10.1167/11.5.8)
- **Colour palette:** Okabe & Ito,
  [Color Universal Design](https://jfly.uni-koeln.de/color/)
- **Contrast ratios:** [WCAG 2.2](https://www.w3.org/TR/WCAG22/)

## Citing this

If you use this in published work, please cite it. GitHub builds a citation from
`CITATION.cff` via the "Cite this repository" button in the sidebar.

## License

MIT
