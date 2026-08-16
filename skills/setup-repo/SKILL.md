---
name: setup-repo
description: Bootstrap a new or existing repository with Momoi Labs engineering conventions — conventional-commits validation for PR titles and commit messages, my-commit as the default commit path, rebase-and-merge as the merge strategy, and PRINCIPLES.md + ADR scaffolding. Idempotent; safe to re-run. Use when setting up a new repository or adopting an existing one.
disable-model-invocation: true
---

# Setup Repo

Bootstrap a repository with the Momoi Labs engineering conventions. This skill
is **idempotent**: re-running it never duplicates a section, never overwrites
user-owned content, and converges the skill-owned files on the current
convention. It works for a fresh repository and for adopting an existing one.

## What this produces

- Issue tracker, triage labels, and domain-doc layout — via the
  `setup-matt-pocock-skills` skill (orchestrated, not reimplemented).
- A `### Commit convention` block recording that every commit goes through
  `my-commit`, and that merges use rebase-and-merge.
- `.github/workflows/conventional-commits.yml` validating PR titles and commit
  messages with the `momoi-labs/actions/conventional-commits` action.
- Merge strategy configured to rebase-and-merge (GitHub repositories only).
- `docs/PRINCIPLES.md` (seeded with four starting principles) and `docs/adr/_template.md` (format).

## Process

### 1. Explore

Look at the current repo; don't assume. Check:

- `git remote -v` — GitHub? GitLab? No remote?
- `AGENTS.md` / `CLAUDE.md` — which exists? Is there a `## Agent skills` block?
- `.github/workflows/` — is there already a conventional-commits workflow?
- `docs/PRINCIPLES.md`, `docs/adr/`, `CONTEXT.md`, `CONTEXT-MAP.md` — present?

### 2. Run setup-matt-pocock-skills

Invoke the `setup-matt-pocock-skills` skill and follow it completely. It
configures the issue tracker, triage labels, and domain-doc layout, and writes
the `## Agent skills` block. Do not reimplement it here.

### 3. Add the commit convention block

After `setup-matt-pocock-skills` has written (or updated) the `## Agent skills`
block, add or update this sub-block inside it, in place (never a duplicate):

```markdown
### Commit convention

Create commits with `my-commit` (conventional commits). PR titles and commit
messages are validated by the `conventional-commits` workflow; merges use
rebase-and-merge.
```

### 4. Conventional commits validation

If the repository has a GitHub remote, write
`.github/workflows/conventional-commits.yml` from
[assets/conventional-commits.yml](assets/conventional-commits.yml). Reference
the action by its tag: `momoi-labs/actions/conventional-commits@conventional-commits-v1`.

- If the workflow does not exist, write it.
- If it exists, update it in place to the current seed. Do not append a second
  job or a second workflow file.
- If there is no GitHub remote, skip this step and rely on `my-commit` as the
  local gate. Say so.

### 5. Merge strategy: rebase and merge

If the repository has a GitHub remote, make rebase-and-merge the only merge
method. GitHub has no API for the *default* merge button — disabling the other
two methods leaves rebase as the only option. Idempotent:

```bash
gh repo edit --enable-rebase-merge=true --enable-merge-commit=false --enable-squash-merge=false
```

If there is no GitHub remote, skip this step.

### 6. Engineering principles and ADR scaffolding

Create these only if they are absent; never overwrite existing content:

- `docs/PRINCIPLES.md` — from [assets/principles.md](assets/principles.md). It
  ships the preamble, the tie-breaker rule, and four starting principles
  (smallest viable change, commit history tells a story, compatibility
  contract, no silent defaults). Offer to adapt them to this repo.
- `docs/adr/_template.md` — from [assets/adr-template.md](assets/adr-template.md).
  It documents the ADR format (YAML frontmatter: `status`, `date`, `supersedes`,
  `superseded_by`, `tags`). Real ADRs are written as decisions are made —
  record every decision, append-only (see the `Decisions are recorded,
  append-only` principle in `PRINCIPLES.md`) — by `/domain-modeling`, never by
  this skill.

If `docs/PRINCIPLES.md` already exists with real content, leave it untouched.

Optional: if the user wants, help adapt or add principles now using
`/grill-with-docs`. Do not write invented principles without the user.

### 7. Idempotency contract

| Files this skill owns | Rule |
| --------------------- | ---- |
| `.github/workflows/conventional-commits.yml` | update in place; never duplicate |
| `## Agent skills` block (incl. `### Commit convention`) | update in place; never duplicate |
| `docs/adr/_template.md` | update in place |

| Files the user owns | Rule |
| ------------------- | ---- |
| `CONTEXT.md` / `CONTEXT-MAP.md` | created only via `setup-matt-pocock-skills` / `domain-modeling`; never overwrite |
| `docs/PRINCIPLES.md` (real principles) | create skeleton only if absent; never overwrite |
| `docs/adr/NNNN-*.md` (real ADRs) | never touch; `/domain-modeling` owns them |

## Done

Report what was created, what was left untouched, and that re-running is safe.
