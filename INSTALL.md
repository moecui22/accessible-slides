# Install

Pick your tool. Every route installs the same skill; nothing here is
Claude-specific.

## Fastest, any agent

```bash
npx skills add moecui22/accessible-slides
```

Works with any harness that reads the Agent Skills format.

## Claude Code

**As a plugin:**

```
/plugin marketplace add moecui22/accessible-slides
/plugin install accessible-slides@accessible-slides
```

**As a plain skill:**

```bash
git clone https://github.com/moecui22/accessible-slides.git
mkdir -p ~/.claude/skills
cp -R accessible-slides ~/.claude/skills/accessible-slides
```

Check it registered with `/plugin list` or by asking Claude to list its skills.

## Cursor

```bash
git clone https://github.com/moecui22/accessible-slides.git
mkdir -p .cursor/skills
cp -R accessible-slides .cursor/skills/accessible-slides
```

The repo also ships a ready-made copy under `.cursor/skills/`, so cloning into
your project puts it in the right place already.

## Any other agent

The skill is a Markdown file and two Python scripts. There is no runtime and no
framework. Either:

1. Copy `SKILL.md`, `references/` and `scripts/` into wherever your agent reads
   skills from, or
2. Point your agent at the raw file:
   `https://raw.githubusercontent.com/moecui22/accessible-slides/main/SKILL.md`

If your agent reads an `AGENTS.md`, the short version in this repo's
`AGENTS.md` can be pasted straight into yours.

## No agent at all

The scripts work on their own:

```bash
git clone https://github.com/moecui22/accessible-slides.git
cd accessible-slides
python3 scripts/audit.py --colors "#d62728,#2ca02c"
```

`audit.py` needs only Python 3. `simulate_cvd.py` also needs `numpy` and
`Pillow`:

```bash
pip install numpy Pillow
```

## Checking it works

```bash
python3 tests/test_audit.py
```

All checks should pass. They compare the contrast and colour maths against
published reference values.

## Trouble

**The skill does not trigger.** Say what you want in plain words: "check this
deck for accessibility", "will these colours work for colour blind readers".
Skills are matched on their description, so naming the file rarely helps.

**`simulate_cvd.py` fails on import.** Install `numpy` and `Pillow`.

**Text-size answers look wrong.** The skill needs the room. Tell it the screen
height and the distance to the back row, or it falls back to a 2 m screen at
15 m.
