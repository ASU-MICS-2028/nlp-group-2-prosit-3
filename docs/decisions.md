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
- ADR-4: demo tool (draft below, proposed by Nana for the M0 spike)

### ADR-4: demo tool for M3 (audio in, text out)
- Status: proposed (needs team agreement at the M0 spike; not accepted)
- Date: 2026-11-24
- Chose: Gradio (Python), run locally first; Hugging Face Spaces only if C3 (deployment) is reached.
- Why:
  - Gradio has a ready-made audio input (upload a file or record from the microphone), so we write almost no UI code
    and spend our time on input checks (bad audio, wrong sample rate, empty transcript), which M3 requires.
  - It is plain Python, the same language as the model and WER code, so the model owner can plug in without
    learning a new tool. We start with a stub model and swap in the real one after M2.
  - Hugging Face Spaces can host Gradio apps on a free CPU tier, which fits C3 and the free-tiers rule.
    (Free-tier limits: unverified, check the Spaces docs before relying on them.)
- Gave up:
  - Less control over layout than a custom web app (Flask + HTML). Fine for a demo, not a hospital product.
  - A free CPU Space may be slow for a large model; the demo may need a small model or local runs (depends on ADR-1).
  - The demo is not a secure clinical system: no login, no patient-data handling. We must say this in the report (Section 7).
- Options considered (cost, risk):
  - Gradio: free, low effort, built for ML demos. Risk: API changes between versions, so we pin the version.
  - Streamlit: free, also simple, has an audio input widget (check it exists in the current docs). Risk: whole script
    re-runs on each interaction, slightly more work to keep a loaded model in memory (needs caching).
  - Flask + HTML page: free, full control. Risk: we have to write the front end (upload/record page) ourselves,
    much more code for no grade
    benefit; takes time away from evaluation.
  - Notebook only (Colab): zero setup. Risk: not a real "audio in, text out" app for doctors; disconnects; weak for Q4.
- To check before accepting: Gradio Audio component docs (current version), Hugging Face Spaces free hardware limits,
  Streamlit audio input docs. Nobody has opened these yet for this ADR.
