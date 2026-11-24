"""Word error rate (WER) for the Ayamra dictation project (PLAN task E1).

WER = (S + D + I) / N
  S = substitutions (a reference word replaced by a different word)
  D = deletions     (a reference word the system missed)
  I = insertions    (an extra word the system added)
  N = number of words in the REFERENCE (the human transcript)

Worked example (knowledge/understanding.md):
  reference  "the patient has fever"      N = 4
  hypothesis "the patient had a fever"    has->had is S, "a" is I
  WER = (1 + 0 + 1) / 4 = 0.50

We count S, D and I with the classic edit-distance table (Levenshtein, 1966),
applied to words instead of letters. It is our own code so every line can be
explained in the viva; tests check it against hand-worked examples.

Corpus WER adds up errors and words over ALL clips first, then divides once
(sum of errors / sum of N). It does NOT average per-clip WERs, because that
would let a 2-word clip count as much as a 40-word clip.

Run on a CSV with columns id, reference, hypothesis (optional extra columns,
e.g. accent or domain, can be used to group results):
  python -m evaluation.wer tests/fixtures/fake_transcripts.csv --by accent
"""

from __future__ import annotations

import argparse
import csv
import re
import unicodedata
from dataclasses import dataclass, field
from pathlib import Path

REQUIRED_COLUMNS = ("id", "reference", "hypothesis")

# Anything that is not a letter, digit, apostrophe or space becomes a space.
# Apostrophes stay so "patient's" stays one word. This is the proposed ADR-3 rule.
_PUNCTUATION = re.compile(r"[^\w\s']", flags=re.UNICODE)


def normalise(text: str) -> str:
    """Make two transcripts comparable: same Unicode form, lower case, no punctuation.

    "Paracetamol 500 mg, twice a day." -> "paracetamol 500 mg twice a day"
    Numbers are NOT converted to words ("500" vs "five hundred" still counts as errors).
    """
    text = unicodedata.normalize("NFC", text)
    text = text.lower()
    text = _PUNCTUATION.sub(" ", text)
    text = text.replace("_", " ")  # \w keeps underscores; we do not want them
    return " ".join(text.split())


def words(text: str) -> list[str]:
    """Normalise, then split on spaces."""
    return normalise(text).split()


@dataclass
class ErrorCounts:
    """How many of each error type, plus N (reference length)."""

    substitutions: int = 0
    deletions: int = 0
    insertions: int = 0
    hits: int = 0
    ref_words: int = 0
    alignment: list[tuple[str, str, str]] = field(default_factory=list, repr=False)

    @property
    def errors(self) -> int:
        return self.substitutions + self.deletions + self.insertions

    @property
    def wer(self) -> float:
        if self.ref_words == 0:
            raise ValueError("WER is undefined when the reference has no words (N = 0).")
        return self.errors / self.ref_words

    def __add__(self, other: "ErrorCounts") -> "ErrorCounts":
        return ErrorCounts(
            substitutions=self.substitutions + other.substitutions,
            deletions=self.deletions + other.deletions,
            insertions=self.insertions + other.insertions,
            hits=self.hits + other.hits,
            ref_words=self.ref_words + other.ref_words,
        )


def align(reference: list[str], hypothesis: list[str]) -> ErrorCounts:
    """Find the cheapest way to turn the reference into the hypothesis, then count each step.

    cost[i][j] = fewest edits to turn the first i reference words into the first j hypothesis words.
    Each cell takes the cheapest of: match/substitute (diagonal), delete (up), insert (left).
    """
    n_ref, n_hyp = len(reference), len(hypothesis)
    cost = [[0] * (n_hyp + 1) for _ in range(n_ref + 1)]
    for i in range(n_ref + 1):
        cost[i][0] = i  # delete all i reference words
    for j in range(n_hyp + 1):
        cost[0][j] = j  # insert all j hypothesis words

    for i in range(1, n_ref + 1):
        for j in range(1, n_hyp + 1):
            same = reference[i - 1] == hypothesis[j - 1]
            cost[i][j] = min(
                cost[i - 1][j - 1] + (0 if same else 1),  # match or substitution
                cost[i - 1][j] + 1,  # deletion
                cost[i][j - 1] + 1,  # insertion
            )

    # Walk back from the bottom-right corner to see WHICH edits were used.
    counts = ErrorCounts(ref_words=n_ref)
    steps: list[tuple[str, str, str]] = []
    i, j = n_ref, n_hyp
    while i > 0 or j > 0:
        if i > 0 and j > 0:
            same = reference[i - 1] == hypothesis[j - 1]
            if cost[i][j] == cost[i - 1][j - 1] + (0 if same else 1):
                if same:
                    counts.hits += 1
                    steps.append(("match", reference[i - 1], hypothesis[j - 1]))
                else:
                    counts.substitutions += 1
                    steps.append(("sub", reference[i - 1], hypothesis[j - 1]))
                i, j = i - 1, j - 1
                continue
        if i > 0 and cost[i][j] == cost[i - 1][j] + 1:
            counts.deletions += 1
            steps.append(("del", reference[i - 1], ""))
            i -= 1
        else:
            counts.insertions += 1
            steps.append(("ins", "", hypothesis[j - 1]))
            j -= 1
    counts.alignment = list(reversed(steps))
    return counts


def count_errors(reference: str, hypothesis: str) -> ErrorCounts:
    """S, D, I and N for one clip, after normalising both texts."""
    return align(words(reference), words(hypothesis))


def wer(reference: str, hypothesis: str) -> float:
    """WER for one clip. Raises ValueError if the reference is empty."""
    return count_errors(reference, hypothesis).wer


def corpus_wer(pairs: list[tuple[str, str]]) -> ErrorCounts:
    """Add up S, D, I and N over many (reference, hypothesis) pairs. Use .wer on the result."""
    total = ErrorCounts()
    for reference, hypothesis in pairs:
        total = total + count_errors(reference, hypothesis)
    return total


def load_rows(csv_path: str | Path) -> list[dict[str, str]]:
    """Read a transcripts CSV. Fails loudly on missing columns or empty references."""
    with open(csv_path, newline="", encoding="utf-8") as handle:
        reader = csv.DictReader(handle)
        missing = [c for c in REQUIRED_COLUMNS if c not in (reader.fieldnames or [])]
        if missing:
            raise ValueError(f"{csv_path}: missing column(s) {missing}; need {list(REQUIRED_COLUMNS)}")
        rows = [dict(row) for row in reader]
    for row in rows:
        if not words(row["reference"] or ""):
            raise ValueError(f"{csv_path}: row {row['id']!r} has an empty reference, WER is undefined")
        row["hypothesis"] = row["hypothesis"] or ""  # an empty transcript is allowed: all deletions
    return rows


def evaluate_rows(rows: list[dict[str, str]], by: str | None = None) -> dict[str, ErrorCounts]:
    """Corpus WER for all rows ("ALL"), and per value of column `by` if given."""
    results: dict[str, ErrorCounts] = {"ALL": ErrorCounts()}
    for row in rows:
        counts = count_errors(row["reference"], row["hypothesis"])
        results["ALL"] = results["ALL"] + counts
        if by is not None:
            if by not in row:
                raise ValueError(f"no column {by!r} to group by")
            key = f"{by}={row[by] or 'unknown'}"
            results[key] = results.get(key, ErrorCounts()) + counts
    return results


def format_table(results: dict[str, ErrorCounts]) -> str:
    lines = ["group | N | S | D | I | WER", "---|---|---|---|---|---"]
    for name, c in results.items():
        lines.append(f"{name} | {c.ref_words} | {c.substitutions} | {c.deletions} | {c.insertions} | {c.wer:.4f}")
    return "\n".join(lines)


def main(argv: list[str] | None = None) -> None:
    parser = argparse.ArgumentParser(description="Corpus WER from a CSV of reference/hypothesis pairs.")
    parser.add_argument("csv_path", help="CSV with columns id, reference, hypothesis")
    parser.add_argument("--by", help="optional column to group by, e.g. accent or domain")
    args = parser.parse_args(argv)
    print(format_table(evaluate_rows(load_rows(args.csv_path), by=args.by)))


if __name__ == "__main__":
    main()
