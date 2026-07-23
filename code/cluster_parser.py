"""Parse and normalize NotebookLM econometric audit question clusters."""

from __future__ import annotations

import csv
from pathlib import Path
from typing import Any

import pandas as pd


HEADER_ALIASES = {
    "id": ("ID",),
    "audit_question": ("Audit Question", "Audit Question for NotebookLM"),
    "target_concept": ("Target Concept", "Specific Literature Target"),
    "validation_metric": (
        "Validation Metric",
        "Validation Metric (What to look for in the answer)",
    ),
}

def parse_cluster(csv_path: str | Path) -> list[dict[str, Any]]:
    """Read one cluster CSV into normalized dictionaries."""
    path = Path(csv_path).expanduser().resolve()
    if not path.is_file():
        raise FileNotFoundError(f"Cluster CSV not found: {path}")

    # The supplied ledgers contain unescaped quotation marks and commas inside
    # mathematical prose. The csv module exposes recoverable pieces, and the
    # stable "Look for..." phrase marks the validation field. A DataFrame then
    # provides consistent string normalization and dictionary records.
    with path.open(encoding="utf-8-sig", newline="") as cluster_file:
        rows = list(csv.reader(cluster_file))
    if not rows:
        raise ValueError(f"Cluster CSV is empty: {path}")

    records: list[dict[str, Any]] = []
    for row_number, row in enumerate(rows[1:], start=2):
        if not row or not any(cell.strip() for cell in row):
            continue
        validation_index = next(
            (
                index
                for index, cell in enumerate(row[2:], start=2)
                if cell.lstrip(' "').startswith("Look for")
            ),
            None,
        )
        if validation_index is None or validation_index < 3:
            raise ValueError(
                f"Could not recover the four fields in {path.name}, row {row_number}."
            )

        records.append(
            {
                "id": row[0].strip(),
                "audit_question": ",".join(row[1 : validation_index - 1]).strip(),
                "target_concept": row[validation_index - 1].strip(),
                "validation_metric": ",".join(row[validation_index:]).strip(),
            }
        )
    frame = pd.DataFrame.from_records(records, columns=HEADER_ALIASES)
    normalized = frame.fillna("").astype(str).to_dict(orient="records")
    return _validate_records(normalized, path)


def _validate_records(
    records: list[dict[str, Any]],
    path: Path,
) -> list[dict[str, Any]]:
    for row_number, record in enumerate(records, start=2):
        if not record["id"] or not record["audit_question"]:
            raise ValueError(f"Blank ID or audit question in {path.name}, row {row_number}.")
        record["cluster"] = path.stem
    return records


def parse_all_clusters(cluster_directory: str | Path) -> list[dict[str, Any]]:
    """Read cluster_1.csv through cluster_6.csv in numeric order."""
    directory = Path(cluster_directory).expanduser().resolve()
    questions: list[dict[str, Any]] = []
    for cluster_number in range(1, 7):
        questions.extend(parse_cluster(directory / f"cluster_{cluster_number}.csv"))
    return questions
