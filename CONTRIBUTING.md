# Contributing

- One branch per task (named after the PLAN ID, e.g. `e1-wer`). One PR per branch. No stacked PRs.
- Plain code, short functions, type hints. Any logic gets a pytest.
- If a task's blocker isn't done, work against a fake or fallback input and say so in the PR.
- Update the learnings note and the PLAN row in the SAME PR.
- Never commit secrets, tokens, `.env`, audio, datasets or checkpoints. Link or script them instead.
- Raw outputs and screenshots for every reported number go in `evidence/`; every run gets a row in `experiments/log.md`.
