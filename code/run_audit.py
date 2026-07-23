"""Run the six-phase NotebookLM econometric audit."""

from __future__ import annotations

import argparse
import logging
import random
import time
from datetime import datetime
from pathlib import Path
from typing import Any

from cluster_parser import parse_cluster
from notebooklm_engine import NotebookLMAuditor, ThreadResetError


MASTER_SYSTEM_PROMPT = """You are a Senior Econometric Referee for *Econometric Theory*. I will provide you with questions from an Econometric Audit Ledger. Your task is to systematically validate the mathematical claims in my uploaded notes by interrogating the uploaded source literature (Wagner & Hong, Vogelsang & Wagner, etc.). For every question, you must provide: (1) The exact Theorem/Lemma name from the literature, (2) The rigorous mathematical proof or condition using standard LaTeX, and (3) A 'Pass/Fail' verdict on whether my notes correctly captured the asymptotic mechanics. Do not summarize. Provide only dense mathematical validation."""

SOURCE_INTELLIGENCE_QUERY = """Extract the 3 most critical contributions of this paper specifically relevant to validating Cointegrating Polynomial Regressions (CPR) with I(2) interactive terms. Focus exclusively on asymptotic mechanics, rank conditions, and estimator transformations. Output as dense bullet points with LaTeX."""

DEFAULT_NOTEBOOK_ID = "b0c5603e-e34a-4c97-b436-8577da5280eb"
DEFAULT_NOTEBOOK_TITLE = "CPR Co-integration IM-OLS"
DEFAULT_MASTER_LEDGER = "econometric_audit_master.md"
DEFAULT_EXPECTED_SOURCE_COUNT = 14

PHASE_LEDGER_NAMES = {
    1: "audit_phase_1_i2_trap.md",
    2: "audit_phase_2_dols_fmols.md",
    3: "audit_phase_3_im_ols.md",
    4: "audit_phase_4_fwl_orthogonalization.md",
    5: "audit_phase_5_cpr_cointegration_tests.md",
    6: "audit_phase_6_delta_wald.md",
}

PHASE_TITLES = {
    1: "The I(2) Trap",
    2: "DOLS and FM-OLS",
    3: "IM-OLS",
    4: "FWL Orthogonalization",
    5: "CPR Cointegration Tests",
    6: "Delta Method and Wald Tests",
}

PHASE_SLUGS = {
    1: "i2-trap",
    2: "dols-fmols",
    3: "im-ols",
    4: "fwl-orthogonalization",
    5: "cpr-cointegration-tests",
    6: "delta-wald",
}


def _table_cell(value: str) -> str:
    return value.replace("\\", "&#92;").replace("|", "&#124;").replace("\r", " ").replace("\n", " ")


class QueryRateLimiter:
    """Apply query jitter and a longer pause around thread boundaries."""

    def __init__(
        self,
        *,
        jitter_min: float = 8.0,
        jitter_max: float = 15.0,
        thread_pause: float = 30.0,
        sleeper: Any = None,
        randomizer: Any = None,
    ) -> None:
        if jitter_min < 0 or jitter_max < jitter_min:
            raise ValueError("Jitter bounds must satisfy 0 <= min <= max.")
        if thread_pause < 0:
            raise ValueError("Thread pause cannot be negative.")
        self.jitter_min = jitter_min
        self.jitter_max = jitter_max
        self.thread_pause = thread_pause
        self.sleeper = sleeper or time.sleep
        self.randomizer = randomizer or random.uniform
        self.query_count = 0

    def before_query(self, *, new_thread: bool) -> None:
        if self.query_count:
            delay = self.randomizer(self.jitter_min, self.jitter_max)
            logging.info("Inter-query rate-limit pause: %.1f seconds.", delay)
            self.sleeper(delay)
        if new_thread:
            logging.info(
                "Thread reset/creation pause: %.1f seconds.",
                self.thread_pause,
            )
            self.sleeper(self.thread_pause)
        self.query_count += 1

    def before_final_reset(self) -> None:
        logging.info("Final thread-close pause: %.1f seconds.", self.thread_pause)
        self.sleeper(self.thread_pause)


def _question_prompt(question: dict[str, Any]) -> str:
    return f"""Audit ledger ID: {question["id"]}

Specific literature target:
{question["target_concept"]}

Audit question:
{question["audit_question"]}

Mandatory validation metric:
{question["validation_metric"]}

Explicitly test the proposed validation metric against the uploaded sources. If
the metric itself is mathematically false or unsupported by those sources,
state that fact and return a Fail verdict rather than repairing it silently."""


def _master_ledger_header(
    notebook_id: str,
    notebook_title: str,
    source_count: int,
) -> str:
    return f"""---
type: econometric_audit_master
status: running
notebook_id: "{notebook_id}"
notebook_title: "{notebook_title}"
source_intelligence_count: {source_count}
source_clusters: [1, 2, 3, 4, 5, 6]
partition_key: audit_phase
---
# Econometric Audit Master Ledger

| Field | Value |
|---|---|
| NotebookLM notebook ID | `{notebook_id}` |
| Generated | {datetime.now().astimezone().isoformat(timespec="seconds")} |
| Source-intelligence threads | {source_count} |
| Source clusters | `cluster_1.csv` through `cluster_6.csv` |
| Partition contract | Stable HTML boundary markers around every phase and question |

"""


def _source_intelligence_header() -> str:
    return """<!-- SOURCE_INTELLIGENCE_START -->
## Source Intelligence Baseline

Each source below was queried in a clean, source-restricted NotebookLM thread.

"""


def _source_intelligence_footer() -> str:
    return """<!-- SOURCE_INTELLIGENCE_END -->

"""


def _render_source_intelligence(
    source_number: int,
    source: dict[str, Any],
    answer: str,
) -> str:
    source_id = str(source.get("id", "UNKNOWN"))
    title = str(source.get("title", "Untitled source")).replace("\r", " ").replace("\n", " ")
    source_type = str(source.get("type", "UNKNOWN"))
    return f"""<!-- SOURCE_INTELLIGENCE_ITEM_START index="{source_number}" source_id="{source_id}" -->
### Source {source_number:02d} — {title}

| Source field | Value |
|---|---|
| NotebookLM source ID | `{source_id}` |
| Source type | `{source_type}` |
| Thread policy | New source-restricted thread |

#### Query

{SOURCE_INTELLIGENCE_QUERY}

#### Critical contributions

{answer.rstrip()}

<!-- SOURCE_INTELLIGENCE_ITEM_END index="{source_number}" source_id="{source_id}" -->

"""


def _phase_header(phase: int) -> str:
    return f"""<!-- AUDIT_PHASE_START phase="{phase}" slug="{PHASE_SLUGS[phase]}" source="cluster_{phase}.csv" -->
## Phase {phase} — {PHASE_TITLES[phase]}

"""


def _phase_footer(phase: int) -> str:
    return f"""<!-- AUDIT_PHASE_END phase="{phase}" -->

"""


def _render_answer(phase: int, question: dict[str, Any], answer: str) -> str:
    return f"""<!-- AUDIT_QUESTION_START id="{question["id"]}" phase="{phase}" -->
### {question["id"]}

| Audit field | Content |
|---|---|
| Literature target | {_table_cell(question["target_concept"])} |
| Validation metric | {_table_cell(question["validation_metric"])} |

#### Audit question

{question["audit_question"]}

#### NotebookLM mathematical validation

{answer.rstrip()}

<!-- AUDIT_QUESTION_END id="{question["id"]}" phase="{phase}" -->

"""


def _log_failure(log_path: Path, scope: str, item_id: str, exc: Exception) -> None:
    timestamp = datetime.now().astimezone().isoformat(timespec="seconds")
    log_path.parent.mkdir(parents=True, exist_ok=True)
    with log_path.open("a", encoding="utf-8", newline="\n") as log_file:
        log_file.write(
            f"[{timestamp}] scope={scope} id={item_id} "
            f"error={type(exc).__name__}: {exc}\n"
        )


def _append_text(path: Path, text: str) -> None:
    with path.open("a", encoding="utf-8", newline="\n") as output:
        output.write(text)


def _set_ledger_status(path: Path, status: str) -> None:
    if not path.is_file():
        return
    text = path.read_text(encoding="utf-8")
    updated = text.replace("status: running", f"status: {status}", 1)
    path.write_text(updated, encoding="utf-8", newline="\n")


def run_audit(args: argparse.Namespace) -> None:
    repo_root = Path(__file__).resolve().parents[1]
    cluster_directory = (args.cluster_directory or repo_root / "cluster_question_files").resolve()
    ledger_directory = (
        args.ledger_directory or repo_root / "working_ledgers" / "notebooklm"
    ).resolve()
    ledger_path = (
        args.ledger_file.resolve()
        if args.ledger_file
        else ledger_directory / DEFAULT_MASTER_LEDGER
    )
    failure_log = (
        args.failure_log or ledger_directory / "failed_questions.log"
    ).resolve()
    notes_path = (
        args.notes
        or repo_root / "notes" / "source_snapshots" / "i2_trap"
    ).resolve()
    ledger_directory.mkdir(parents=True, exist_ok=True)

    auditor = NotebookLMAuditor(
        request_timeout=args.request_timeout,
        source_wait_timeout=args.source_wait_timeout,
    )
    rate_limiter = QueryRateLimiter(
        jitter_min=args.jitter_min,
        jitter_max=args.jitter_max,
        thread_pause=args.thread_pause,
    )
    ledger_initialized = False
    failed_queries = 0
    try:
        logging.info("Validating NotebookLM authentication.")
        auditor.authenticate()
        if args.create_notebook:
            if not args.pdf:
                raise ValueError("--create-notebook requires at least one --pdf source.")
            notebook_id = auditor.setup_notebook(
                args.notebook_name,
                args.pdf,
                notes_path,
            )
        else:
            notebook_id = auditor.connect_notebook(args.notebook)
        logging.info("Notebook ready: %s", notebook_id)
        if len(auditor.sources) != args.expected_source_count:
            raise RuntimeError(
                f"Expected {args.expected_source_count} ready notebook sources; "
                f"found {len(auditor.sources)}. Reconcile the source inventory "
                "before running a destructive thread-reset audit."
            )

        ledger_path.parent.mkdir(parents=True, exist_ok=True)
        if ledger_path.exists() and ledger_path.stat().st_size:
            raise FileExistsError(
                f"Canonical audit ledger already exists and is append-only: "
                f"{ledger_path}. Use --ledger-file with a new path for another run."
            )
        ledger_path.write_text(
            _master_ledger_header(
                notebook_id,
                auditor.notebook_title or DEFAULT_NOTEBOOK_TITLE,
                len(auditor.sources),
            ),
            encoding="utf-8",
            newline="\n",
        )
        ledger_initialized = True

        _append_text(ledger_path, _source_intelligence_header())
        for source_number, source in enumerate(auditor.sources, start=1):
            source_id = str(source["id"])
            source_title = str(source.get("title") or source_id)
            rate_limiter.before_query(new_thread=True)
            logging.info(
                "Starting source-intelligence thread %d/%d: %s",
                source_number,
                len(auditor.sources),
                source_title,
            )
            try:
                answer = auditor.start_new_thread(
                    "",
                    SOURCE_INTELLIGENCE_QUERY,
                    source_ids=[source_id],
                )
            except ThreadResetError as exc:
                _log_failure(
                    failure_log,
                    "source_thread_reset",
                    source_id,
                    exc,
                )
                raise
            except Exception as exc:
                failed_queries += 1
                logging.exception(
                    "Source-intelligence query failed for %s; continuing.",
                    source_title,
                )
                _log_failure(failure_log, "source_intelligence", source_id, exc)
                answer = (
                    f"**FAILED:** See `{failure_log.name}` for the recorded error."
                )
            _append_text(
                ledger_path,
                _render_source_intelligence(source_number, source, answer),
            )
        _append_text(ledger_path, _source_intelligence_footer())

        for phase in range(1, 7):
            questions = parse_cluster(cluster_directory / f"cluster_{phase}.csv")
            _append_text(ledger_path, _phase_header(phase))

            for question_index, question in enumerate(questions):
                is_new_phase_thread = question_index == 0
                rate_limiter.before_query(new_thread=is_new_phase_thread)
                logging.info("Auditing question %s.", question["id"])
                try:
                    if is_new_phase_thread:
                        answer = auditor.start_new_thread(
                            MASTER_SYSTEM_PROMPT,
                            _question_prompt(question),
                        )
                    else:
                        answer = auditor.ask_question(
                            "",
                            _question_prompt(question),
                        )
                    _append_text(
                        ledger_path,
                        _render_answer(phase, question, answer),
                    )
                except ThreadResetError as exc:
                    _log_failure(
                        failure_log,
                        "phase_thread_reset",
                        str(phase),
                        exc,
                    )
                    raise
                except Exception as exc:  # Per-question failures must not stop the batch.
                    failed_queries += 1
                    logging.exception("Question %s failed; continuing.", question["id"])
                    _log_failure(
                        failure_log,
                        f"phase_{phase}",
                        str(question["id"]),
                        exc,
                    )
                    _append_text(
                        ledger_path,
                        _render_answer(
                            phase,
                            question,
                            f"**FAILED:** See `{failure_log.name}` for the recorded error.",
                        )
                    )
            _append_text(ledger_path, _phase_footer(phase))

        rate_limiter.before_final_reset()
        try:
            auditor.reset_thread()
        except ThreadResetError as exc:
            _log_failure(failure_log, "final_thread_reset", "phase_6", exc)
            raise

        _set_ledger_status(
            ledger_path,
            "complete" if failed_queries == 0 else "partial",
        )
    except Exception:
        if ledger_initialized:
            _set_ledger_status(ledger_path, "partial")
        raise
    finally:
        auditor.close()


def build_argument_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Run six NotebookLM mathematical-audit clusters."
    )
    parser.add_argument(
        "--pdf",
        action="append",
        type=Path,
        help="PDF to upload when --create-notebook is used. Repeat as needed.",
    )
    parser.add_argument(
        "--notebook",
        default=DEFAULT_NOTEBOOK_ID,
        help=(
            "Existing notebook ID or exact title. Defaults to "
            f"'{DEFAULT_NOTEBOOK_TITLE}' ({DEFAULT_NOTEBOOK_ID})."
        ),
    )
    parser.add_argument(
        "--create-notebook",
        action="store_true",
        help="Create and populate a new notebook instead of using --notebook.",
    )
    parser.add_argument(
        "--notes",
        type=Path,
        help=(
            "Markdown note file or folder to upload. Defaults to the copied "
            "notes/source_snapshots/i2_trap folder containing E_00 and E_01."
        ),
    )
    parser.add_argument(
        "--notebook-name",
        default="Empirical CPR Okishio — Econometric Audit",
    )
    parser.add_argument("--cluster-directory", type=Path)
    parser.add_argument("--ledger-directory", type=Path)
    parser.add_argument(
        "--ledger-file",
        type=Path,
        help=(
            "Canonical Markdown output path. Defaults to "
            f"working_ledgers/notebooklm/{DEFAULT_MASTER_LEDGER}."
        ),
    )
    parser.add_argument("--failure-log", type=Path)
    parser.add_argument("--request-timeout", type=int, default=240)
    parser.add_argument("--source-wait-timeout", type=int, default=600)
    parser.add_argument(
        "--expected-source-count",
        type=int,
        default=DEFAULT_EXPECTED_SOURCE_COUNT,
        help="Abort before resets if the ready source inventory has changed.",
    )
    parser.add_argument("--jitter-min", type=float, default=8.0)
    parser.add_argument("--jitter-max", type=float, default=15.0)
    parser.add_argument("--thread-pause", type=float, default=30.0)
    return parser


def main() -> None:
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s %(levelname)s %(message)s",
    )
    run_audit(build_argument_parser().parse_args())


if __name__ == "__main__":
    main()
