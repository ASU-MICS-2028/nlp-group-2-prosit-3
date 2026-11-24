# Understanding the Ask, the Plan and the Mental Model

Read this before approving anything. If a section doesn't make sense, say so. That is a bug in this file, not in you.
Nothing here is a result. Claims about what will work are marked **hypothesis** until we measure them.

---

## 1. The ask in plain words

**The story.** Ayamra (hospitals in African cities) wants doctors to *speak* their notes and get text back.
A consultant told them: "use RNNs, and train on the AfriSpeech-200 dataset."

**Our job.** We are the AI technologists they hired. We must NOT just obey the consultant. We must:

| # | Ayamra asks | What a good answer looks like |
|---|---|---|
| Q1 | What are RNNs and how could they solve this? | Plain explanation + how an RNN-based speech recogniser is built (audio in, text out) |
| Q2 | Are RNNs the best approach? Pros and cons vs others? | A fair comparison, backed by citations AND our own measurement |
| Q3 | Would we recommend RNNs? If not, what and why? | A clear recommendation with reasons tied to the evidence |
| Q4 | Can we build the recommended system? | A working demo + a measured error rate + honest limits |

**What we hand in:** a technical report (ACL style, under 10 pages), a 10-minute presentation, code on GitHub
(link on page 1 of both report and slides), then an individual viva quiz.

**Grading (what each piece is really testing):**
- Presentation 20%: is it *educational*, and do we *understand our own work*?
- Report 45%: Section A (individual) 20%, Section B (shared; implementation + results) 20%, writing 5%.
- Viva 35%: individual questions. **This is the biggest single item.** Nobody can borrow someone else's understanding.

**Note on framing (from the PDF):** the Prosit is titled "Supervised Speech Recognition **with Transformers**", and Ayamra
wants to *understand* the system. So our RNN-vs-transformer section is a *justified recommendation* (we expect to
recommend a transformer and must prove why, including where RNNs win), and everything must be readable by non-technical
hospital leaders. Section 3 below is still a hypothesis until we measure.

**The hidden point:** the course wants us to *read papers, build, measure, and explain*, not to ship the fanciest model.
An honest small result that we fully understand beats an impressive result we can't explain.

---

## 2. Mental model: how speech-to-text (ASR) works

Think of it as a pipeline. Every technical term we meet belongs to one box.

```
 sound wave ──► features ──► ENCODER ──► per-moment guesses ──► DECODER ──► text
 (16,000 numbers   (spectrogram:      (the neural net:          (probabilities     (pick the
  per second)       "which pitches     RNN OR Transformer)       of letters/words    best sentence)
                    at which time")                              at each moment)
```

1. **Audio is just numbers.** A waveform sampled N times per second (the *sample rate*, e.g. 16 kHz). Wrong sample rate = garbage out. This is a real failure path we must test.
2. **Features.** We turn the waveform into a spectrogram (a picture of pitch over time) because that's easier for a network to read.
3. **Encoder = the part we are comparing.** It reads the sequence of audio moments and builds a representation.
   - **RNN:** reads one moment at a time, left to right, carrying a "memory" (hidden state) forward. Like reading a sentence word by word and keeping notes.
   - **Transformer:** looks at *all* moments at once and learns which ones relate to which (**attention**). Like laying the whole page out and drawing lines between related words.
4. **Aligning sound to text.** Audio is long (many moments) and text is short (few letters). We need a rule for matching them.
   **CTC** is one such rule (tiny example below). Alternatives: attention-based encoder-decoder.
5. **Decoder.** Turns the per-moment guesses into the final text.
6. **Evaluation:** WER (below) compares the output text with the human reference text.

### Tiny worked example A: CTC collapse
The net outputs one symbol per moment, allowing a blank `-`. Say it outputs: `h h e - l l - l o o`
- Step 1, merge repeats: `h e - l - l o`
- Step 2, drop blanks: `h e l l o`

The blank between the two `l` groups is what lets CTC write a *double* "ll". That's why blanks exist.
(CTC = Connectionist Temporal Classification; see sources.)

### Tiny worked example B: WER
WER = (S + D + I) / N, where S = substitutions, D = deletions, I = insertions, N = words in the *reference*.
- Reference: `the patient has fever` (N = 4)
- Hypothesis: `the patient had a fever`
- Alignment: `has`→`had` is 1 substitution; `a` is 1 insertion; 0 deletions.
- WER = (1 + 0 + 1) / 4 = **0.50** (50%).

Notes to be able to say in the viva: WER can exceed 100% (many insertions); it counts *words*, so one wrong letter in a
drug name costs a whole word, which matters clinically. Lower is better.

### Why this matters for hospitals (the "so what")
- Doctors speak with many **African accents** and use **medical terms**. The dataset is built around this
  (check the dataset card for exactly how, see Section 6).
- A wrong word in a medical note can be harmful, so the report must discuss "what if the model is wrong" and
  recommend human review, not blind trust.

---

## 3. RNN vs Transformer: the argument we will test

Say this out loud until it is natural. It is a **hypothesis**, not a finding yet.

**Why RNNs were popular for speech:** audio is naturally a sequence, and RNNs (e.g. LSTM/GRU) process sequences step by step.
Early end-to-end systems used them with CTC.

**Why we suspect they are not the best choice today (hypothesis, to be supported by papers AND our run):**
- *Sequential:* each step waits for the last, so training can't be parallelised as well. Slower on GPUs.
- *Long-range memory:* audio is very long; keeping information across many steps is hard.
- *Data hunger:* a model trained from scratch needs lots of labelled audio. Our accented, low-resource setting has little.
- *Transformers + pretraining:* models pretrained on huge amounts of speech can be **fine-tuned** or used directly with
  little data. That is the key practical advantage for a low-resource setting.

**What we would honestly also say in favour of RNNs:** small, cheap at inference, can stream (process audio as it
arrives), and are simpler to understand. Report these. A fair comparison has both sides.

**Our experiment (MUST tier):** a small RNN/CTC baseline vs a pretrained transformer, on the *same* small subset,
*same* metric (WER), *same* split, with hardware and seed noted. If the RNN wins on our setup, we report that too.
Negative results count.

---

## 4. How we achieve the deliverables

| Deliverable | How we get it | Proof (a file anyone can open) |
|---|---|---|
| Q1 answer | Read the sources, write it in plain words, add the RNN/CTC baseline as the concrete example | `report/` section + `learnings/models.md` |
| Q2 answer | Literature (cited) + our measured comparison | `experiments/log.md` rows + `evidence/` |
| Q3 answer | Recommendation follows from Q2 evidence, including cost, data and accent limits | `report/` section |
| Q4 answer | Pretrained-model transcription of real AfriSpeech audio, WER measured, small demo | demo + `evidence/` |
| Code on GitHub | Public repo, no secrets, no audio, no checkpoints | repo + final check row in PLAN.md |
| Report (<10 pages, ACL template) | Skeleton with "TBD" result slots written on day 1; results dropped in as they arrive | `report/outline.md` → final PDF |
| Slides | Built from the report, GitHub link on slide 1 | slides file + Canvas upload |
| Viva readiness | Each owner writes 5 viva Q&A in their learnings note; everyone runs the whole pipeline once on 10 clips | `learnings/*.md` |

**Scope ladder (cut from the bottom first):**
- **MUST:** honest, cited answers to Q1-Q3; one real AfriSpeech clip transcribed with a measured WER; a small demo;
  RNN/CTC baseline vs pretrained transformer on the same small subset (so Q2 has our own measurement).
- **SHOULD:** fine-tuning; per-accent and clinical vs general analysis (the brief stresses training and Africa-focused ideas).
- **COULD:** deployment.

**How we avoid last project's failures:**
| Prosit 2 problem | Rule now |
|---|---|
| Status in 3 places | Status only in PLAN.md |
| Report written last | Skeleton with TBD slots on day 1 |
| Stale claims on deadline day | Integrator checks each claim against `evidence/` / `experiments/log.md` |
| One section missing at the end | One row per person for Section A in the deliverables checklist, checked early |

**How we avoid stalling when someone is away:** every area has an owner and a backup, and every task has a fallback
input (e.g. evaluation runs on a fake CSV; the demo runs on a stub model until the real one exists).

---

## 5. Who owns what (proposal, confirm before treating as final)

| Area | Owner | Backup |
|---|---|---|
| Data (load, subset, accents, splits) | Elise | Perfect |
| Models (pretrained inference + small RNN/CTC baseline) | Perfect | Elise |
| Evaluation (WER, per-accent, error analysis) | Opei | Nana |
| Demo + deployment (thin) | Nana | Opei |
| Integrator (checks every report claim vs evidence) | Nana (Elise checks Nana's own numbers) | |
| Final repo check (sign-off) | Elise | |

Report questions: Q1 Perfect, Q2 Opei, Q3 Elise, Q4 Nana. Each person also reviews one other person's question.
Owning an area means *leading* it, not being the only one who understands it. The viva can ask anyone about any stage.

---

## 6. Sources to read first (verify each exists before citing)

Marked `sure` = I am confident it exists; `check it exists` = search first. None of these has been opened by us yet.

- Dataset card: AfriSpeech-200 on Hugging Face (URL is in the brief). `sure`. **All dataset facts (size, accents, splits, licence) must come from this card; we have not read it yet.**
- Olatunji et al., 2023, the AfriSpeech-200 paper. `check it exists`. Search: `AfriSpeech-200 Pan-African accented speech dataset clinical general domain ASR`
- Graves et al., 2006, Connectionist Temporal Classification. `sure`. Search: `Graves Fernandez Gomez Schmidhuber 2006 connectionist temporal classification`
- Vaswani et al., 2017, "Attention Is All You Need". `sure`.
- Baevski et al., 2020, wav2vec 2.0. `sure`. Search: `wav2vec 2.0 self-supervised learning of speech representations`
- Radford et al., 2022, Whisper ("Robust Speech Recognition via Large-Scale Weak Supervision"). `sure`. Search: `Whisper robust speech recognition large-scale weak supervision`
- Hannun et al., 2014, Deep Speech. `check it exists`. Search: `Deep Speech scaling up end-to-end speech recognition Hannun`
- Hugging Face Transformers docs, the ASR task / pipeline page. `check it exists`. Search: `Hugging Face transformers automatic speech recognition task guide`

Any source we actually use gets added to `knowledge/reading-list.md`.

---

## 7. Self-test (answer before approving the plan; answers go in your learnings note)

1. In one sentence, what does an ASR encoder do?
2. Why does CTC need a blank symbol? (Use the `hello` example.)
3. Compute the WER for reference `take two tablets daily` vs hypothesis `take tablets daily now`. Show S, D, I, N.
4. Give one reason RNNs might be a poor fit here and one reason they might still be reasonable.
5. Why do we compare models on the *same* subset, split and metric?
6. Why is a low WER on general speech not enough to trust the system in a hospital?
