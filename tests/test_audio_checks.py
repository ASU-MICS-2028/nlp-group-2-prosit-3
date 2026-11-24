"""One test per input case in the M3 design. Test audio is generated here, never committed."""

import numpy as np
import pytest
import soundfile as sf

from demo.audio_checks import MAX_SECONDS, TARGET_SAMPLE_RATE, AudioError, load_and_check


def tone(seconds: float, sample_rate: int, channels: int = 1, loudness: float = 0.3) -> np.ndarray:
    """A 440 Hz sine wave, shaped (frames, channels)."""
    t = np.arange(int(seconds * sample_rate)) / sample_rate
    wave = (loudness * np.sin(2 * np.pi * 440 * t)).astype(np.float32)
    return np.repeat(wave[:, None], channels, axis=1)


def write_wav(tmp_path, samples: np.ndarray, sample_rate: int, name: str = "clip.wav"):
    path = tmp_path / name
    sf.write(path, samples, sample_rate)
    return path


def test_good_16k_mono_passes_unchanged(tmp_path):
    path = write_wav(tmp_path, tone(2.0, 16_000), 16_000)
    result = load_and_check(path)
    assert result.sample_rate == TARGET_SAMPLE_RATE
    assert result.samples.shape == (32_000,)  # 2 s x 16,000 samples per second
    assert result.notes == []


def test_44k_is_downsampled_with_note(tmp_path):
    path = write_wav(tmp_path, tone(10.0, 44_100), 44_100)
    result = load_and_check(path)
    assert result.samples.shape == (160_000,)  # 441,000 samples -> 160,000
    assert "44100 Hz -> 16000 Hz" in result.notes[0]
    assert "Warning" not in result.notes[0]


def test_8k_is_upsampled_with_warning(tmp_path):
    path = write_wav(tmp_path, tone(1.0, 8_000), 8_000)
    result = load_and_check(path)
    assert result.samples.shape == (16_000,)
    assert "Warning" in result.notes[0]


def test_stereo_is_mixed_to_mono(tmp_path):
    path = write_wav(tmp_path, tone(1.0, 16_000, channels=2), 16_000)
    result = load_and_check(path)
    assert result.samples.ndim == 1
    assert "2 channels" in result.notes[0]


@pytest.mark.parametrize("bad_path", [None, ""])
def test_no_file_given(bad_path):
    with pytest.raises(AudioError, match="No audio"):
        load_and_check(bad_path)


def test_missing_file(tmp_path):
    with pytest.raises(AudioError, match="could not be found"):
        load_and_check(tmp_path / "nope.wav")


def test_zero_byte_file(tmp_path):
    path = tmp_path / "empty.wav"
    path.write_bytes(b"")
    with pytest.raises(AudioError, match="0 bytes"):
        load_and_check(path)


def test_not_audio_file(tmp_path):
    path = tmp_path / "report.wav"  # a text file pretending to be audio
    path.write_text("this is not audio")
    with pytest.raises(AudioError, match="Could not read"):
        load_and_check(path)


def test_valid_header_but_no_frames(tmp_path):
    path = write_wav(tmp_path, np.zeros((0, 1), dtype=np.float32), 16_000)
    with pytest.raises(AudioError, match="no audio"):
        load_and_check(path)


def test_too_long(tmp_path):
    path = write_wav(tmp_path, tone(MAX_SECONDS + 1, 8_000), 8_000)
    with pytest.raises(AudioError, match="limit"):
        load_and_check(path)


def test_silent(tmp_path):
    path = write_wav(tmp_path, np.zeros((16_000, 1), dtype=np.float32), 16_000)
    with pytest.raises(AudioError, match="No sound"):
        load_and_check(path)
