"""Validate provenance, schema-v2 contracts, graph integrity, and navigation."""

from __future__ import annotations

import csv
import hashlib
import json
import re
import sys
import tempfile
from pathlib import Path
from urllib.parse import unquote

import yaml

from cluster_parser import parse_all_clusters
from partition_audit_ledger import partition_ledger


MARKDOWN_LINK_RE = re.compile(r"(?<!!)\[[^\]]+\]\(([^)]+)\)")
WIKILINK_RE = re.compile(r"\[\[([^\]]+)\]\]")
ID_RE = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
LEGACY_MATH_DELIMITER_RE = re.compile(r"\\(?:\(|\)|\[|\])")
COMMON_FIELDS = {
    "schema_version",
    "id",
    "title",
    "type",
    "status",
    "aliases",
    "tags",
    "created",
    "updated",
    "last_reviewed",
}
TYPE_FIELDS = {
    "concept": {
        "source_snapshots",
        "source_dossiers",
        "audit_questions",
        "theory_tasks",
    },
    "source-dossier": {
        "source_channel",
        "publication_status",
        "citation_key",
        "doi",
        "notebooklm_source_id",
        "reviewed",
        "audit_questions",
    },
    "theory-task": {
        "sequence",
        "depends_on",
        "resolves_concepts",
        "source_dossiers",
        "audit_questions",
        "proof_status",
        "simulation_status",
        "outcome",
        "mathematical_status",
        "scholarly_status",
        "finite_sample_status",
    },
    "validation-report": {
        "source_snapshots",
        "audit_questions",
        "theory_tasks",
        "concepts",
    },
    "knowledge-index": {"contains"},
}
KNOWLEDGE_STATUSES = {"under-review", "validated", "disputed", "excluded"}
THEORY_STATUSES = {"open", "in-progress", "resolved", "blocked"}
THEORY_OUTCOMES = {None, "proved", "refuted", "qualified"}
MATHEMATICAL_STATUSES = {
    "open",
    "locally-proved",
    "locally-qualified",
    "locally-refuted",
}
SCHOLARLY_STATUSES = {"awaiting-peer-review", "peer-reviewed"}
FINITE_SAMPLE_STATUSES = {"unsupported", "diagnostic", "usable", "robust"}
CONCEPT_SECTIONS = {
    "Formal claim",
    "Assumptions and rank conditions",
    "Proof or theorem evidence",
    "Audit verdict",
    "Required correction",
    "Implementation implications",
    "Unresolved questions",
    "Related notes",
}
THEORY_SECTIONS = {
    "Formal setup",
    "Assumptions",
    "Lemmas",
    "Derivation",
    "Rank conditions",
    "Degenerate cases",
    "Peer-reviewed evidence",
    "Simulation design",
    "Results",
    "Verdict",
    "Concept-note implications",
    "Remaining gaps",
    "Related notes",
}
VALIDATION_REPORT_SECTIONS = {
    "Current bottom line",
    "What is being validated",
    "Evidence ladder",
    "Step-by-step validation",
    "Claim disposition",
    "Operational decision sequence",
    "Reproducing the validation",
    "Review checklist",
    "Related notes",
}
EXCLUDED_SOURCE_ID = "industrial-policy-beyond-hegemons"
VAULT_DIRECTORY = "03B_econometrics_validation"


def _sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest().upper()


def _split_frontmatter(text: str, path: Path) -> tuple[dict, str]:
    match = re.match(r"^---\r?\n(.*?)\r?\n---\r?\n(.*)$", text, re.DOTALL)
    if not match:
        raise ValueError(f"{path}: missing or unterminated YAML frontmatter")
    data = yaml.safe_load(match.group(1))
    if not isinstance(data, dict):
        raise ValueError(f"{path}: YAML frontmatter must be a mapping")
    return data, match.group(2)


def _editable_markdown_files(repo_root: Path) -> list[Path]:
    knowledge = repo_root / VAULT_DIRECTORY
    paths: list[Path] = []
    for path in knowledge.rglob("*.md"):
        relative = path.relative_to(knowledge)
        if relative.parts[:2] in {
            ("sources", "snapshots"),
            ("evidence", "notebooklm"),
        }:
            continue
        paths.append(path)
    return sorted(paths)


def _load_notes(paths: list[Path]) -> tuple[dict[str, tuple[Path, dict, str]], list[str]]:
    notes: dict[str, tuple[Path, dict, str]] = {}
    token_owner: dict[str, str] = {}
    errors: list[str] = []
    for path in paths:
        try:
            data, body = _split_frontmatter(path.read_text(encoding="utf-8"), path)
        except (OSError, ValueError, yaml.YAMLError) as exc:
            errors.append(str(exc))
            continue
        if LEGACY_MATH_DELIMITER_RE.search(body):
            errors.append(
                f"{path}: use $...$ or $$...$$ instead of legacy LaTex delimiters"
            )
        missing = COMMON_FIELDS - set(data)
        note_type = data.get("type")
        if note_type not in TYPE_FIELDS:
            errors.append(f"{path}: unsupported type {note_type!r}")
            required = set()
        else:
            required = TYPE_FIELDS[note_type]
        missing.update(required - set(data))
        if missing:
            errors.append(f"{path}: missing fields: {sorted(missing)}")

        note_id = str(data.get("id", ""))
        if not ID_RE.fullmatch(note_id):
            errors.append(f"{path}: invalid kebab-case id {note_id!r}")
        if path.stem != note_id:
            errors.append(f"{path}: filename stem must equal id {note_id!r}")
        if data.get("schema_version") != 2:
            errors.append(f"{path}: schema_version must be numeric 2")
        if note_id in notes:
            errors.append(f"{path}: duplicate id {note_id}")
        notes[note_id] = (path, data, body)

        status = data.get("status")
        allowed_statuses = THEORY_STATUSES if note_type == "theory-task" else KNOWLEDGE_STATUSES
        if status not in allowed_statuses:
            errors.append(f"{path}: invalid status {status!r} for {note_type}")

        aliases = data.get("aliases")
        if not isinstance(aliases, list):
            errors.append(f"{path}: aliases must be a list")
            aliases = []
        for token in [note_id, *[str(alias) for alias in aliases]]:
            folded = token.casefold()
            owner = token_owner.get(folded)
            if owner is not None and owner != note_id:
                errors.append(
                    f"{path}: id/alias {token!r} collides with note {owner!r}"
                )
            token_owner[folded] = note_id
    return notes, errors


def _validate_manifests(repo_root: Path) -> list[str]:
    errors: list[str] = []
    snapshot_dir = repo_root / VAULT_DIRECTORY / "sources" / "snapshots" / "i2-trap"
    snapshot_manifest_path = snapshot_dir / "manifest.json"
    evidence_manifest_path = repo_root / VAULT_DIRECTORY / "_meta" / "evidence-manifest.json"
    migration_path = repo_root / VAULT_DIRECTORY / "_meta" / "path-migration.json"
    try:
        snapshot_manifest = json.loads(snapshot_manifest_path.read_text(encoding="utf-8"))
        evidence_manifest = json.loads(evidence_manifest_path.read_text(encoding="utf-8"))
        migration = json.loads(migration_path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        return [f"Cannot read a provenance manifest: {exc}"]

    if snapshot_manifest.get("snapshot_policy") != "immutable":
        errors.append(f"{snapshot_manifest_path}: snapshot_policy must be immutable")
    for entry in snapshot_manifest.get("files", []):
        path = snapshot_dir / str(entry.get("filename", ""))
        if not path.is_file():
            errors.append(f"{path}: snapshot is missing")
            continue
        if _sha256(path) != str(entry.get("sha256", "")).upper():
            errors.append(f"{path}: SHA-256 mismatch")
        required = {
            "original_filename",
            "original_path",
            "previous_repository_path",
            "repository_path",
            "notebooklm_source_id",
        }
        if any(not entry.get(field) for field in required):
            errors.append(f"{snapshot_manifest_path}: incomplete provenance for {path.name}")

    for entry in evidence_manifest.get("artifacts", []):
        path = repo_root / str(entry.get("repository_path", ""))
        if not path.is_file():
            errors.append(f"{path}: evidence artifact is missing")
        elif _sha256(path) != str(entry.get("sha256", "")).upper():
            errors.append(f"{path}: append-only evidence hash mismatch")

    for old, new in migration.get("mappings", {}).items():
        old_path = repo_root / old.rstrip("/")
        new_path = repo_root / new.rstrip("/")
        if old_path.exists():
            errors.append(f"{old_path}: stale pre-migration path still exists")
        if not new_path.exists():
            errors.append(f"{new_path}: migration target is missing")
    return errors


def _validate_graph(
    repo_root: Path,
    notes: dict[str, tuple[Path, dict, str]],
) -> list[str]:
    errors: list[str] = []
    question_dir = repo_root / VAULT_DIRECTORY / "evidence" / "notebooklm" / "questions"
    valid_questions = {
        str(question["id"]) for question in parse_all_clusters(question_dir)
    }
    snapshot_ids = {"e-00-i2-trap", "e-01-i2-trap"}
    references = {
        "source_snapshots": snapshot_ids,
        "source_dossiers": {
            note_id
            for note_id, (_, data, _) in notes.items()
            if data.get("type") == "source-dossier" and data.get("status") != "excluded"
        },
        "theory_tasks": {
            note_id
            for note_id, (_, data, _) in notes.items()
            if data.get("type") == "theory-task"
        },
        "depends_on": {
            note_id
            for note_id, (_, data, _) in notes.items()
            if data.get("type") == "theory-task"
        },
        "resolves_concepts": {
            note_id
            for note_id, (_, data, _) in notes.items()
            if data.get("type") == "concept"
        },
        "concepts": {
            note_id
            for note_id, (_, data, _) in notes.items()
            if data.get("type") == "concept"
        },
        "contains": set(notes) - {EXCLUDED_SOURCE_ID},
    }

    for note_id, (path, data, body) in notes.items():
        for field, allowed in references.items():
            if field not in data:
                continue
            value = data[field]
            if not isinstance(value, list):
                errors.append(f"{path}: {field} must be a list")
                continue
            for target in value:
                if target not in allowed:
                    errors.append(f"{path}: unresolved or prohibited {field} id {target!r}")
        if "audit_questions" in data:
            questions = data["audit_questions"]
            if not isinstance(questions, list):
                errors.append(f"{path}: audit_questions must be a list")
            for question in questions if isinstance(questions, list) else []:
                if str(question) not in valid_questions:
                    errors.append(f"{path}: unknown audit question {question!r}")

        note_type = data.get("type")
        sections = set(re.findall(r"^## (.+)$", body, re.MULTILINE))
        if note_type == "concept":
            missing = CONCEPT_SECTIONS - sections
            if missing:
                errors.append(f"{path}: missing concept sections: {sorted(missing)}")
            for field in ("source_dossiers", "audit_questions", "theory_tasks"):
                if not data.get(field):
                    errors.append(f"{path}: {field} must not be empty")
            if data.get("status") == "validated":
                for task_id in data.get("theory_tasks", []):
                    task = notes.get(task_id)
                    if (
                        task is None
                        or task[1].get("status") != "resolved"
                        or task[1].get("scholarly_status") != "peer-reviewed"
                    ):
                        errors.append(
                            f"{path}: validated concept depends on unresolved task {task_id}"
                        )
        elif note_type == "theory-task":
            missing = THEORY_SECTIONS - sections
            if missing:
                errors.append(f"{path}: missing theory sections: {sorted(missing)}")
            if data.get("outcome") not in THEORY_OUTCOMES:
                errors.append(f"{path}: invalid theory outcome {data.get('outcome')!r}")
            if data.get("mathematical_status") not in MATHEMATICAL_STATUSES:
                errors.append(
                    f"{path}: invalid mathematical_status "
                    f"{data.get('mathematical_status')!r}"
                )
            if data.get("scholarly_status") not in SCHOLARLY_STATUSES:
                errors.append(
                    f"{path}: invalid scholarly_status "
                    f"{data.get('scholarly_status')!r}"
                )
            finite_status = data.get("finite_sample_status")
            if not isinstance(finite_status, dict) or set(finite_status) != {
                "t50",
                "t100",
            }:
                errors.append(
                    f"{path}: finite_sample_status must contain exactly t50 and t100"
                )
            elif any(
                value not in FINITE_SAMPLE_STATUSES
                for value in finite_status.values()
            ):
                errors.append(f"{path}: invalid finite_sample_status value")
            if data.get("status") == "resolved" and (
                data.get("proof_status") != "passed"
                or data.get("simulation_status") != "passed"
                or data.get("outcome") not in {"proved", "refuted", "qualified"}
                or data.get("scholarly_status") != "peer-reviewed"
            ):
                errors.append(f"{path}: resolved task has not passed all closure gates")
            if (
                data.get("mathematical_status")
                in {"locally-proved", "locally-qualified"}
                and data.get("simulation_status") not in {"passed", "diagnostic-passed"}
            ):
                errors.append(
                    f"{path}: locally closed mathematical status lacks passing simulations"
                )
        elif note_type == "source-dossier":
            source_id = data.get("notebooklm_source_id")
            if data.get("source_channel") == "notebooklm" and not source_id:
                errors.append(f"{path}: NotebookLM dossier lacks notebooklm_source_id")
            if data.get("status") == "excluded" and data.get("audit_questions"):
                errors.append(f"{path}: excluded source must have no audit questions")
        elif note_type == "validation-report":
            missing = VALIDATION_REPORT_SECTIONS - sections
            if missing:
                errors.append(
                    f"{path}: missing validation-report sections: {sorted(missing)}"
                )
            for field in (
                "source_snapshots",
                "audit_questions",
                "theory_tasks",
                "concepts",
            ):
                if not data.get(field):
                    errors.append(f"{path}: {field} must not be empty")
            if data.get("status") == "validated":
                for task_id in data.get("theory_tasks", []):
                    task = notes.get(task_id)
                    if (
                        task is None
                        or task[1].get("status") != "resolved"
                        or task[1].get("scholarly_status") != "peer-reviewed"
                    ):
                        errors.append(
                            f"{path}: validated report depends on unresolved task {task_id}"
                        )

        serialized = json.dumps(data, ensure_ascii=False)
        if note_id != EXCLUDED_SOURCE_ID and EXCLUDED_SOURCE_ID in serialized:
            errors.append(f"{path}: active metadata references excluded industrial source")

    source_index = notes.get("source-index")
    if source_index and EXCLUDED_SOURCE_ID in source_index[1].get("contains", []):
        errors.append("source-index: industrial-policy source cannot be active")

    expected_by_index = {
        "source-index": {
            note_id
            for note_id, (_, data, _) in notes.items()
            if data.get("type") == "source-dossier" and data.get("status") != "excluded"
        },
        "concept-index": {
            note_id
            for note_id, (_, data, _) in notes.items()
            if data.get("type") == "concept"
        },
        "theory-index": {
            note_id
            for note_id, (_, data, _) in notes.items()
            if data.get("type") == "theory-task"
        },
    }
    for index_id, expected in expected_by_index.items():
        index = notes.get(index_id)
        if index is None:
            errors.append(f"Missing required index {index_id}")
            continue
        actual = set(index[1].get("contains", []))
        if actual != expected:
            errors.append(
                f"{index[0]}: contains differs from discovered notes; "
                f"missing={sorted(expected - actual)}, extra={sorted(actual - expected)}"
            )

    notebook_source_owners: dict[str, str] = {}
    for note_id, (path, data, _) in notes.items():
        source_id = data.get("notebooklm_source_id")
        if not source_id:
            continue
        owner = notebook_source_owners.get(str(source_id))
        if owner is not None:
            errors.append(
                f"{path}: duplicate notebooklm_source_id shared with {owner}"
            )
        notebook_source_owners[str(source_id)] = note_id

    # Dependency DAG cycle detection.
    dependencies = {
        note_id: list(data.get("depends_on", []))
        for note_id, (_, data, _) in notes.items()
        if data.get("type") == "theory-task"
    }
    visiting: set[str] = set()
    visited: set[str] = set()

    def visit(node: str) -> None:
        if node in visiting:
            errors.append(f"Theory dependency cycle detected at {node}")
            return
        if node in visited:
            return
        visiting.add(node)
        for dependency in dependencies.get(node, []):
            visit(dependency)
        visiting.remove(node)
        visited.add(node)

    for task_id in dependencies:
        visit(task_id)
    return errors


def _validate_links(
    notes: dict[str, tuple[Path, dict, str]],
    repo_root: Path,
) -> list[str]:
    errors: list[str] = []
    wiki_targets: dict[str, str] = {}
    for note_id, (_, data, _) in notes.items():
        wiki_targets[note_id.casefold()] = note_id
        for alias in data.get("aliases", []):
            wiki_targets[str(alias).casefold()] = note_id
    for snapshot in ("e-00-i2-trap", "e-01-i2-trap"):
        wiki_targets[snapshot] = snapshot

    editable_paths = {path.resolve() for path, _, _ in notes.values()}
    snapshot_paths = {
        (repo_root / VAULT_DIRECTORY / "sources" / "snapshots" / "i2-trap" / f"{stem}.md").resolve()
        for stem in ("e-00-i2-trap", "e-01-i2-trap")
    }
    note_paths = editable_paths | snapshot_paths

    for path, _, body in notes.values():
        current_section = ""
        for line_number, line in enumerate(body.splitlines(), start=1):
            if line.startswith("## "):
                current_section = line[3:].strip()
            wikilinks = WIKILINK_RE.findall(line)
            if wikilinks and not current_section.casefold().startswith("related"):
                errors.append(
                    f"{path}:{line_number}: wikilinks are allowed only in Related sections"
                )
            wiki_ids = {
                item.split("|", 1)[0].split("#", 1)[0].strip().casefold()
                for item in wikilinks
            }
            for target in wiki_ids:
                if target not in wiki_targets:
                    errors.append(f"{path}:{line_number}: unresolved wikilink [[{target}]]")

            for raw_target in MARKDOWN_LINK_RE.findall(line):
                target = raw_target.strip().strip("<>")
                if not target or target.startswith(("#", "http://", "https://", "mailto:")):
                    continue
                target = unquote(target.split("#", 1)[0])
                resolved = (path.parent / target).resolve()
                if not resolved.exists():
                    errors.append(f"{path}:{line_number}: broken Markdown link {raw_target}")
                    continue
                if resolved in note_paths:
                    expected = resolved.stem.casefold()
                    if expected not in wiki_ids:
                        errors.append(
                            f"{path}:{line_number}: note link lacks matching wikilink [[{resolved.stem}]]"
                        )
    return errors


def _validate_ledger_and_views(repo_root: Path) -> list[str]:
    errors: list[str] = []
    master = (
        repo_root
        / VAULT_DIRECTORY
        / "evidence"
        / "notebooklm"
        / "econometric-audit-master.md"
    )
    text = master.read_text(encoding="utf-8")
    if not re.search(r"^status:\s*complete\s*$", text, re.MULTILINE):
        errors.append(f"{master}: status is not complete")
    source_count = len(re.findall(r"<!-- SOURCE_INTELLIGENCE_ITEM_START ", text))
    question_count = len(re.findall(r"<!-- AUDIT_QUESTION_START ", text))
    if source_count != 13:
        errors.append(f"{master}: expected 13 source responses; found {source_count}")
    if question_count != 18:
        errors.append(f"{master}: expected 18 audit answers; found {question_count}")
    if "**FAILED:**" in text:
        errors.append(f"{master}: contains failed-query markers")
    if EXCLUDED_SOURCE_ID in text:
        errors.append(f"{master}: contains active industrial-policy source ID")

    with tempfile.TemporaryDirectory(prefix="cpr-audit-views-") as temporary:
        written = partition_ledger(master, Path(temporary))
        if len(written) != 7 or len(list(Path(temporary).glob("*.md"))) != 7:
            errors.append("Master ledger did not regenerate exactly seven views")

    gitignore = (repo_root / ".gitignore").read_text(encoding="utf-8")
    for ignored in (
        "/03B_econometrics_validation/evidence/notebooklm/views/",
        "/03B_econometrics_validation/evidence/notebooklm/attempts/",
        "/03B_econometrics_validation/theory/results/raw/",
    ):
        if ignored not in gitignore:
            errors.append(f".gitignore: missing {ignored}")
    return errors


def _read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(encoding="utf-8", newline="") as source:
        return list(csv.DictReader(source))


def _validate_theory_results(repo_root: Path) -> list[str]:
    errors: list[str] = []
    result_dir = repo_root / VAULT_DIRECTORY / "theory" / "results"
    manifest_path = result_dir / "run-manifest.json"
    try:
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        return [f"{manifest_path}: cannot read theory result manifest: {exc}"]
    if manifest.get("schema_version") != 2:
        errors.append(f"{manifest_path}: expected result schema version 2")
    if manifest.get("seed") != 20260723:
        errors.append(f"{manifest_path}: unexpected simulation seed")
    expected_sizes = [40, 50, 60, 80, 100, 120, 200, 500, 1000]
    if manifest.get("sample_sizes") != expected_sizes:
        errors.append(f"{manifest_path}: unexpected sample-size design")
    profile = manifest.get("profile")
    if profile not in {"smoke", "full"}:
        errors.append(f"{manifest_path}: invalid profile {profile!r}")
    if profile == "smoke":
        if manifest.get("replications") != 250 or manifest.get("limit_draws") != 5000:
            errors.append(f"{manifest_path}: noncanonical smoke profile")
        if manifest.get("bootstrap_replications") != {
            "small_samples": 99,
            "asymptotic": 99,
        }:
            errors.append(f"{manifest_path}: smoke profile requires 99 bootstrap draws")
        if not str(manifest.get("calibration_status", "")).startswith("smoke-only"):
            errors.append(f"{manifest_path}: smoke run must be marked non-promotional")
    elif profile == "full":
        if manifest.get("replications") != 10_000:
            errors.append(f"{manifest_path}: full profile requires 10000 replications")
        if manifest.get("limit_draws") != 200_000:
            errors.append(f"{manifest_path}: full profile requires 200000 limit draws")

    for artifact in manifest.get("artifacts", []):
        path = result_dir / str(artifact)
        if not path.is_file() or not path.stat().st_size:
            errors.append(f"{path}: theory artifact missing or empty")

    tasks = set(manifest.get("tasks", []))
    required_by_task = {
        "t03": {
            "t03-fixed-b-critical-values.json",
            "t03-imols-summary.csv",
            "t03-rate-checks.csv",
            "t03-rank-diagnostics.csv",
            "t03-naive-estimator-diagnostic.csv",
        },
        "t05": {
            "t05-critical-values.csv",
            "t05-size-power.csv",
            "t05-residual-scaling-summary.csv",
            "t05-residual-rate-checks.csv",
        },
        "t06": {
            "t06-fixed-state-inference.csv",
            "t06-path-band-coverage.csv",
            "t06-efficiency-wald.csv",
            "t06-i0-diagnostic.csv",
        },
    }
    artifact_names = set(manifest.get("artifacts", []))
    for task, required in required_by_task.items():
        if task in tasks and not required <= artifact_names:
            errors.append(
                f"{manifest_path}: {task} missing artifacts "
                f"{sorted(required - artifact_names)}"
            )

    fwl_path = result_dir / "t04-fwl-check.json"
    if fwl_path.is_file():
        fwl = json.loads(fwl_path.read_text(encoding="utf-8"))
        if not fwl.get("fwl_identity_passes") or not fwl.get("noncommutation_detected"):
            errors.append(f"{fwl_path}: FWL algebra checks failed")

    if "t03" in tasks:
        estimator_path = result_dir / "t03-imols-summary.csv"
        estimator_rows = _read_csv(estimator_path)
        anchors = {
            int(row["sample_size"])
            for row in estimator_rows
            if row.get("method") == "moving-block-bootstrap"
        }
        if not set(expected_sizes) <= anchors:
            errors.append(f"{estimator_path}: bootstrap sample grid is incomplete")
        if profile == "smoke" and any(
            int(row["successful_replications"]) != 250
            for row in estimator_rows
            if row.get("method") == "moving-block-bootstrap"
        ):
            errors.append(f"{estimator_path}: smoke bootstrap requires 250 outer draws")
        diagnostic_rows = _read_csv(result_dir / "t03-rank-diagnostics.csv")
        singular = [
            row
            for row in diagnostic_rows
            if row["scenario"] == "singular-common-trend"
        ]
        if not singular or any(float(row["rank_supported_rate"]) > 0 for row in singular):
            errors.append(f"{result_dir / 't03-rank-diagnostics.csv'}: singular rank gate failed")

    if "t05" in tasks:
        test_rows = _read_csv(result_dir / "t05-size-power.csv")
        for anchor in expected_sizes:
            methods = {
                row["method"]
                for row in test_rows
                if int(row["sample_size"]) == anchor
                and row["experiment"] == "null-size"
            }
            if methods != {"fixed-b", "moving-block-bootstrap"}:
                errors.append(
                    f"{result_dir / 't05-size-power.csv'}: missing null calibrations at T={anchor}"
                )
        if profile == "smoke" and any(
            int(row["replications"]) != 250
            for row in test_rows
            if row["method"] == "moving-block-bootstrap"
            and row["experiment"] == "null-size"
        ):
            errors.append("T05 smoke bootstrap requires 250 outer draws")

    if "t06" in tasks:
        state_rows = _read_csv(result_dir / "t06-fixed-state-inference.csv")
        targets = {row["target"] for row in state_rows}
        if targets != {"theta", "gap"}:
            errors.append(
                f"{result_dir / 't06-fixed-state-inference.csv'}: corrected targets missing"
            )
        if profile == "smoke" and any(
            int(row["replications"]) != 250
            for row in state_rows
            if row["method"] == "moving-block-bootstrap"
        ):
            errors.append("T06 smoke bootstrap requires 250 outer draws")
        bootstrap_sizes = {
            int(row["sample_size"])
            for row in state_rows
            if row["method"] == "moving-block-bootstrap"
        }
        if not set(expected_sizes) <= bootstrap_sizes:
            errors.append("T06 bootstrap sample grid is incomplete")
        path_rows = _read_csv(result_dir / "t06-path-band-coverage.csv")
        methods = {row["method"] for row in path_rows}
        if not {
            "conditional-path-band",
            "unconditional-path-band",
        } <= methods:
            errors.append(
                f"{result_dir / 't06-path-band-coverage.csv'}: path bands missing"
            )
        for method in ("conditional-path-band", "unconditional-path-band"):
            sizes = {
                int(row["sample_size"])
                for row in path_rows
                if row["method"] == method
            }
            if not set(expected_sizes) <= sizes:
                errors.append(f"T06 {method} sample grid is incomplete")

    if profile == "full":
        if "t03" in tasks:
            rows = _read_csv(result_dir / "t03-imols-summary.csv")
            gated = [
                row
                for row in rows
                if row["scenario"] == "rho-0.5-ar-0.5"
                and int(row["sample_size"]) >= 500
            ]
            if any(
                not 0.93 <= float(row["coverage_95"]) <= 0.97
                for row in gated
            ):
                errors.append("T03 full-profile asymptotic coverage gate failed")
        if "t05" in tasks:
            rows = _read_csv(result_dir / "t05-size-power.csv")
            gated = [
                row
                for row in rows
                if row["experiment"] == "null-size"
                and int(row["sample_size"]) >= 500
            ]
            if any(
                not 0.03 <= float(row["rejection_rate"]) <= 0.07
                for row in gated
            ):
                errors.append("T05 full-profile asymptotic size gate failed")
        if "t06" in tasks:
            rows = _read_csv(result_dir / "t06-fixed-state-inference.csv")
            gated = [row for row in rows if int(row["sample_size"]) >= 500]
            if any(
                not 0.93 <= float(row["coverage_95"]) <= 0.97
                for row in gated
            ):
                errors.append("T06 full-profile asymptotic coverage gate failed")
    return errors


def validate_repository(repo_root: Path) -> list[str]:
    repo_root = repo_root.resolve()
    paths = _editable_markdown_files(repo_root)
    notes, errors = _load_notes(paths)
    errors.extend(_validate_manifests(repo_root))
    errors.extend(_validate_graph(repo_root, notes))
    errors.extend(_validate_links(notes, repo_root))
    errors.extend(_validate_ledger_and_views(repo_root))
    errors.extend(_validate_theory_results(repo_root))
    return errors


def main() -> None:
    repo_root = Path(__file__).resolve().parents[1]
    errors = validate_repository(repo_root)
    if errors:
        for error in errors:
            print(f"ERROR: {error}", file=sys.stderr)
        raise SystemExit(1)
    print("Knowledge repository validation passed.")


if __name__ == "__main__":
    main()
