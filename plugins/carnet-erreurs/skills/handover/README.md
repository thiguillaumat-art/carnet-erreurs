# handover

**Carries a long conversation into a new one without carrying its mistakes
forward.**

Not a summary. A sort, in two passes, where the second pass does not trust the
first. Output: three lists — carry, carry with a caveat, **do not carry**.

[Why](#why) · [Install](#install) · [How it runs](#how-it-runs) ·
[Real output](#real-output-of-extractpy) · [Limits](#limits)

---

## Why

Measured on one real project:

| | Errors |
| --- | --- |
| Produced by the machine | **19** |
| Caught by the machine, on its own work | **7** |
| Caught by a human | **12** |

**7 out of 19 — 37 %.**

A summary is written by whoever did the work. So it keeps that worker's
conclusions and drops the corrections it was forced to accept. The error goes
into the next conversation intact, stripped of the thing that disproved it.

⭐ **That is why this skill is run by the conversation that starts, not the one
that ends.** A different session reads the old transcript: work it did not
produce, no conclusion to defend.

---

## Install

Ships in the [carnet-erreurs](../../../../) plugin:

```
/plugin marketplace add thiguillaumat-art/carnet-erreurs
/plugin install carnet-erreurs@carnet-erreurs
```

The extraction script runs standalone, no dependencies. Tested on Python 3.10:

```bash
python3 scripts/extract.py transcript.txt > candidates.md
cat transcript.txt | python3 scripts/extract.py -
```

---

## How it runs

| | Step | Rule |
| --- | --- | --- |
| 0 | **Find the transcript** | A session-reading tool, or a manual export to a file. ⛔ Never rebuilt from the files the old session wrote — that is its own output, suspect by construction |
| 1 | `extract.py` | Mechanical. Flags what deserves a look. Decides nothing |
| 2 | Verify every candidate **against the transcript**, not against `candidates.md` | Four questions: is it really there · fact or assistant's conclusion · contradicted later · **who decided** |
| 3 | Write `PASSATION.md` | ✅ carry · ⚠️ carry with a caveat · ⛔ do not carry |

⛔ **A decision the assistant made on the user's behalf is never carried.** It
resurfaces weeks later, when nobody remembers who made it.

⚠️ **Check the tool, not its name.** In the first real run, a tool called
`list_sessions` answered — it belonged to a sandbox provider and listed
machines, not conversations.

> 🚨 **No transcript, no handover.** Say so and stop.

---

## Real output of `extract.py`

On [`evals/fixtures/extrait-transcription.txt`](evals/fixtures/extrait-transcription.txt),
a 9-line sample written for the test. Unedited:

```markdown
# Candidats de passation — evals/fixtures/extrait-transcription.txt

⛔ **Ceci n'est PAS une passation.** C'est la liste de ce qui doit être examiné. La passe 2 vérifie chaque ligne contre la transcription et tranche.

## 🚨 À NE PAS transmettre tel quel — 4

⭐ **La section la plus importante.** Une passation qui ne transmet que le bon reconduit les erreurs en silence — elles repartent sans leur correction.

- `L2` **correction d'une erreur passée — ⛔ vérifier que c'est la version CORRIGÉE qui part**  
  > assistant: J'avais écrit « domaine retenu : la fiscalité » dans ENGAGEMENTS.md. C'est faux, tu ne l'as jamais choisi.
- `L5` **⚠️ limite déclarée — ⭐ elle DOIT être transmise, c'est ce qui se perd en premier**  
  > assistant: ⚠️ Je n'ai pas pu vérifier le rendu après correction — pas de node_modules.
- `L6` **⚠️ une supposition — ne jamais la transmettre comme un fait**  
  > assistant: L'article vient probablement d'une source sponsorisée, à confirmer.
- `L8` **🚨 un secret possible — ⛔ ne JAMAIS transmettre**  
  > assistant: La clé API est dans le fichier de configuration.

## ⭐ Les mots de l'utilisateur — 3

⛔ **Ne jamais reformuler.** C'est la seule matière qu'un résumé ne peut pas remplacer sans la trahir.

- `L1` ok et donc prochaine étape ?
- `L3` ce n'est pas moi qui ai choisi le domaine, c'est exactement toi qui a choisi sans même me demander une fois
- `L9` je veux vraiment faire le choix le plus éclairé de ma vie

## Chiffres et mesures — 1

⚠️ Chacun doit repartir **avec sa source**. Un chiffre sans source devient une affirmation au tour suivant.

- `L4` assistant: Le contraste mesuré est de 1,26:1 contre un seuil de 3:1, vérifié avec scripts/contrast.py.

## Lignes marquées — 1

- `L5` assistant: ⚠️ Je n'ai pas pu vérifier le rendu après correction — pas de node_modules.

## Fichiers écrits — 2

⭐ Ce qui est dans un fichier n'a pas besoin d'être transmis : il suffit de dire où regarder.

- `/contrast.py`
- `~/dev/engagements/OFFRE-diagnostic.md`

## Liens — 1

- https://github.com/exemple/depot
```

### What that output gets wrong — read off it, not guessed

| Line | Defect |
| --- | --- |
| `L2` | Matches **three** trap patterns — past correction, contradicted claim, decision. **Only the first is reported**: one trap per line. The "who decided?" flag, the most important one, is hidden behind it |
| `L6` | Same masking: "probablement" is reported, "à confirmer" is matched but hidden. And "sponsorisée" is **not matched at all** — the pattern only knows "sponsorisé" |
| Files | `scripts/contrast.py` comes out as **`/contrast.py`**: a relative path loses its first segment. `ENGAGEMENTS.md` (no directory) is not caught at all |

⭐ Kept in the README on purpose. A pass that misses a candidate is exactly
what pass 2 exists to catch — which is why pass 2 reads the transcript, never
this list.

---

## Measured against no skill at all

**Not yet.** There is no with/without comparison. See
[`evals/RESULTS.md`](evals/RESULTS.md).

The one real run so far (23 Sep 2026): the session had no transcript, **refused
to build a handover from the old session's files**, and stopped. While reading
those files it found two contradictions in the project's source of truth that
the author had missed. The handover itself failed; the refusal is what the
skill is for.

---

## Limits

🚨 **The two passes have never run on a real transcript.** The core of the
skill is untested.

⚠️ `extract.py` has only been run on the 9-line fixture above, which was
written for the test.

⚠️ **n = 1.** One run, one model, one environment. No with/without comparison,
so what the skill *adds* is unknown — only what it *prevented* once.

⛔ **French only.** The trap patterns (`j'avais écrit`, `probablement`,
`non vérifié`…) and the output labels are French. An English transcript
yields user turns, numbers, paths and links, and almost no traps: on a 2-line English test, only "API key" was flagged — "I had written", "that was wrong" and "probably" were not.

⚠️ **User turns are detected by a line prefix** (`user:`, `utilisateur:`,
`human:`…). A transcript in another shape needs converting first.

⚠️ **No session-reading tool is assumed.** Where none exists, export the
transcript to a file by hand. That is a normal path, not a fallback.

---

## License

MIT. See [LICENSE](../../../../LICENSE).
