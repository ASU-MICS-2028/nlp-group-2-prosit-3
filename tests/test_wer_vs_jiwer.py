"""Cross-check our WER against the jiwer library on random word strings.

Skipped when jiwer is not installed (it is not a project requirement; install it with
`pip install jiwer` to run this check). Our own code is what we report; jiwer is only a second opinion.
"""

import random

import pytest

from evaluation.wer import corpus_wer

jiwer = pytest.importorskip("jiwer")


def test_matches_jiwer_on_2000_random_pairs():
    rng = random.Random(0)
    vocab = "a b c d e f".split()
    for _ in range(2000):
        ref = " ".join(rng.choices(vocab, k=rng.randint(1, 12)))
        hyp = " ".join(rng.choices(vocab, k=rng.randint(1, 12)))
        assert corpus_wer([(ref, hyp)]).wer == pytest.approx(jiwer.wer(ref, hyp)), (ref, hyp)
