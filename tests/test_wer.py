"""Tests for evaluation.wer (PLAN task E1). Every expected number is worked out by hand in the comment."""

from pathlib import Path

import pytest

from evaluation.wer import (
    corpus_wer,
    count_errors,
    evaluate_rows,
    load_rows,
    main,
    normalise,
    wer,
)

FIXTURE = Path(__file__).parent / "fixtures" / "fake_transcripts.csv"


def test_worked_example_from_understanding_md():
    # has->had = 1 S, "a" = 1 I, N = 4 -> (1 + 0 + 1) / 4 = 0.5
    c = count_errors("the patient has fever", "the patient had a fever")
    assert (c.substitutions, c.deletions, c.insertions, c.ref_words) == (1, 0, 1, 4)
    assert c.wer == pytest.approx(0.5)


def test_self_test_question_3():
    # "two" missing = 1 D, "now" extra = 1 I, N = 4 -> 2 / 4 = 0.5
    c = count_errors("take two tablets daily", "take tablets daily now")
    assert (c.substitutions, c.deletions, c.insertions) == (0, 1, 1)
    assert c.wer == pytest.approx(0.5)


def test_identical_is_zero():
    assert wer("blood pressure is normal", "blood pressure is normal") == 0.0


def test_case_and_punctuation_do_not_count():
    assert wer("The patient has fever.", "the patient, has fever") == 0.0


def test_numbers_are_not_converted():
    # "500" vs "five hundred": 1 S + 1 I over N = 2
    assert wer("500 mg", "five hundred mg") == pytest.approx(1.0)


def test_empty_hypothesis_is_all_deletions():
    c = count_errors("take two tablets", "")
    assert (c.deletions, c.wer) == (3, 1.0)


def test_wer_can_exceed_one():
    # 1 S ("yes"->"no") + 3 I over N = 1 -> 4.0
    assert wer("yes", "no no no no") == pytest.approx(4.0)


def test_empty_reference_raises():
    with pytest.raises(ValueError, match="undefined"):
        wer("", "anything")
    with pytest.raises(ValueError):
        wer("  ...  ", "anything")  # punctuation only becomes empty


def test_alignment_lists_each_step():
    c = count_errors("a b c", "a x c d")
    assert c.alignment == [("match", "a", "a"), ("sub", "b", "x"), ("match", "c", "c"), ("ins", "", "d")]


def test_corpus_wer_is_not_the_mean_of_clip_wers():
    # clip 1: 1 error / 1 word (WER 1.0); clip 2: 0 errors / 9 words (WER 0.0)
    # corpus = 1 / 10 = 0.1, while the mean of clip WERs would be 0.5
    pairs = [("yes", "no"), ("one two three four five six seven eight nine",) * 2]
    assert corpus_wer(pairs).wer == pytest.approx(0.1)


def test_apostrophe_and_unicode_kept_as_one_word():
    assert normalise("Patient's   Ɔkɔm") == "patient's ɔkɔm"
    assert wer("ɔkɔm", "ɔkɔm") == 0.0


def test_fake_csv_overall_and_grouped():
    rows = load_rows(FIXTURE)
    results = evaluate_rows(rows, by="accent")
    # fake-01: 2/4, fake-02: 2/4, fake-03: 0/4, fake-04: 1 I /5, fake-05: "500"->"five" S + "hundred" I = 2/6
    # total errors 7, total N 23
    assert results["ALL"].errors == 7
    assert results["ALL"].ref_words == 23
    assert results["ALL"].wer == pytest.approx(7 / 23)
    assert results["accent=twi"].wer == pytest.approx(2 / 8)
    assert results["accent=yoruba"].wer == pytest.approx(3 / 9)
    assert results["accent=igbo"].wer == pytest.approx(2 / 6)


def test_missing_column_fails_loudly(tmp_path):
    bad = tmp_path / "bad.csv"
    bad.write_text("id,reference\nx,hello\n", encoding="utf-8")
    with pytest.raises(ValueError, match="hypothesis"):
        load_rows(bad)


def test_empty_reference_row_fails_loudly(tmp_path):
    bad = tmp_path / "bad.csv"
    bad.write_text("id,reference,hypothesis\nx,,hello\n", encoding="utf-8")
    with pytest.raises(ValueError, match="'x'"):
        load_rows(bad)


def test_empty_hypothesis_cell_is_allowed(tmp_path):
    f = tmp_path / "ok.csv"
    f.write_text("id,reference,hypothesis\nx,take two tablets,\n", encoding="utf-8")
    assert evaluate_rows(load_rows(f))["ALL"].wer == 1.0


def test_unknown_group_column_fails():
    with pytest.raises(ValueError, match="speaker"):
        evaluate_rows(load_rows(FIXTURE), by="speaker")


def test_cli_prints_table(capsys):
    main([str(FIXTURE), "--by", "domain"])
    out = capsys.readouterr().out
    assert "ALL | 23 |" in out
    assert "domain=general | 5 | 0 | 0 | 1 | 0.2000" in out
