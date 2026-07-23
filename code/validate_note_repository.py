"""Validate note provenance, contracts, and dual-link navigation."""

from __future__ import annotations

import hashlib
import json
import re
import sys
from pathlib import Path
from urllib.parse import unquote


MARKDOWN_LINK_RE = re.compile(r"(?<!!)\[[^\]]+\]\(([^)]+)\)")
WIKILINK_RE = re.compile(r"\[\[([^\]]+)\]\]")
REQUIRED_CONCEPT_FIELDS = {
    "id",
    "type",
    "status",
    "aliases",
    "source_snapshots",
    "audit_phases",
    "audit_questions",
    "last_reviewed",
}
REQUIRED_CONCEPT_SECTIONS = {
    "Formal claim",
    "Assumptions and rank conditions",
    "Proof or theorem evidence",
    "Audit verdict",
    "Required correction",
    "Implementation implications",
    "Unresolved questions",
    "Related notes",
}


def _frontmatter(text: str, path: Path) -> str:
    if not text.startswith("---\n"):
        raise ValueError(f"{path}: missing YAML frontmatter")
    end = text.find("\n---\n", 4)
    if end < 0:
        raise ValueError(f"{path}: unterminated YAML frontmatter")
    return text[4:end]


def _frontmatter_keys(frontmatter: str) -> set[str]:
    return {
        match.group(1)
        for match in re.finditer(r"^([A-Za-z_][A-Za-z0-9_-]*):", frontmatter, re.MULTILINE)
    }


def _aliases(frontmatter: str, path: Path) -> list[str]:
    match = re.search(r"^aliases:\s*(\[.*\])\s*$", frontmatter, re.MULTILINE)
    if not match:
        return []
    try:
        values = json.loads(match.group(1))
    except json.JSONDecodeError as exc:
        raise ValueError(f"{path}: aliases must be a JSON-compatible YAML list") from exc
    return [str(value) for value in values]


def _validate_snapshot_hashes(repo_root: Path) -> list[str]:
    errors: list[str] = []
    snapshot_dir = repo_root / "notes" / "source_snapshots" / "i2_trap"
    manifest_path = snapshot_dir / "manifest.json"
    try:
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        return [f"{manifest_path}: cannot read snapshot manifest: {exc}"]

    if manifest.get("snapshot_policy") != "immutable":
        errors.append(f"{manifest_path}: snapshot_policy must be 'immutable'")
    for entry in manifest.get("files", []):
        path = snapshot_dir / str(entry.get("filename", ""))
        if not path.is_file():
            errors.append(f"{path}: snapshot is missing")
            continue
        actual = hashlib.sha256(path.read_bytes()).hexdigest().upper()
        expected = str(entry.get("sha256", "")).upper()
        if actual != expected:
            errors.append(f"{path}: SHA-256 mismatch; snapshot was modified")
        if not entry.get("original_path") or not entry.get("notebooklm_source_id"):
            errors.append(f"{manifest_path}: incomplete provenance for {path.name}")
    return errors


def _curated_markdown_files(repo_root: Path) -> list[Path]:
    files = [repo_root / "notes" / "_index.md"]
    files.extend(sorted((repo_root / "notes" / "source_intelligence").glob("*.md")))
    files.extend(sorted((repo_root / "concepts").glob("*.md")))
    return [path for path in files if path.is_file() and path.name != ".gitkeep"]


def _validate_local_links(paths: list[Path]) -> list[str]:
    errors: list[str] = []
    target_names: set[str] = set()
    text_by_path: dict[Path, str] = {}

    for path in paths:
        text = path.read_text(encoding="utf-8")
        text_by_path[path] = text
        target_names.add(path.stem.casefold())
        frontmatter = _frontmatter(text, path)
        target_names.update(alias.casefold() for alias in _aliases(frontmatter, path))

    # Immutable snapshots are valid wikilink targets but are not curated here.
    snapshot_dir = paths[0].parents[0] / "source_snapshots" / "i2_trap"
    target_names.update(path.stem.casefold() for path in snapshot_dir.glob("*.md"))

    for path, text in text_by_path.items():
        current_section = ""
        for line_number, line in enumerate(text.splitlines(), start=1):
            if line.startswith("## "):
                current_section = line[3:].strip()

            for raw_target in MARKDOWN_LINK_RE.findall(line):
                target = raw_target.strip().strip("<>")
                if (
                    not target
                    or target.startswith(("#", "http://", "https://", "mailto:"))
                ):
                    continue
                target = unquote(target.split("#", 1)[0])
                resolved = (path.parent / target).resolve()
                if not resolved.exists():
                    errors.append(
                        f"{path}:{line_number}: broken Markdown link: {raw_target}"
                    )

            wikilinks = WIKILINK_RE.findall(line)
            if wikilinks and not current_section.lower().startswith("related"):
                errors.append(
                    f"{path}:{line_number}: wikilinks are allowed only in Related sections"
                )
            for raw_target in wikilinks:
                target = raw_target.split("|", 1)[0].split("#", 1)[0].strip().casefold()
                if target not in target_names:
                    errors.append(
                        f"{path}:{line_number}: unresolved wikilink: [[{raw_target}]]"
                    )
            if (
                current_section.lower().startswith("related")
                and ".md)" in line
                and not wikilinks
            ):
                errors.append(
                    f"{path}:{line_number}: related Markdown note link lacks a wikilink"
                )
    return errors


def _validate_concept_contracts(repo_root: Path) -> list[str]:
    errors: list[str] = []
    concept_paths = sorted((repo_root / "concepts").glob("*.md"))
    concept_paths = [path for path in concept_paths if path.name != ".gitkeep"]
    if len(concept_paths) != 6:
        errors.append(f"Expected 6 canonical concept notes; found {len(concept_paths)}")

    for path in concept_paths:
        text = path.read_text(encoding="utf-8")
        frontmatter = _frontmatter(text, path)
        missing_fields = REQUIRED_CONCEPT_FIELDS - _frontmatter_keys(frontmatter)
        if missing_fields:
            errors.append(f"{path}: missing fields: {sorted(missing_fields)}")
        audit_match = re.search(
            r"^audit_questions:\s*\[(.*?)\]\s*$",
            frontmatter,
            re.MULTILINE,
        )
        if not audit_match or not audit_match.group(1).strip():
            errors.append(f"{path}: audit_questions must contain at least one ID")
        if "../notes/source_intelligence/" not in text:
            errors.append(f"{path}: must cite at least one source-intelligence note")

        sections = {
            match.group(1).strip()
            for match in re.finditer(r"^## (.+)$", text, re.MULTILINE)
        }
        missing_sections = REQUIRED_CONCEPT_SECTIONS - sections
        if missing_sections:
            errors.append(f"{path}: missing sections: {sorted(missing_sections)}")
    return errors


def _validate_source_inventory(repo_root: Path) -> list[str]:
    paths = sorted((repo_root / "notes" / "source_intelligence").glob("*.md"))
    errors: list[str] = []
    if len(paths) != 14:
        errors.append(f"Expected 14 source-intelligence dossiers; found {len(paths)}")

    source_ids: set[str] = set()
    for path in paths:
        text = path.read_text(encoding="utf-8")
        frontmatter = _frontmatter(text, path)
        match = re.search(
            r'^notebook_source_id:\s*"([^"]+)"\s*$',
            frontmatter,
            re.MULTILINE,
        )
        if not match:
            errors.append(f"{path}: missing notebook_source_id")
            continue
        source_id = match.group(1)
        if source_id in source_ids:
            errors.append(f"{path}: duplicate notebook_source_id {source_id}")
        source_ids.add(source_id)
    return errors


def validate_repository(repo_root: Path) -> list[str]:
    repo_root = repo_root.resolve()
    curated_paths = _curated_markdown_files(repo_root)
    errors: list[str] = []
    errors.extend(_validate_snapshot_hashes(repo_root))
    errors.extend(_validate_source_inventory(repo_root))
    errors.extend(_validate_concept_contracts(repo_root))
    errors.extend(_validate_local_links(curated_paths))
    return errors


def main() -> None:
    repo_root = Path(__file__).resolve().parents[1]
    errors = validate_repository(repo_root)
    if errors:
        for error in errors:
            print(f"ERROR: {error}", file=sys.stderr)
        raise SystemExit(1)
    print("Note repository validation passed.")


if __name__ == "__main__":
    main()
