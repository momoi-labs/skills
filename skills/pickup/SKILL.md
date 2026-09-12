---
name: pickup
description: Continue work started on another computer by reading a handoff document, reconciling it against real repository state, and building the session task list.
argument-hint: "Path to the handoff document"
disable-model-invocation: true
---

# Pickup

Pick up work started on another computer. The handoff document says what was
happening; the repository says what is true. This skill reconciles the two and
leaves a task list ready to run.

It pairs with `my-handoff` on the sending side. The file travels however the
user moved it (AirDrop, scp, sync); this skill only reads it.

## 1. Resolve the handoff document

Require the path to the handoff document as the argument. If no path was
passed, stop and ask for it. If the file is missing or unreadable, stop and
report the path that was tried.

Read the whole document before touching the repository. Record its date, its
focus, the artifacts it references, its next steps and pending decisions, and
its suggested skills.

## 2. Reconcile against the repository

Establish what is true before planning:

- Run `git fetch`, then report incoming and outgoing commits for the current
  branch. Pull or rebase only after the user approves.
- Run `git status` and `git log` covering the period since the handoff date.
- Check every artifact the handoff references: file paths, issues, pull
  requests, branches. Mark each one present or missing.

The repository is the source of truth. Where the handoff and the repository
disagree, trust the repository and record the divergence for the brief.

If a referenced branch or worktree is missing both locally and on the remote,
report it and stop: the user opens the worktree with the environment's
default mechanism and runs this skill again. Naming and placement of
worktrees belong to the default tooling.

## 3. Build the session task list

Turn the handoff's next steps and pending decisions into a session task list.
Drop every step the reconciliation shows as already done, and add the
follow-ups the divergences demand. Keep the handoff's own priority order.

## 4. Present the brief and stop

Deliver one decision-ready brief:

- divergences found, with the repository side winning each one
- incoming and outgoing commits
- missing artifacts
- the suggested skills from the handoff, listed by name for the user to invoke
- the single next action

Then stop. The work itself starts when the user starts it.
