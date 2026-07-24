---
schema_version: 2
id: "note-schema"
title: "Knowledge Note Schema"
type: "knowledge-index"
status: "validated"
aliases: ["YAML Contract", "Schema v2"]
tags: ["metadata", "validation"]
created: "2026-07-23"
updated: "2026-07-23"
last_reviewed: "2026-07-23"
contains: []
---
# Knowledge Note Schema

Every editable Markdown note under `knowledge/` uses schema version 2. Immutable
snapshots and the append-only NotebookLM ledger are governed by JSON manifests
instead, so their bytes do not change.

## Common fields

`id`, `title`, `type`, `status`, `aliases`, `tags`, `created`, `updated`, and
`last_reviewed` are mandatory. Editable filenames equal their IDs. IDs,
aliases, and references are globally unique after case folding.

## Type contracts

- `concept`: `source_snapshots`, `source_dossiers`, `audit_questions`,
  `theory_tasks`.
- `source-dossier`: `source_channel`, `publication_status`, `citation_key`,
  `doi`, `notebooklm_source_id`, `reviewed`, `audit_questions`.
- `theory-task`: `sequence`, `depends_on`, `resolves_concepts`,
  `source_dossiers`, `audit_questions`, `proof_status`, `simulation_status`,
  `outcome`.
- `knowledge-index`: `contains`.

## Status and outcome rules

Editable knowledge uses `under-review`, `validated`, `disputed`, or `excluded`.
Theory tasks use `open`, `in-progress`, `resolved`, or `blocked`; their outcome
is `proved`, `refuted`, `qualified`, or `null`.

## Related navigation

- [Knowledge Index](../knowledge-index.md) · [[knowledge-index|Knowledge Index]]
