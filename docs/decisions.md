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
- ADR-3: how we compute WER (library or our own, text normalisation rules)
- ADR-4: demo tool

### ADR-2: AfriSpeech-200 subset
- Status: proposed
- Date: 2026-11-24
- Chose: For the first workflow check, propose one clinical Setswana clip from the `dev` split of `evie-8/afrispeech-200`. The reference transcript starts with “rickets in growing children.”
- Why: The audio plays in the viewer, and the reference transcript is visible.
- Gave up: One clip can check whether the workflow runs. It cannot tell us how well the model performs across clips or accents.
- Options considered (cost, risk): Try several clips first. That covers more examples but takes longer to run and inspect.
- Evaluation subset: Size, accents, split, and seed are still open for M0.
