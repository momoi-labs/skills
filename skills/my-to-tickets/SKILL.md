---
name: my-to-tickets
description: Turn an existing GitHub epic into resumable, dependency-ordered sub-issues through the user's personal workflow around to-tickets. Use when the epic should retain the final implementation slice, child issues should use native GitHub parent and blocking relationships, and the result should include a shared handoff plus paste-ready my-implement prompts grouped by unlock wave.
---

# My To Tickets

Orchestrate the user's personal epic-planning workflow without copying or
replacing the underlying ticket discipline.

Before starting, read and follow `~/.agents/skills/to-tickets/SKILL.md`
completely. Also read [my-handoff](../my-handoff/SKILL.md) and apply its handoff
content, path, naming, redaction, language, and collision conventions. Where
this skill adds or overrides a convention, follow this skill.

## 1. Resolve the epic, repository, and base

Require an existing GitHub issue as the epic. Accept its URL or its number in
the current repository. Fetch its full body, comments, state, parent,
sub-issues, and blocking relationships with `gh`. Stop if it is closed, belongs
to another repository than the current checkout, or is itself a sub-issue.

Resolve the base branch once for the whole epic. If the user did not provide
one, ask and recommend `main`. Fetch `origin`, require the selected
`origin/<base>` to exist, and record its current commit. If a custom base exists
only locally, explain that and ask before using it. Record the verified branch
name for every implementation prompt; do not make later agents resolve it
again.

Require `gh` support for native `--parent`, `--blocked-by`,
`--add-blocked-by`, and the `subIssues` and `blockedBy` JSON fields. Stop with a
clear compatibility error rather than emulating relationships in issue text.

## 2. Reconcile existing epic work

Treat publication as resumable. Inspect all current sub-issues before drafting
or creating anything. Classify every existing child with the user as one of:

- already represented by the proposed breakdown;
- additional relevant work that must join the graph;
- out of scope and to be removed from the epic by the user.

Never ignore an open relevant child: doing so could let the epic close early.
Do not remove, close, overwrite, or silently repurpose an existing issue.

Recognize issues created by this skill by both their epic reference and this
hidden body marker:

```markdown
<!-- my-to-tickets: epic=OWNER/REPO#NUMBER; key=STABLE-SLUG -->
```

On a retry, reconcile marked issues by stable key, title, delivery, and
relationships. Show any mismatch and get approval before updating it. Never
create a duplicate merely because a previous publication stopped partway
through.

## 3. Draft the graph and reserve the epic's final slice

Follow `to-tickets` to draft tracer-bullet vertical slices and genuine blocking
edges. Publish every slice except the final one as a sub-issue.

Reserve one narrow, real implementation slice in the epic itself. It must
deliver meaningful integration, end-to-end behavior, migration, documentation,
or another concrete acceptance outcome. Do not invent a verification-only
ticket, empty commit, or ceremonial closer. If the work has no legitimate final
slice, return to the breakdown with the user instead of forcing one.

Make the epic the final node of the graph. It is blocked by every leaf whose
completion is necessary for that final slice, including leaves already closed
when a resumed run publishes the relationships. The pull request produced from
implementing the epic will close it through the normal issue-backed
`my-implement` workflow.

Before changing GitHub, show an approval preview containing:

1. Each proposed or reused sub-issue, its blockers, and what it delivers.
2. The final implementation slice retained by the epic.
3. Existing sub-issue reconciliation decisions.
4. The resulting unlock waves, including the epic as the final wave.

Retain the upstream granularity and blocking-edge quiz. Publish only after
explicit approval of the complete preview.

## 4. Publish resumably with native relationships

Create new issues in dependency order with `gh issue create --parent` and
`--blocked-by`. Apply the configured agent-ready triage label from
`to-tickets`. Include the upstream issue template, the epic reference, and the
hidden reconciliation marker.

Use native GitHub relationships as the source of truth. Textual `Blocked by`
sections may explain the graph but never substitute for native edges. After
creation, re-fetch every affected issue and verify its parent, blockers, label,
body marker, and open state.

Preserve the epic body byte-for-byte outside this managed section:

```markdown
<!-- my-to-tickets:final-slice:start -->
## Final implementation slice

### What remains

<The real end-to-end behavior retained by the epic.>

### Acceptance criteria

- [ ] <Criterion>

### Blocked by

- #<leaf>
<!-- my-to-tickets:final-slice:end -->
```

Append the section if absent; replace only the content between its markers on a
resume. Treat the leaf list in the previous managed section as the set of
blocker edges managed by this skill. After approval, add native `blocked by`
relationships from the epic to every required leaf, whether open or closed, and
remove obsolete relationships only when they appeared in that previous managed
list. Preserve unrelated existing blockers. Re-fetch the epic and verify both
its managed section and native relationships.

If any write or verification fails, stop immediately. Report exactly which
issues and relationships were created or updated so the next run can reconcile
them safely. Do not roll back by deleting issues.

## 5. Write the shared handoff

Write one dated handoff under the OS temporary directory using `my-handoff`
conventions. Capture the epic, base branch, approved graph, completed work,
remaining work, final slice, native relationships, decisions, and guardrails.
Use one shared handoff for every implementation prompt.

When resuming, treat closed blockers as satisfied. Record closed issues in the
handoff, but omit them from the paste-ready prompt list. Recompute unlock waves
from the remaining open graph.

## 6. Emit every remaining implementation prompt

Write the response in the current chat language. First report the handoff path,
the current frontier, the complete wave order, and any safe parallelism.

Then emit one separately copyable fenced block for every open sub-issue and,
last, the epic. Group blocks under numbered unlock-wave headings. Include every
wave now, but state that a future-wave prompt must not be opened until all of
its blockers are `CLOSED`.

Use this shape, adapting the scope sentence to the ticket:

```text
Leia <absolute-handoff-path> e continue de onde a sessão parou.

---
Invoque $my-implement no issue <canonical-issue-url>.
Base: <base>. Implemente somente <ticket-scope>.
Confirme com gh que <blocker-urls-or-numbers> estão CLOSED antes de começar.
Não antecipe tickets de ondas posteriores.
```

For an issue with no blockers, replace the confirmation line with
`Este issue não tem blockers e pode começar agora.` For the final epic prompt,
name all required leaf blockers and state explicitly that its pull request must
close the epic through the normal `$my-implement` issue-backed behavior.

Do not close the epic directly. Do not open agents or start implementation on
the user's behalf; the paste-ready prompts are the handoff deliverable.
