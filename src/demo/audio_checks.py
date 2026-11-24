"""Input checks for the dictation demo (PLAN M3).

Every recording goes through `load_and_check` before it reaches the model.
Bad input stops with an AudioError carrying a plain message for the doctor.
Fixable input (stereo, wrong sample rate) is fixed, and a note says what changed.
"""

from dataclasses import dataclass, field
from pathlib import Path

import librosa
import numpy as np
import soundfile as sf

# Our settings, not facts. Change them here only.
TARGET_SAMPLE_RATE = 16_000  # typical for speech models; unverified until ADR-1 picks the model
MAX_SECONDS = 60.0  # longer clips risk running out of memory on free compute
SILENCE_RMS = 1e-3  # below this average loudness we treat the clip as silent


class AudioError(Exception):
    """Input we cannot use. The message is shown to the user as-is."""


@dataclass
class CleanAudio:
    samples: np.ndarray  # mono, float32, at TARGET_SAMPLE_RATE
    sample_rate: int
    notes: list[str] = field(default_factory=list)


def check_file(path: str | Path | None) -> Path:
    if path is None or str(path).strip() == "":
        raise AudioError("No audio was given. Please upload or record a file.")
    path = Path(path)
    if not path.is_file():
        raise AudioError("The audio file could not be found.")
    if path.stat().st_size == 0:
        raise AudioError("The audio file is empty (0 bytes).")
    return path


def read_audio(path: Path) -> tuple[np.ndarray, int]:
    """Returns samples shaped (frames, channels) and the file's sample rate."""
    try:
        samples, sample_rate = sf.read(path, dtype="float32", always_2d=True)
    except (RuntimeError, OSError) as err:
        raise AudioError("Could not read this file as audio. Try a WAV or FLAC file.") from err
    if samples.shape[0] == 0:
        raise AudioError("The file contains no audio.")
    return samples, sample_rate


def check_duration(samples: np.ndarray, sample_rate: int) -> None:
    seconds = samples.shape[0] / sample_rate
    if seconds > MAX_SECONDS:
        raise AudioError(
            f"The recording is {seconds:.0f} s long; the limit is {MAX_SECONDS:.0f} s. "
            "Please split it into shorter parts."
        )


def to_mono(samples: np.ndarray, notes: list[str]) -> np.ndarray:
    channels = samples.shape[1]
    if channels > 1:
        notes.append(f"Mixed {channels} channels down to 1 (mono).")
    return samples.mean(axis=1)


def check_not_silent(samples: np.ndarray) -> None:
    rms = float(np.sqrt(np.mean(samples**2)))
    if rms < SILENCE_RMS:
        raise AudioError("No sound detected. Please check the microphone and record again.")


def to_target_rate(samples: np.ndarray, sample_rate: int, notes: list[str]) -> np.ndarray:
    if sample_rate == TARGET_SAMPLE_RATE:
        return samples
    note = f"Converted sample rate {sample_rate} Hz -> {TARGET_SAMPLE_RATE} Hz."
    if sample_rate < TARGET_SAMPLE_RATE:
        note += " Warning: low-quality audio; accuracy may be lower."
    notes.append(note)
    # librosa filters out high frequencies before dropping samples, which avoids aliasing.
    return librosa.resample(samples, orig_sr=sample_rate, target_sr=TARGET_SAMPLE_RATE)


def load_and_check(path: str | Path | None) -> CleanAudio:
    """Cheap checks first, so we never resample a file we are about to reject."""
    notes: list[str] = []
    file_path = check_file(path)
    samples, sample_rate = read_audio(file_path)
    check_duration(samples, sample_rate)
    mono = to_mono(samples, notes)
    check_not_silent(mono)
    clean = to_target_rate(mono, sample_rate, notes)
    return CleanAudio(samples=clean.astype(np.float32), sample_rate=TARGET_SAMPLE_RATE, notes=notes)
