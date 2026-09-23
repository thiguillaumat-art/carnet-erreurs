# render-check

**A Claude skill that refuses to say "done" on visual work without rendering it
and looking at it.**

Ships a render bench (view a PDF, an email, a component, a mobile page — with
no browser), a list of what a typecheck never catches, and a WCAG contrast
calculator that knows all three thresholds.

[Why](#why) · [Install](#install) · [What it catches](#what-it-catches) ·
[Contrast tool](#contrast-tool) · [Limits](#limits)

---

## Why

A typecheck proves the code runs. **It proves nothing about what a person
sees.**

Measured on a single three-day project, all seven found by looking, none by
reading code:

| Defect | Measurement |
| --- | --- |
| Text silently cut off on mobile | **260 px** hidden — `max-height` animation on unknown-length content |
| Invisible button | text colour equal to its own background |
| Unreadable secondary text | **1.65:1** contrast, posted 5 times — threshold is 4.5 |
| Font silently reset | dropped to **7.5 pt** after a PDF page break |
| Bullet printed at wrong size | one of four, twice too small |
| SVG text in the wrong family | fell back to serif |
| A whole page section | missing |

⭐ **The fifth one was in the banner of a post that was about that exact
mistake.** That is the case for an automated check.

---

## Install

Ships in the [carnet-erreurs](../../../../) plugin:

```
/plugin marketplace add thiguillaumat-art/carnet-erreurs
/plugin install carnet-erreurs@carnet-erreurs
```

The contrast tool runs standalone, no install, Python ≥ 3.9:

```bash
python3 scripts/contrast.py "#5D6061" "#15181A"
#  #5D6061 on #15181A    2.81:1   not enough for any use
```

---

## What it catches

`references/what-a-typecheck-misses.md` — **16 entries, each one born
from a real incident.** No preventive rules.

| Category | Example |
| --- | --- |
| Silent clipping | `max-height` animating content of unknown length — a bet on character count |
| Global state | font and letter-spacing survive a page break in a PDF; `setCharSpace` persists until reset |
| Collapsed flex child | a separator with no content collapses to zero width |
| CSS specificity | `.gabarit-article p` (0,0,1,1) beats `.text-sm` (0,0,1,0) |
| Colour hunting | searching a hue in hex only misses `rgb()` and array notations |
| Data writes | `ws.cell(row, col, value=None)` does **not** clear a cell in openpyxl |

---

## Contrast tool

Three thresholds, and the third is the forgotten one:

```
4.5:1   body text
3.0:1   large text (≥ 24 px, or ≥ 18.7 px bold)
3.0:1   THE OUTLINE OF AN INTERACTIVE COMPONENT (WCAG 1.4.11)
```

⭐ **The rule that avoids half the mistakes:** compute a text colour against the
**darkest surface it will sit on**, not against the page background. A grey at
4.55 on the background falls to 3.96 the moment it lands on a tinted card.

---

## Measured against no skill at all

3 evals, run with and without the skill on the fixtures shipped in
[`evals/fixtures/`](evals/fixtures). Full write-up: [`evals/RESULTS.md`](evals/RESULTS.md).

| | With skill | Without |
| --- | --- | --- |
| Expectations met | **15/15** | 12/15 |

⚠️ **One run per configuration.** A signal, not a measurement.

⭐ **And one eval gained nothing** — the PDF overflow was caught either way.
That row is kept in the table on purpose: it marks where this skill is not
needed.

---

## Limits

⚠️ **This skill does not render anything by itself.** It tells you how to get a
render out of a PDF, an email or a component, and what to look for. The looking
is still yours.

⚠️ **The contrast tool covers colour only.** It says nothing about font size,
hit-target size, focus order or motion.

⛔ **A passing contrast ratio is not an accessibility audit.**

---

## License

MIT. See [LICENSE](../../../../LICENSE) at the repository root.
