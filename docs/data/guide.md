# Data Guide

The canonical list of every table and field in the system. Empty until v0.0 introduces the first schema — the `doc-writer` subagent adds a section here whenever a feature introduces or changes a table.

## Format for each entry

```
## table_name

Purpose: one line.

| Column | Type | Description |
|---|---|---|
| id | uuid | ... |

Relationships: ...

Added by: [feature doc](../features/<slug>.md)
```
