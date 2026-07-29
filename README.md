# Momoi Labs Skills

Personal Agent Skills and workflow wrappers used across Codex and other
Agent Skills-compatible clients.

## Prerequisite

Some skills in this repository wrap workflows maintained in
[`mattpocock/skills`](https://github.com/mattpocock/skills):

| Skill           | Upstream dependency                   |
| --------------- | ------------------------------------- |
| `my-handoff`    | `handoff`                             |
| `my-implement`  | `implement` and its upstream workflow |
| `my-to-tickets` | `to-tickets`                          |

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

## Setup

Run **`/setup-matt-pocock-skills`** before your first engineering flow to configure the issue tracker, triage labels, and domain doc layout the skills assume.

## Main Flow: Idea → Ship

The route most work travels.

1. **`/grill`** or **`/grill-with-docs`** — sharpen the idea through interview
2. **`/to-spec`** — turn the conversation into a spec and publish it as an epic issue
3. **`/my-to-tickets`** — break the epic into dependency-ordered sub-issues with native blocking relationships
4. **`/my-implement`** — implement each sub-issue (blockers first), with local validation and PR publication

### Branching during the flow

- **Can every question be settled in conversation?** No → detour through **`/prototype`** (via **`/my-handoff`**):
  1. **`/my-handoff`** out (compact into a dated document)
  2. Open a fresh session against that file
  3. **`/prototype`** to answer with throwaway code
  4. **`/my-handoff`** back (reference what you learned)
- **Multi-session build?** Use steps 1–4 above.
- **Single session?** Skip `/my-to-tickets` and run **`/my-implement`** directly.

## On-Ramps

Starting situations that generate work, then merge onto the main flow.

| Situation                                                    | Skill                                                                                    |
| ------------------------------------------------------------ | ---------------------------------------------------------------------------------------- |
| Bugs / requests piling up                                    | **`/triage`** — moves issues through triage roles, produces agent-ready issues           |
| Something's broken (hard bug, intermittent flake)            | **`/diagnosing-bugs`** — tight feedback loop, regression test, post-mortem               |
| Greenfield project or huge feature (too big for one session) | **`/wayfinder`** — charts a shared map of decision tickets, then hands off to `/to-spec` |

> **`/triage`** is only for issues you didn't create — bug reports, incoming feature requests. Issues produced by `/my-to-tickets` are already agent-ready.

## Codebase Health

Not feature work — upkeep.

- **`/improve-codebase-architecture`** — surfaces deepening opportunities; picking one generates an idea you can take into the main flow at `/grill-with-docs`

## Vocabulary Layers

Skills that run beneath the others, providing shared terminology.

- **`/domain-modeling`** — sharpen the project's domain language (challenge fuzzy terms, resolve overloaded words, record ADRs)
- **`/codebase-design`** — deep-module vocabulary (module, interface, depth, seam, adapter, leverage) for designing a module's shape

## Personal Wrappers

These wrap Matt Pocock's original skills with personal conventions (path naming, branch prefixes, validation loops, git workflows).

| Personal           | Original     | What it adds                                                                                   |
| ------------------ | ------------ | ---------------------------------------------------------------------------------------------- |
| `my-handoff`       | `handoff`    | Dated docs, OS temp path, slug naming, paste-ready prompt                                      |
| `my-to-tickets`    | `to-tickets` | GitHub native `--parent` / `--blocked-by`, reconciliation, shared handoff, unlock waves        |
| `my-implement`     | `implement`  | Treehouse worktree lease, `seba/` branches, local validation loop, `my-commit`, PR publication |
| `my-commit`        | (none)       | Personal commit gate — inspect, stage explicitly, validate                                     |
| `my-pg-researcher` | (none)       | PostgreSQL source code and mailing list researcher                                             |

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
