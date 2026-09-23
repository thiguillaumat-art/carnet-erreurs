# Carnet d'erreurs

**Skills built from mistakes that actually shipped. Every one of them was
measured, not remembered.**

No preventive best practices, no rules invented because they sound right. Each
entry in this repo exists because something went out broken, someone counted
the damage, and the count is in the file.

[Install](#install) · [The skills](#the-skills) · [Why it's built this way](#why-its-built-this-way) · [Limits](#limits) · [Standard](STANDARD.md)

---

## The skills

| Skill | What it does | Born from |
| --- | --- | --- |
| [`render-check`](plugins/carnet-erreurs/skills/render-check) | Refuses to say "done" on visual work without rendering it and looking at it. Render bench, 16 things a typecheck never catches, WCAG contrast calculator with all three thresholds. | **7 visual defects on one 3-day project** — 260 px of text silently cut off, a 1.65:1 contrast posted five times, a font that dropped to 7.5 pt after a page break. |
| [`ai-text-markers`](plugins/carnet-erreurs/skills/ai-text-markers) | Counts measurable "AI-sounding" markers in a French text. Never returns a verdict on who wrote it. | **A failed hypothesis, kept in the repo.** Sentence irregularity was supposed to separate human from machine writing. Measured on 7 real posts, it separates nothing. |
| [`handover`](plugins/carnet-erreurs/skills/handover) | Carries a long conversation into a new one — different model, fresh context — without losing what matters **and without carrying mistakes forward**. Produces three lists: carry, carry with a caveat, **do not carry**. | **A measured failure of self-review.** On one real project the machine produced 19 errors and caught **7 of its own**. A human caught 12. A summary written by the one who did the work keeps its own conclusions and drops the corrections it was given. |

---

## Install

```
/plugin marketplace add thiguillaumat-art/carnet-erreurs
/plugin install carnet-erreurs@carnet-erreurs
```

That's it. All three skills become available; Claude triggers them on its own
from their descriptions.

The Python scripts run standalone too, no install and no dependencies,
Python ≥ 3.9:

```bash
python3 plugins/carnet-erreurs/skills/render-check/scripts/contrast.py "#5D6061" "#15181A"
#  #5D6061 on #15181A    2.81:1   not enough for any use
```

---

## Why it's built this way

**One repo, not one per skill.** The skills come from the same practice and
share the same standard. Splitting them would split their history too.

**Three rules the whole repo follows:**

1. ⭐ **A number is counted, never estimated.** Every figure in every file here
   has a source that can be re-measured. The ones that were written before
   being counted are marked as the mistakes they were.
2. ⭐ **A failed hypothesis stays in the repo.** `ai-text-markers` ships the
   table showing its own core assumption does not hold. That table is the most
   useful thing in it.
3. ⛔ **No tool returns a verdict it cannot back.** `ai-text-markers` refuses to
   output "87% AI" because a false positive accuses someone who has no way to
   disprove it.
4. ⬜ **A test that cannot fail is not a test.** An eval ships with its prompt,
   its fixture, its expected output written beforehand, and the result *without*
   the skill — otherwise it measures the model, not the skill.

The four conditions a change meets before it goes out, and the one that was
already broken on day one, are in [STANDARD.md](STANDARD.md).

**Written in French, named in English.** The skills read French text and were
written in French. The names, descriptions and file names are English, because
a skill's `description` is what triggers it — in French it never fires for
anyone else.

---

## Limits

⚠️ **`ai-text-markers` is French-only.** Its vocabulary lists and patterns would
need rebuilding for any other language.

⚠️ **`render-check` renders nothing by itself.** It tells you how to get a
render and what to look for. The looking is still yours.

⚠️ **Small samples.** 7 posts, one 3-day project. Every conclusion here is a
lead from real measurement, not a study.

⚠️ **No third-party content is redistributed.** The posts measured for
`ai-text-markers` were written by real, identifiable people. Only the
measurements ship — re-run the tool on your own feed to verify.

---

## License

MIT. See [LICENSE](LICENSE).
