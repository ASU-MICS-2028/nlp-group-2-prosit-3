"""Audio in, text out: input checks -> model -> output checks (PLAN M3).

`transcribe_file` never raises for bad input or a failing model. It always returns
a DemoResult, so the UI can show a clear message instead of crashing.
"""

from collections.abc import Callable
from dataclasses import dataclass, field
from pathlib import Path

import numpy as np

from demo.audio_checks import AudioError, load_and_check
from demo.stub_model import stub_transcribe

Transcriber = Callable[[np.ndarray, int], str]

DRAFT_WARNING = (
    "DRAFT machine transcript: it can contain wrong words, including drug names and doses. "
    "A clinician must check it before it goes into the patient record."
)


@dataclass
class DemoResult:
    ok: bool
    text: str  # the transcript; empty when ok is False
    message: str  # the draft warning when ok, otherwise what went wrong
    notes: list[str] = field(default_factory=list)  # what the input checks changed


def run_model(model: Transcriber, samples: np.ndarray, sample_rate: int) -> str:
    try:
        return model(samples, sample_rate)
    except MemoryError as err:
        raise AudioError("The model ran out of memory. Please try a shorter recording.") from err
    except Exception as err:  # any model bug must reach the user as a message, not a crash
        raise AudioError("The model failed on this recording. Please try again.") from err


def transcribe_file(path: str | Path | None, model: Transcriber = stub_transcribe) -> DemoResult:
    notes: list[str] = []
    try:
        audio = load_and_check(path)
        notes = audio.notes
        text = (run_model(model, audio.samples, audio.sample_rate) or "").strip()
    except AudioError as err:
        return DemoResult(ok=False, text="", message=str(err), notes=notes)
    if not text:
        return DemoResult(
            ok=False,
            text="",
            message="No speech was recognised. Please record again, closer to the microphone.",
            notes=notes,
        )
    return DemoResult(ok=True, text=text, message=DRAFT_WARNING, notes=notes)
