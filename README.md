# Momoi Labs Skills

Personal Agent Skills and workflow wrappers used across Codex and other
Agent Skills-compatible clients.

## Prerequisite

Some skills in this repository wrap workflows maintained in
[`mattpocock/skills`](https://github.com/mattpocock/skills):

| Skill | Upstream dependency |
| --- | --- |
| `my-handoff` | `handoff` |
| `my-implement` | `implement` and its upstream workflow |
| `my-to-tickets` | `to-tickets` |

The Agent Skills specification and the `skills` CLI do not currently resolve
transitive skill dependencies. Install Matt Pocock's skills before installing
this repository:

```bash
npx skills@latest add mattpocock/skills
npx skills@latest add momoi-labs/skills
```

For a non-interactive Codex installation:

```bash
npx skills@latest add mattpocock/skills \
  --skill '*' \
  --agent codex \
  --global \
  --yes

npx skills@latest add momoi-labs/skills \
  --skill '*' \
  --agent codex \
  --global \
  --yes
```

## Available skills

- `my-commit`: create signed Conventional Commits.
- `my-handoff`: add personal conventions to the upstream handoff workflow.
- `my-implement`: deliver issues and plans through the upstream implementation
  workflow.
- `my-pg-researcher`: research PostgreSQL source code, mailing lists, and
  CommitFest entries.
- `my-to-tickets`: turn epics into dependency-ordered GitHub issues.

## Repository layout

Each skill follows the open
[Agent Skills specification](https://agentskills.io/specification):

```text
skills/
└── skill-name/
    ├── SKILL.md
    ├── agents/       # optional client metadata
    ├── references/   # optional supporting documentation
    └── scripts/      # optional executable helpers
```
