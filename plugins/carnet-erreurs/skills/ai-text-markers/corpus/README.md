# corpus

**Measurements only.** `measurements.json` holds the readings taken on 7 real
LinkedIn posts, 17 Sep 2026.

🚨 **The posts themselves are not here, and will not be.** They were written by
real, identifiable people. Redistributing them would mean republishing someone
else's work without consent, and publishing personal data — and one of the seven
carries a `s` label meaning "suspected machine-written", which is an accusation
nobody agreed to have attached to their name.

⭐ **The measurements are enough.** Every figure in `references/` can be
reproduced by running `scripts/markers.py` on your own feed.

## Fields

| Field | Meaning |
| --- | --- |
| `etiquette` | `h` human / `s` suspect — ⚠️ a judgement, not a proof |
| `theme` | topic, no author |
| `irregularite` | σ/μ of sentence length in words |
| `details_100m` | numbers + proper nouns per 100 words |
| `registre_familier` | count of slang / informal markers found |
