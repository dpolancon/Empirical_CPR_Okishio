"""Partition the canonical econometric audit ledger into phase ledgers."""

from __future__ import annotations

import argparse
import re
from datetime import datetime
from pathlib import Path

from run_audit import DEFAULT_MASTER_LEDGER, PHASE_LEDGER_NAMES, PHASE_TITLES


SOURCE_INTELLIGENCE_FILENAME = "00-source-intelligence.md"

SOURCE_INTELLIGENCE_PATTERN = re.compile(
    r"<!-- SOURCE_INTELLIGENCE_START -->\s*"
    r"(?P<body>.*?)"
    r"<!-- SOURCE_INTELLIGENCE_END -->",
    re.DOTALL,
)

PHASE_PATTERN = re.compile(
    r'<!-- AUDIT_PHASE_START phase="(?P<start>\d+)"[^>]*-->\s*'
    r"(?P<body>.*?)"
    r'<!-- AUDIT_PHASE_END phase="(?P<end>\d+)" -->',
    re.DOTALL,
)


def partition_ledger(master_path: Path, output_directory: Path) -> list[Path]:
    """Split a master ledger into source intelligence plus six phase ledgers."""
    master_path = master_path.expanduser().resolve()
    output_directory = output_directory.expanduser().resolve()
    if not master_path.is_file():
        raise FileNotFoundError(f"Master audit ledger not found: {master_path}")

    master_text = master_path.read_text(encoding="utf-8")
    source_match = SOURCE_INTELLIGENCE_PATTERN.search(master_text)
    if source_match is None:
        raise ValueError(
            f"Marked source-intelligence section not found in {master_path.name}."
        )
    matches = list(PHASE_PATTERN.finditer(master_text))
    if len(matches) != 6:
        raise ValueError(
            f"Expected 6 marked audit phases in {master_path.name}; found {len(matches)}."
        )

    output_directory.mkdir(parents=True, exist_ok=True)
    source_output_path = output_directory / SOURCE_INTELLIGENCE_FILENAME
    source_partition = f"""---
type: econometric_source_intelligence
source_master: "{master_path.name}"
generated: "{datetime.now().astimezone().isoformat(timespec="seconds")}"
---
# Source Intelligence Baseline

{source_match.group("body").strip()}
"""
    source_output_path.write_text(
        source_partition,
        encoding="utf-8",
        newline="\n",
    )
    written: list[Path] = [source_output_path]
    seen: set[int] = set()
    for match in matches:
        start_phase = int(match.group("start"))
        end_phase = int(match.group("end"))
        if start_phase != end_phase:
            raise ValueError(
                f"Mismatched phase markers: start={start_phase}, end={end_phase}."
            )
        if start_phase in seen or start_phase not in PHASE_LEDGER_NAMES:
            raise ValueError(f"Invalid or duplicate audit phase: {start_phase}.")
        seen.add(start_phase)

        output_path = output_directory / PHASE_LEDGER_NAMES[start_phase]
        partition = f"""---
type: econometric_audit_partition
source_master: "{master_path.name}"
audit_phase: {start_phase}
generated: "{datetime.now().astimezone().isoformat(timespec="seconds")}"
---
# Econometric Audit — Phase {start_phase}: {PHASE_TITLES[start_phase]}

{match.group("body").strip()}
"""
        output_path.write_text(partition, encoding="utf-8", newline="\n")
        written.append(output_path)
    return written


def build_argument_parser() -> argparse.ArgumentParser:
    repo_root = Path(__file__).resolve().parents[1]
    parser = argparse.ArgumentParser(
        description=(
            "Split the master econometric audit into source intelligence "
            "and six phase ledgers."
        )
    )
    parser.add_argument(
        "--master",
        type=Path,
        default=(
            repo_root
            / "knowledge"
            / "evidence"
            / "notebooklm"
            / DEFAULT_MASTER_LEDGER
        ),
    )
    parser.add_argument(
        "--output-directory",
        type=Path,
        default=repo_root / "knowledge" / "evidence" / "notebooklm" / "views",
    )
    return parser


def main() -> None:
    args = build_argument_parser().parse_args()
    written = partition_ledger(args.master, args.output_directory)
    for path in written:
        print(path)


if __name__ == "__main__":
    main()
