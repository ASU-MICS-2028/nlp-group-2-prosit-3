# Decisions (short ADRs)

Accepted ADRs are never edited, only superseded by a new one. Status: proposed | accepted | superseded by ADR-N.

## Template
### ADR-N: title
- Status:
- Date:
- Chose:
- Why:
- Gave up:
- Options considered (cost, risk):

## Open decisions (filled by the M0 spike)
- ADR-1: pretrained model(s) feasible on free compute
- ADR-2: AfriSpeech-200 subset (size, accents, split, seed)
- ADR-3: how we compute WER (library or our own, text normalisation rules)
- ADR-4: demo tool

### ADR-3: how we compute WER
- Status: proposed (needs team agreement at the M0 spike; not accepted)
- Date: 2026-11-24
- Chose: our own WER code (`src/evaluation/wer.py`), word-level edit distance, corpus WER = total (S+D+I) / total N.
  Normalisation, applied the same way to reference and hypothesis: Unicode NFC, lower case, every character that is
  not a letter, digit, apostrophe or space becomes a space, then collapse spaces. Numbers are not converted to words.
- Why:
  - Every line can be explained in the viva (the evaluation owner can walk through the table by hand).
  - A test checks it against the `jiwer` library on 2,000 random pairs (0 differences, evidence/e1-wer-pytest.txt),
    so we get a library's correctness without hiding the method.
  - Corpus WER (not the mean of clip WERs) so short clips do not dominate.
  - Small normalisation only, so a capital letter or a full stop is not counted as an error, but real errors are kept.
- Gave up:
  - Number and spelling rules (e.g. Whisper's English text normaliser maps "500" and "five hundred" together). Without
    them, a model that writes numbers as words is penalised. Revisit after M2 shows what the chosen model outputs.
  - Character error rate (CER). Could be added later for drug-name analysis (C1).
- Options considered (cost, risk):
  - jiwer only: free, tested, little code. Risk: harder to explain what it does inside; its default transforms change between versions.
  - Hugging Face `evaluate` "wer" metric: free; it uses jiwer underneath (check it exists in its docs). Same risk, more dependencies.
  - Our own code (chosen): free, about 100 lines. Risk: bugs, reduced by hand-worked tests and the jiwer cross-check.

