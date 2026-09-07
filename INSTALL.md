# Install

Pick your tool. Every route installs the same skill; nothing here is
Claude-specific.

## Fastest, any agent

```bash
npx skills add moecui22/accessible-slides
```

Works with any harness that reads the Agent Skills format.

This form clones the whole repository into the skill directory: about 2 MB, and
it carries the demo assets, the tests and the two packaging copies along with
it. To install only the skill — `SKILL.md`, `references/` and `scripts/`, 36 KB
— point at it directly:

```bash
npx skills add https://github.com/moecui22/accessible-slides/tree/main/plugins/accessible-slides/skills/accessible-slides
```

## Claude Code

**As a plugin:**

```
/plugin marketplace add moecui22/accessible-slides
/plugin install accessible-slides@accessible-slides
```

**As a plain skill:**

```bash
git clone https://github.com/moecui22/accessible-slides.git
mkdir -p ~/.claude/skills/accessible-slides
cp -R accessible-slides/{SKILL.md,references,scripts} ~/.claude/skills/accessible-slides/
```

Copy those three paths, not the whole repo. The repo also carries assets, tests
and two packaging copies of the skill; putting all of that in `~/.claude/skills`
adds about 3 MB and leaves duplicate `SKILL.md` files nested inside the skill
directory, which can register as extra skills.

Check it registered with `/plugin list` or by asking Claude to list its skills.

## Cursor

```bash
git clone https://github.com/moecui22/accessible-slides.git
mkdir -p .cursor/skills/accessible-slides
cp -R accessible-slides/{SKILL.md,references,scripts} .cursor/skills/accessible-slides/
```

The repo also ships a ready-made copy under `.cursor/skills/`, so cloning it
into your project puts the skill in the right place already.

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
