# Learnings: evaluation

Owner: Opei   Backup: Nana

## What was done
- **E1:** our own word error rate (WER) code in `src/evaluation/wer.py`, with 17 hand-checked tests in
  `tests/test_wer.py` and one cross-check against the `jiwer` library in `tests/test_wer_vs_jiwer.py`.
- It reads a CSV (`id, reference, hypothesis`, plus any extra columns such as `accent` or `domain`) and prints
  corpus WER overall and per group. The per-group view is what C1 (per-accent, clinical vs general) will use.
- It runs on a made-up CSV (`tests/fixtures/fake_transcripts.csv`) so it does not wait for D1 (data) or M2 (model).
- Text rules (normalisation) are a proposal in ADR-3 in `docs/decisions.md`; the team still has to accept them.

## How to check it
```
pip install pytest            # jiwer is optional: pip install jiwer to run the cross-check
pytest -v                     # expect 18 passed (17 + 1 skipped if jiwer is missing)
python -m evaluation.wer tests/fixtures/fake_transcripts.csv --by accent   # needs PYTHONPATH=src
```
Saved output: `evidence/e1-wer-pytest.txt`.

## How the code works (in plain words)
1. **Normalise both texts:** same Unicode form (NFC), lower case, punctuation becomes a space, keep apostrophes.
   So `"The patient has fever."` and `"the patient, has fever"` count as identical.
2. **Split into words.**
3. **Fill an edit-distance table** (Levenshtein): cell `[i][j]` is the fewest edits that turn the first `i`
   reference words into the first `j` hypothesis words. Each cell takes the cheapest of three moves:
   diagonal (match costs 0, substitution 1), up (deletion 1), left (insertion 1).
4. **Walk back** from the bottom-right cell to see which moves were used, and count S, D, I.
5. **WER = (S + D + I) / N**, with N the number of reference words.
6. **Corpus WER** adds all errors and all N over every clip, then divides once.

Tiny table, reference `has fever`, hypothesis `had a fever`:

|        | (start) | had | a | fever |
|---|---|---|---|---|
| (start)| 0 | 1 | 2 | 3 |
| has    | 1 | 1 | 2 | 3 |
| fever  | 2 | 2 | 2 | **2** |

Bottom-right is 2 edits: `has`→`had` (S) and `a` (I). WER = 2 / 2 = 1.0.

## Glossary (every technical term in one line)
- WER: (substitutions + deletions + insertions) / reference words; lower is better; can be above 1.
- Reference: the human (correct) transcript. Hypothesis: what the model wrote.
- Substitution: a reference word replaced by a different word.
- Deletion: a reference word the model left out.
- Insertion: an extra word the model added.
- Edit distance (Levenshtein distance): fewest single edits to turn one sequence into another.
- Dynamic programming: solving a big problem by filling a table of small sub-problems.
- Normalisation: cleaning both texts the same way (case, punctuation) so we only count real word errors.
- Corpus WER (micro-average): total errors / total reference words over all clips.
- Mean per-clip WER (macro-average): average of each clip's WER; we do NOT report this as the main number.

## Viva questions (5, with answers written by the owner)
(Draft answers below so the shape is clear. Kobina: rewrite each in your own words before the viva.)
1. Q: Compute WER for reference `take two tablets daily` vs hypothesis `take tablets daily now`.
   A: "two" is missing (D = 1), "now" is extra (I = 1), no substitutions, N = 4. WER = (0 + 1 + 1) / 4 = 0.5.
2. Q: Why can WER be above 100%?
   A: N counts only reference words, but insertions have no limit. `yes` vs `no no no no` is 1 S + 3 I over N = 1, so WER = 4.0.
3. Q: Why do you add up errors over all clips instead of averaging each clip's WER?
   A: Averaging lets a 1-word clip weigh as much as a 9-word clip. One wrong word in a 1-word clip (WER 1.0) plus a
   perfect 9-word clip (WER 0.0) averages to 0.5, but only 1 of 10 words was wrong, so corpus WER is 0.1.
4. Q: Why normalise text before scoring, and what is the risk?
   A: Without it, a capital letter or a full stop counts as a whole wrong word, which is not a real error.
   The risk is hiding real errors, so we keep rules small and the same for every model. We do not turn numbers into
   words, so `500` vs `five hundred` still counts as 2 errors.
5. Q: Why is a low WER not enough to trust the system in a hospital?
   A: WER weighs every word the same. Getting `the` wrong and getting a drug name or dose wrong both cost 1 word, but
   only the second can harm a patient. So we also look at error examples on clinical words, and recommend that a
   doctor reviews every note.

## What is NOT tested yet
- No real AfriSpeech transcripts and no real model output (waits on D1 and M2).
- Number rules (`500` vs `five hundred`), British/American spelling, and hyphenated words are not handled.
- Speed on long files: the table is reference length x hypothesis length; fine for clips, not checked for hour-long audio.

## Sources used
- Levenshtein, V. I. (1966). Binary codes capable of correcting deletions, insertions, and reversals.
  *Soviet Physics Doklady, 10*(8), 707-710. (`sure` it exists; not opened by us)
- jiwer, a Python WER library (PyPI: `jiwer`), version 4.0.0, used only as a second opinion in a test. (`verified` installed and run 2026-11-24)
