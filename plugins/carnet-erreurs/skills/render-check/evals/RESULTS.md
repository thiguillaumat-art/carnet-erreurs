# Eval results

**Run 2026-09-14.** 3 evals, each run with and without the skill, on the three
fixtures in [`fixtures/`](fixtures). Every fixture in this folder is the real
input the eval was run on — re-run them yourself.

| Eval | Fixture | With skill | Without |
| --- | --- | --- | --- |
| `contraste-sur-fond-sombre` | `palette.css` | **5/5** | 3/5 |
| `accordeon-qui-coupe-sur-mobile` | `accordeon.html` | **5/5** | 4/5 |
| `titre-pdf-qui-deborde` | `rapport.py` | **5/5** | **5/5** |
| **Total** | | **15/15** | 12/15 |

---

## ⚠️ What these numbers do not say

**`runs_per_configuration = 1`.** One run each. Three passes gained out of
fifteen is a signal, not a measurement — a second run could move it.

**Eval 2 shows no gain at all.** Without the skill, the PDF overflow was caught
just as well. ⭐ That row stays in the table: an eval where the skill changes
nothing is the most useful one, because it says where the skill is not needed.

**Where the gain actually came from.** In eval 0, the run without the skill
judged contrast by eye and missed two ratios. The run with it measured them and
additionally reported a defect nobody asked about — a 1.33:1 interactive
outline (WCAG 1.4.11). ⭐ **That is the skill's real function: finding the
defect that was not the question.**

---

## Re-running them

The evals are declarative — `evals.json` holds the prompt, the fixture and the
expected output for each. Run them with the eval runner of your harness, or
read each prompt and check the expectations by hand.

⛔ **A pass rate produced without the fixtures present is meaningless.** They
ship here for that reason.
