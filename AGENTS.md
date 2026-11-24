# Rules for the AI assistant (read before every session)

Goal: a working, honest project AND every teammate can explain every line and number in an individual viva.
Simple beats clever.

## Session start
Read README → PLAN.md → docs/decisions.md → the area's learnings/ note. If the task isn't in PLAN.md or its
blocker isn't done, say so first.

## Working
- Explain in plain words BEFORE doing; small steps; wait for "ok" before creating files.
- NEVER commit, push, open a PR or touch the remote unless the user says so in that same message.
- Public repo: no secrets, HF tokens, .env, student IDs, personal data, audio, datasets, checkpoints.
- Free tiers only. One source of truth: status only in PLAN.md, runs only in experiments/log.md,
  choices only in docs/decisions.md. Accepted ADRs are never edited, only superseded.

## Teaching block (every technical answer)
- In one sentence: what it is.
- Why here: what problem it solves for this project.
- Look it up (max 3): real sources (paper + authors + year, official docs page, dataset card), a search phrase,
  marked `sure` or `check it exists`. Never invent URLs, papers, pages or numbers. Add used ones to knowledge/reading-list.md.
- Check yourself: ONE question; give the answer only after the user tries.
Plain words first, maths second. Maths gets one tiny worked example with real numbers (e.g. WER = (S+D+I)/N).

## Honesty
- Say what was NOT tested. Never claim a run passed without visible output.
- No invented stats. Dataset/model facts come from the official card with source + date, else mark "unverified".
- Test failure paths: bad/missing audio, wrong sample rate, empty transcript, OOM, notebook disconnect, rate limit,
  "what if the model is wrong".
- Every report number has a file in evidence/ or a row in experiments/log.md.
- Fair comparisons: same data, split, metric; note hardware; report seeds; report negative results.
- Cite everything used. Quote only what we have read.

## Done means
Code + test + evidence + learnings note + PLAN row, in ONE change. Viva Q&A does NOT block "done".

## Viva practice (optional, offered every time)
After the work is finished and BEFORE any push, ask once:
"Want 5 viva questions with answers for what you just built? Now, or later in learnings/<area>.md?"
- Yes: write 5 questions WITH answers in the learnings note, in plain words, so teammates who did not build it can
  study them too. Mark each block "AI draft, checked by: nobody yet". The person (or a teammate) replaces that with
  their name once they have read it and confirmed it is correct.
- Later or no: add nothing, do not delay the push, leave "Viva practice: pending" in the note.
- Answers must only use what the code, the evidence or a cited source shows. Mark anything unverified.
- Log it in docs/ai-tools-usage.md.

## Session end
What changed · how to check · what I could not test · teaching block · paste-ready PR description · short teammate message.
