---
name: my-implement
description: Implement work from either a GitHub issue or an already-resolved brainstorm, grill, or implementation plan through the user's personal workflow around the externally maintained implement skill. Use when work should run in an isolated native Git worktree, use seba-prefixed branches and my-commit, wait for local user validation, publish a ready pull request without requiring an issue, wait for that PR to merge, and remove the worktree.
---

# My Implement

Orchestrate the user's personal delivery workflow without copying or replacing
the underlying implementation discipline.

Before starting, read and follow `~/.agents/skills/implement/SKILL.md` completely.
Where this skill adds a convention or gate, apply it around that workflow.

## 1. Resolve the work source and repository

Accept either of these work sources:

- **Issue-backed work:** Fetch the GitHub issue with `gh`. Record its canonical
  URL, repository `owner/name`, number, and title. Use the issue as the approved
  implementation brief.
- **Conversation-backed work:** Reuse the current conversation when a brainstorm,
  grill, or implementation plan has already resolved the problem, scope, key
  decisions, acceptance behavior, and testing approach. Do not call `to-spec`,
  create an issue, or repeat the interview. Synthesize a concise work title from
  the approved plan and use the conversation itself as the implementation brief.

Conversation-backed work is ready only when no material decision remains open.
If the context is incomplete, identify the unresolved decision and ask the user
to finish it before implementation; do not invent requirements. If the work
title is ambiguous, offer three concise titles and let the user choose.

Resolve the current checkout's canonical `owner/name` with `gh repo view`. For
issue-backed work, compare that identity case-insensitively with the issue
repository. Do not compare raw Git remote URLs: SSH and HTTPS forms may identify
the same repo. Stop and ask the user to select the correct repository if the
identities differ; never search for or guess another checkout. For
conversation-backed work, the current repository is the target repository.

If the prompt does not name a base branch, ask the user which base to use and
recommend `main`. If it does, do not ask again.

Fetch `origin` before resolving the base:

- For `main`, require the updated `origin/main`.
- For a custom base, prefer the updated `origin/<base>`.
- If a custom base exists only locally, explain that and ask before using it.
- If the base does not exist, stop.

Record the exact base commit before creating the task branch. Use that immutable
commit later when compacting task commits.

## 2. Create the isolated worktree and branch

Derive a lowercase kebab-case feature slug from the resolved work title and
prefix it with `seba/`. For example, `Add Recurring Expenses` becomes
`seba/add-recurring-expenses`.

Check local branches, remote branches, and existing worktrees for a collision.
If the name is already in use, stop and ask whether to reuse it or choose another
name. Never overwrite or reset a branch merely to resolve the collision.

Identify the canonical main checkout from `git worktree list --porcelain`: it is
the worktree whose path contains the repository's `.git` directory rather than a
`.git` file. Record its absolute path as `<main-checkout-path>`. Derive every
task worktree from that checkout, even when the skill starts inside another
worktree, using this deterministic sibling path:

```text
<parent-of-repository>/<repository-name>-worktrees/<branch-name>
```

For example, the `seba/add-recurring-expenses` branch for
`/projects/budget` uses
`/projects/budget-worktrees/seba/add-recurring-expenses`. Record the resulting
absolute path and the main checkout path. Run every `git worktree` command below
with `git -C <main-checkout-path>`.

If the user chooses reuse, continue only when `git worktree list --porcelain`
identifies the existing registered worktree for that branch, the local branch is
unpushed and unpublished, the worktree is clean, and the branch descends from the
recorded base. Show its commits and changed paths, then require the user to
confirm that they all belong to this work. Continue directly in that worktree; do
not create another worktree or recreate/switch the branch. A remote branch,
published branch, unregistered or dirty worktree, or unverifiable history
requires a different branch name and stays outside this new-work workflow.

For a new branch name, create the parent directory and add a native Git
worktree at the deterministic path from the resolved base commit:

```bash
mkdir -p "$(dirname <absolute-worktree-path>)"
git -C <main-checkout-path> worktree add -b <branch-name> <absolute-worktree-path> <base-commit>
```

Confirm that the new worktree is clean, then perform every subsequent operation
inside it. Keep it through implementation, validation, publication, and any
post-publication fixes. Do not remove it early unless the user explicitly asks to
abandon it. After the pull request merges, remove it as required in section 6.

## 3. Implement and commit

Follow the original `implement` skill in the isolated worktree, including its TDD,
testing, typechecking, and code-review requirements. Pass it the resolved work
source as its spec: the issue for issue-backed work or the approved conversation
and plan for conversation-backed work.

Replace its generic commit action with this commit gate:

1. Inspect the worktree and confirm every changed path belongs to this task.
2. Stop and ask about any unexpected or pre-existing change.
3. Stage the expected paths explicitly; do not use `git add -A`.
4. Read and follow [my-commit](../my-commit/SKILL.md) to create the commit.

Do not push or create a pull request yet.

## 4. Run the user validation loop

After the implementation is reviewed, tested, and committed, say it is ready for
local validation. Give only the indispensable steps, normally two to four lines:
the worktree or command to use, the action to perform, and the observable result
to expect. Add setup details or automated test results only when needed to make
the validation possible.

Wait for explicit user acceptance.

If the user finds a problem:

1. Correct it in the same worktree.
2. Run the affected tests and all checks required by `implement`.
3. Inspect and stage only the expected paths.
4. Commit the correction with [my-commit](../my-commit/SKILL.md).
5. Return to the short local-validation instructions and wait again.

Never publish while validation is pending or rejected.

## 5. Prepare publication

After explicit acceptance, query pull requests for this repository and exact
head branch across **all states**, not only open pull requests. If any current or
historical pull request exists, stop: the pre-publication compaction below is no
longer allowed.

```bash
gh pr list --repo <owner/name> --head <branch> --state all \
  --json number,state,url
```

Before the first push, compact task checkpoints only when all of these conditions
hold: the worktree is clean, the recorded base is an ancestor of `HEAD`, no pull
request has ever used the branch, and every commit since the base belongs to this
work. If there is already exactly one task commit, leave it intact. Otherwise:

1. Record the pre-compaction commit and tree IDs for recovery and comparison.
2. Soft-reset the branch to the recorded base so the accepted final diff remains
   staged.
3. Verify the staged paths and diff still exactly represent the accepted task.
4. Read and follow [my-commit](../my-commit/SKILL.md) to create one final commit.
5. Verify the new commit's tree ID equals the recorded pre-compaction tree ID and
   `git status --short` is empty.

If compaction or comparison fails, restore the clean branch to the recorded
pre-compaction commit, report the failure, and do not push.

Use this non-interactive shape, substituting the recorded immutable IDs rather
than resolving a moving branch name again:

```bash
git merge-base --is-ancestor <base-commit> HEAD
git status --short
git rev-parse HEAD
git rev-parse 'HEAD^{tree}'
git reset --soft <base-commit>
# inspect the staged diff, then run my-commit
git rev-parse 'HEAD^{tree}'
```

On any failure after the soft reset, restore tracked files and history to the
previously clean state with `git reset --hard <pre-compaction-commit>` before
stopping. Never delete untracked files during recovery; report any that remain
and do not push. Never run this compaction after publication.

Use the resolved work title for the pull request unless the user supplied an
explicit title. Compare that title with the accepted implementation:

- If they align, continue with the resolved work title.
- If the implementation exceeded the approved source's scope, explain the
  mismatch and ask the user to choose between trimming it to that scope or
  explicitly accepting a revised scope. If trimming changes code, rerun the
  required tests and review, commit with `my-commit`, and return to the user
  validation loop. If the user accepts unchanged code under a revised scope,
  record that scope and the chosen PR title, then return directly to explicit
  validation without creating an empty commit. Do not publish an unresolved
  mismatch.
- If only the wording is stale or imprecise, offer three concise titles based on
  the delivered behavior and wait for the user's choice.

At this point read [references/pull-request.md](references/pull-request.md) and
fill the selected body template truthfully. For issue-backed work, include
`Closes #<issue-number>`. For conversation-backed work, do not invent an issue
reference.

Push the branch with upstream tracking and create a ready-for-review pull request
against the chosen base. Report the pull request URL, branch, final commit, and
isolated worktree path, then continue to section 6. Do not end the workflow here.

After creating the pull request, ask the user whether they want you to watch the
CI and merge the pull request automatically once the checks pass. If they
decline, continue to section 6 with the manual-polling path. If they accept,
record the acceptance and follow the monitor-and-merge path in section 6.

## 6. Wait for merge and remove the worktree

When the user accepted automatic merge, follow this path instead of the
manual-polling path below. Watch the CI until it finishes:

```bash
gh pr checks <number> --repo <owner/name> --watch
```

When every check passes, merge the pull request and continue to the `MERGED`
cleanup below:

```bash
gh pr merge <number> --repo <owner/name> --rebase
```

If the pull request is already `MERGED` (merged by someone else during the
watch), skip the merge and go straight to the cleanup below.

If the repository has no checks, report that there is no CI to watch, so
automatic merge is not possible, and stop without merging. If any check fails,
or `gh pr merge` fails — including a required review that blocks the merge —
report the failure and stop without merging. Do not keep waiting and do not
merge.

When the user declined automatic merge, use the manual-polling path below.

After the pull request exists, keep the worktree until that exact PR is merged.
Do not treat the first `OPEN` observation as the end of the workflow. Poll until
`state` is `MERGED`:

```bash
gh pr view <number> --repo <owner/name> --json state,mergedAt,url
```

Repeat that check on a short interval while the PR stays `OPEN`. Between polls,
post-publication fixes from the Published branches rules below remain allowed;
after any such fix, resume polling the same PR until it merges. If the user
reports that the PR merged, verify with `gh` before removing the worktree.

When `state` is `MERGED`:

1. Leave or avoid depending on a shell whose cwd is inside the isolated worktree.
2. Confirm its working tree is clean. If it is not, stop and ask the user whether
   to discard the changes and remove it or keep it for follow-up work.
3. Remove the clean recorded worktree from the recorded main checkout:

```bash
git -C <main-checkout-path> worktree remove <absolute-worktree-path>
```

4. Confirm with `git -C <main-checkout-path> worktree list --porcelain` that the
   path is no longer registered.
5. Report the PR URL and that the worktree was removed. The workflow ends here.

If the PR is `CLOSED` without merge, do not remove automatically. Ask whether to
keep the worktree for follow-up work or remove it. Remove only after an explicit
choice. Before removing it, confirm it is clean; if the user explicitly chooses
to discard uncommitted changes, use
`git -C <main-checkout-path> worktree remove --force <absolute-worktree-path>`.

Remove a merged PR's clean worktree promptly. Never run `git worktree remove`
before merge unless the user explicitly asks to abandon the worktree. Preserve a
dirty worktree until the user explicitly chooses whether to discard or keep it.

## Published branches

After the pull request exists, never amend or squash the task commits. Normal
changes are additive commits made with `my-commit`. A later intentional rebase
onto an updated base may rewrite history and must use `--force-with-lease`, never
bare `--force`; that rebase is a separate workflow from `my-implement`.
