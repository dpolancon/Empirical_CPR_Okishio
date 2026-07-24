---
schema_version: 2
id: "note-schema"
title: "Knowledge Note Schema"
type: "knowledge-index"
status: "validated"
aliases: ["YAML Contract", "Schema v2"]
tags: ["metadata", "validation"]
created: "2026-07-23"
updated: "2026-07-24"
last_reviewed: "2026-07-24"
contains: []
---
# Knowledge Note Schema

Every editable Markdown note under `03B_econometrics_validation/` uses schema version 2. Immutable
snapshots and the append-only NotebookLM ledger are governed by JSON manifests
instead, so their bytes do not change.

## Common fields

`id`, `title`, `type`, `status`, `aliases`, `tags`, `created`, `updated`, and
`last_reviewed` are mandatory. Editable filenames equal their IDs. IDs,
aliases, and references are globally unique after case folding.

## Markdown and math

Use ATX headings (`#`, `##`, and `###`) to make each argument navigable in
Obsidian. Write inline mathematics as `$x_t$` and displayed mathematics as a
standalone `$$` block. Do not use backslash-parenthesis or backslash-bracket
delimiters in editable notes. Keep equations inside the Markdown note body rather than
images, so links, search, and graph navigation remain useful.

## Type contracts

- `concept`: `source_snapshots`, `source_dossiers`, `audit_questions`,
  `theory_tasks`.
- `source-dossier`: `source_channel`, `publication_status`, `citation_key`,
  `doi`, `notebooklm_source_id`, `reviewed`, `audit_questions`.
- `theory-task`: `sequence`, `depends_on`, `resolves_concepts`,
  `source_dossiers`, `audit_questions`, `proof_status`, `simulation_status`,
  `outcome`, `mathematical_status`, `scholarly_status`, and
  `finite_sample_status`.
- `validation-report`: `source_snapshots`, `audit_questions`, `theory_tasks`,
  and `concepts`.
- `knowledge-index`: `contains`.

## Status and outcome rules

Editable knowledge uses `under-review`, `validated`, `disputed`, or `excluded`.
Theory tasks use `open`, `in-progress`, `resolved`, or `blocked`; their outcome
is `proved`, `refuted`, `qualified`, or `null`.

The independent mathematical status is `open`, `locally-proved`,
`locally-qualified`, or `locally-refuted`. Scholarly status is
`awaiting-peer-review` or `peer-reviewed`. `finite_sample_status` must contain
the `t50` and `t100` anchors, each classified as `unsupported`, `diagnostic`,
`usable`, or `robust`. A smoke run cannot promote any of these fields.

## Related navigation

- [Knowledge Index](../knowledge-index.md) · [[knowledge-index|Knowledge Index]]
