# PLAN (the ONLY place for tasks, owners, blockers and status)

Status values: todo | doing | blocked | done. Stage: day 0 (repo setup). Target date: TBD. The team confirmed the roles below.

## Roles (owner / backup)
| Area | Owner | Backup |
|---|---|---|
| Data | Elise | Perfect |
| Models | Perfect | Elise |
| Evaluation | Opei | Nana |
| Demo + deployment | Nana | Opei |
| Integrator (checks every report claim vs evidence) | Nana (Elise checks Nana's own numbers) | |
| Final repo check sign-off | Elise | |

Rotation rule: everyone runs the whole pipeline once on 10 clips and writes one Section B paragraph about a stage they don't own.

## Must
| ID | Task | Owner | Blocked-by | Done-when | Status |
|---|---|---|---|---|---|
| M0 | Decision spike (2 h max): model, subset, WER method, demo tool | all | none | 4 ADRs in docs/decisions.md | doing |
| M1 | Report answers Q1-Q3 with citations | Q1 Perfect, Q2 Opei, Q3 Elise | none (write skeleton day 1) | outline slots filled, every claim cited | todo |
| D1 | Subset loader + manifest script (no audio committed) | Elise | M0 | script reproduces the subset from a seed | todo |
| E1 | WER function + pytest, works on a fake CSV | Opei | none | tests pass on the worked example in knowledge/understanding.md | todo |
| M2 | One real AfriSpeech clip transcribed, WER measured | Perfect | M0, D1 (fallback: any public sample clip) | row in experiments/log.md + file in evidence/ | todo |
| M3 | Small demo (audio in, text out) | Nana | M2 (fallback: stub model) | demo runs; bad-audio and empty-transcript cases handled | todo |
| M4 | Q4 section: can we build it | Nana | M2, M3 | written with evidence links | todo |

## Should
| ID | Task | Owner | Blocked-by | Done-when | Status |
|---|---|---|---|---|---|
| S1 | Small RNN/CTC baseline vs pretrained transformer, SAME subset, split, metric | Perfect + Opei | D1, M2, E1 | both rows in experiments/log.md, hardware and seed noted | todo |

## Could (cut from the bottom first)
| ID | Task | Owner | Blocked-by | Done-when | Status |
|---|---|---|---|---|---|
| C1 | Per-accent and clinical vs general analysis | Opei | S1 | table in report + evidence | todo |
| C2 | Fine-tuning | Perfect | S1 | measured WER change | todo |
| C3 | Deployment | Nana | M3 | reachable demo | todo |

## Deliverables checklist
| Item | Owner | Proof file | Status |
|---|---|---|---|
| Code on GitHub | Elise | repo URL in README | todo |
| GitHub link on page 1 of slides | Nana | slides file | todo |
| GitHub link on page 1 of report | Nana | report PDF | todo |
| Report under 10 pages, ACL-style (PDF: "similar to ACL or other NLP publications"; we use the official ACL template) | Nana | report PDF | todo |
| Report content: answers Q1-Q4 with a scholarly case (rubric: Section A 20%) | all, split per outline | report/outline.md | todo |
| Report: implementation and results (rubric: Section B 20%) | all, split per outline | evidence/ + experiments/log.md | todo |
| Report: writing quality (rubric: 5%) | Nana (integrator) | final PDF | todo |
| Slides uploaded to Canvas | Nana | Canvas receipt screenshot in evidence/ | todo |
| Report uploaded to Canvas | Nana | Canvas receipt screenshot in evidence/ | todo |
| Viva prep: each person can walk through their area | each | learnings/<area>.md | todo |
| Final repo check (no secrets, README and PLAN current) | Elise, second person signs off | note in this table | todo |
