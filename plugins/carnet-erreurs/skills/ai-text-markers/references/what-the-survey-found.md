# What the feed survey produced — 17 Sep 2026

7 posts read directly from a real LinkedIn feed and measured with
`scripts/markers.py`. Label `h` = human on internal evidence (typos,
register, unverifiable personal detail), `s` = suspect.

⚠️ **These labels are judgements, not proofs.** They are a comparison point,
not a ground truth.

🚨 **No author is named and no post is reproduced.** The posts were written by
real, identifiable people who did not agree to have a machine-written suspicion
attached to their name. Raw readings live in `corpus/measurements.json`.

---

| Post | irregularity | details / 100 w | tricolons | register drop |
| --- | --- | --- | --- | --- |
| `h` competitive-exam prep | 0.84 | **10.1** | 1 | ✅ |
| `h` end-of-internship | 0.57 | 5.7 | 0 | — |
| `h` company retrospective | 0.50 | 3.6 | 0 | — |
| `s` brand history | 0.48 | 3.8 | 1 | — |
| `s` outbound tool A | 0.74 | 9.1 | 1 | — |
| `s` scaling advice | 0.86 | 8.9 | 2 | — |
| `s` outbound tool B | 1.15 | 5.3 | 3 | — |

---

## 🚨 The hypothesis failed

I expected **sentence irregularity** to separate human from machine writing —
the idea being that a model writes too evenly.

**It separates nothing.** Human: 0.84 · 0.57 · 0.50. Suspect: 0.48 · 0.74 ·
0.86 · 1.15. The ranges overlap completely. Detail density does no better:
10.1 · 5.7 · 3.6 against 3.8 · 9.1 · 8.9 · 5.3.

**One marker separated**: the **register drop** — slang, a swear word, a
sentence left badly formed. It appears only in the post that is unmistakably
human, and in none of the others.

⚠️ **n = 7.** A lead, not a demonstration.

---

## ⭐ And the explanation is worth more than the table

**On LinkedIn, the "AI style" is simply the LinkedIn style.**

Every figure attributed to models is there, written by humans:

- the one-sentence paragraph: **76 to 100%** of paragraphs, in every post;
- the tricolon — three parallel clauses, found in a media brand's post written
  by a professional copywriter;
- the antithesis *"it's not X, it's Y"*;
- the aphoristic closer.

Models trained on this corpus. **They do not produce a strange style: they
produce the average of that one.** Hence the sense of having read it before.

🚨 **Consequence: a detector returning a verdict would falsely accuse
professional writers.** That is why `markers.py` returns none.

---

## What actually distinguishes — three things, none automatable

1. **The register drop.** A swear word, an informality, a badly formed sentence
   kept as is. The only marker that separated here.
2. **Circumstance.** Where, when, with whom, what you were doing. The most
   human post in the set carried a first-person admission of failure and an
   exact, checkable date from a public calendar. ⭐ **A model cannot invent that
   without risking a falsehood** — which is exactly why it is the best signal.
3. **Asymmetry.** One point developed over ten lines, the next dispatched in
   one. Nobody distributes their interest evenly.

---

## 🎯 Reading this against your own draft

Measure it. If details per 100 words sit far below **10**, and there is no
register drop anywhere, the text will read as machine-written — whoever wrote
it.

⛔ **The fix is never to invent a scene.** That trades a style problem for a
truthfulness problem.
