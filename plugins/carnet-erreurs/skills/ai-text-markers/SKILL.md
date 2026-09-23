---
name: ai-text-markers
description: Count measurable "AI-sounding" markers in a French text before publishing it — sentence irregularity, one-sentence paragraphs, tricolons, antithesis, aphoristic endings, over-produced vocabulary, density of verifiable detail. Use when reviewing a LinkedIn post, a newsletter, or any short text that must not read as machine-written. Never returns a verdict on authorship.
---

# ai-text-markers — a marker counter, not a verdict machine

⭐ **The name is the promise.** It is not called `ai-detector`, because it
detects nothing. It counts markers and points at the sentences carrying them.

## 🚨 Read this before anything else

**This skill never says who wrote a text, and never outputs a probability.**

No detector can. Commercial ones return "94% AI-generated" on human writing;
a false positive accuses someone with no way to disprove it. This tool counts
markers and points at the sentences carrying them. That is all it does.

Its real use is **self-review**: "your paragraph 4 is an antithesis, like
paragraphs 2 and 7" is actionable. "87% AI" is not.

## Run it

```bash
python3 scripts/markers.py draft.txt
python3 scripts/markers.py "corpus/*.txt" draft.txt   # compare
cat draft.txt | python3 scripts/markers.py -
```

## What the survey found — read `references/what-the-survey-found.md`

7 real LinkedIn posts measured. **The hypothesis failed**: sentence
irregularity does not separate human from machine writing (humans 0.50–0.84,
suspects 0.48–1.15 — full overlap). Neither does detail density.

⭐ **The explanation matters more than the table: on LinkedIn, the "AI style"
IS the LinkedIn style.** One-sentence paragraphs, tricolons, antithesis,
aphoristic endings — all present in posts written by humans. The models learned
on that corpus and return its average. A high score means "written in the
register the machine imitates", not "written by a machine".

**One marker did separate**: register drop — slang, a swear word, a sentence
left badly formed. n = 7, so treat it as a lead, not a proof.

## What the counts mean

| Reading | Threshold used | Caveat |
| --- | --- | --- |
| `irrégularité` σ/μ of sentence length | < 0.45 = very even | ⚠️ does NOT discriminate |
| `détails /100 mots` numbers + proper nouns | < 8 = poorly anchored | ⚠️ does NOT discriminate |
| `tricolons`, `antithèses`, `chute aphoristique` | any occurrence | style markers, not authorship |
| `registre familier` | any occurrence | ✅ the only one that separated |
| `lexique sur-produit` | any occurrence | worth rewriting regardless |

## Fixing a text that reads as machine-written

⛔ Do not remove the figures — LinkedIn rewards them and removing them makes the
text flat without making it human.

✅ Add what a model cannot produce without risking a falsehood:

1. **Circumstance** — where, when, on whose screen, what you were doing.
2. **A register drop** — one sentence you would say out loud, not write.
3. **Asymmetry** — develop one point at length, dispatch the next in a line.

🚨 **Never invent the circumstance to make the text sound human.** That trades a
style problem for a truthfulness problem, which is far worse. If the author
cannot supply the detail, publish the text anchor-less rather than furnished
with a scene that did not happen.
