"""Pipeline cases: good path, bad audio, empty transcript, failing model, out of memory."""

import numpy as np
import soundfile as sf

from demo.pipeline import DRAFT_WARNING, transcribe_file


def write_tone(tmp_path, seconds: float = 2.0, sample_rate: int = 16_000):
    t = np.arange(int(seconds * sample_rate)) / sample_rate
    path = tmp_path / "clip.wav"
    sf.write(path, (0.3 * np.sin(2 * np.pi * 440 * t)).astype(np.float32), sample_rate)
    return path


def test_good_audio_gives_text_and_draft_warning(tmp_path):
    result = transcribe_file(write_tone(tmp_path))
    assert result.ok
    assert "2.0 s" in result.text  # the stub saw the full 2 seconds
    assert result.message == DRAFT_WARNING


def test_resample_note_reaches_the_result(tmp_path):
    result = transcribe_file(write_tone(tmp_path, sample_rate=44_100))
    assert result.ok
    assert "44100 Hz -> 16000 Hz" in result.notes[0]


def test_bad_audio_gives_message_not_crash(tmp_path):
    result = transcribe_file(tmp_path / "missing.wav")
    assert not result.ok
    assert result.text == ""
    assert "could not be found" in result.message


def test_empty_transcript_is_flagged(tmp_path):
    result = transcribe_file(write_tone(tmp_path), model=lambda samples, sr: "   ")
    assert not result.ok
    assert "No speech was recognised" in result.message


def test_model_returning_none_is_flagged(tmp_path):
    result = transcribe_file(write_tone(tmp_path), model=lambda samples, sr: None)
    assert not result.ok
    assert "No speech was recognised" in result.message


def test_model_crash_gives_message(tmp_path):
    def broken_model(samples, sr):
        raise ValueError("bug inside the model")

    result = transcribe_file(write_tone(tmp_path), model=broken_model)
    assert not result.ok
    assert "model failed" in result.message


def test_out_of_memory_gives_message(tmp_path):
    def oom_model(samples, sr):
        raise MemoryError

    result = transcribe_file(write_tone(tmp_path), model=oom_model)
    assert not result.ok
    assert "out of memory" in result.message
