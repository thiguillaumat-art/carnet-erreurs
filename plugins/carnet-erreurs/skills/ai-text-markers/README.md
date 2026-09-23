# ai-text-markers

**Counts measurable "AI-sounding" markers in a French text. Never returns a
verdict on who wrote it.**

⭐ Not called `ai-detector`, because it detects nothing — see
[Why no verdict](#why-no-verdict).

Sentence irregularity, one-sentence paragraphs, tricolons, antithesis,
aphoristic endings, over-produced vocabulary, density of verifiable detail —
and it points at the sentences carrying them.

[Why no verdict](#why-no-verdict) · [Install](#install) ·
[What the survey found](#what-the-survey-found) · [Readings](#readings) ·
[Limits](#limits)

---

## Why no verdict

**No detector can tell you who wrote a text.** Commercial ones return
"94% AI-generated" on human writing. A false positive accuses someone with no
way to disprove it.

⭐ So this one counts and points. *"Your paragraph 4 is an antithesis, like
paragraphs 2 and 7"* is actionable. *"87% AI"* is not.

---

## Install

```
/plugin marketplace add thiguillaumat-art/carnet-erreurs
/plugin install carnet-erreurs@carnet-erreurs
```

The script runs standalone too, no dependencies, Python ≥ 3.9:

```bash
python3 scripts/markers.py draft.txt
python3 scripts/markers.py "corpus/*.txt" draft.txt   # compare
cat draft.txt | python3 scripts/markers.py -
```

---

## What the survey found

**7 real LinkedIn posts, measured 17 Sep 2026.** Raw measurements in
[`corpus/measurements.json`](corpus/measurements.json).

🚨 **The hypothesis failed.** Sentence irregularity was supposed to separate
human from machine writing. It does not:

| | irregularity (σ/μ) | verifiable details / 100 words |
| --- | --- | --- |
| labelled human | 0.84 · 0.57 · 0.50 | 10.1 · 5.7 · 3.6 |
| labelled suspect | 0.48 · 0.74 · 0.86 · 1.15 | 3.8 · 9.1 · 8.9 · 5.3 |

Full overlap. Detail density does not separate either.

⭐ **And the explanation matters more than the table: on LinkedIn, the "AI
style" IS the LinkedIn style.** One-sentence paragraphs (76–100% of paragraphs,
everywhere), tricolons, antithesis, aphoristic closers — all present in posts
written by humans. The models trained on that corpus and return its average.

**A high score means "written in the register the machine imitates", not
"written by a machine".**

One marker did separate: **register drop** — slang, a swear word, a sentence
left badly formed. It appears in exactly one post, the unmistakably human one.
⚠️ n = 7, so treat it as a lead, not a proof.

---

## Readings

| Reading | Threshold used | Caveat |
| --- | --- | --- |
| `irrégularité` σ/μ of sentence length | < 0.45 = very even | ⚠️ does **not** discriminate |
| `détails /100 mots` numbers + proper nouns | < 8 = poorly anchored | ⚠️ does **not** discriminate |
| `tricolons`, `antithèses`, `chute aphoristique` | any occurrence | style, not authorship |
| `registre familier` | any occurrence | ✅ the only one that separated |
| `lexique sur-produit` | any occurrence | worth rewriting regardless |

### Fixing a text that reads as machine-written

⛔ Do **not** remove the figures — LinkedIn rewards them, and removing them
makes the text flat without making it human.

✅ Add what a model cannot produce without risking a falsehood:

1. **Circumstance** — where, when, on whose screen, what you were doing.
2. **A register drop** — one sentence you would say out loud, not write.
3. **Asymmetry** — develop one point at length, dispatch the next in a line.

🚨 **Never invent the circumstance to make a text sound human.** That trades a
style problem for a truthfulness problem, which is far worse.

---

## Limits

⛔ **French only.** The vocabulary lists, the antithesis pattern and the
register-drop list are French. Everything else would need rebuilding per
language.

⚠️ **n = 7.** One feed, one day, one country. Every conclusion here is a lead.

⚠️ **The original posts are not redistributed.** They were written by real,
identifiable people. Only the measurements ship, in `corpus/measurements.json` —
re-run the tool on your own feed to verify.

---

## License

MIT. See [LICENSE](../../../../LICENSE) at the repository root.
