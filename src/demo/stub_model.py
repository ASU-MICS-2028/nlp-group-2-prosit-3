"""Stand-in for the real speech model until PLAN M2 lands.

The real model must keep this exact shape: (samples, sample_rate) -> text.
"""

import numpy as np


def stub_transcribe(samples: np.ndarray, sample_rate: int) -> str:
    seconds = len(samples) / sample_rate
    return f"[stub model] placeholder transcript for {seconds:.1f} s of audio; the real model comes in M2."
