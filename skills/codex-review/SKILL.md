---
name: codex-review
description: Have Codex review the plan, each implementation slice, and the final branch before the pull request, looping until Codex approves. Use when the user wants unattended work (for example overnight) with Codex as the reviewer, and wants a review log to check before merging.
argument-hint: "The task or plan to review and implement"
disable-model-invocation: true
---

# Codex Review

Use Codex as a second reviewer while you plan and implement. Codex reviews; you
write. The loop at each gate ends when Codex approves. The user is usually away,
so do not stop to ask questions that a review round can settle.

## 1. Settings

| Gate                  | Model          | Effort   |
| --------------------- | -------------- | -------- |
| Plan                  | `gpt-6.1-sol`  | `medium` |
| Implementation slice  | `gpt-6.1-sol`  | `low`    |
| Final branch (pre-PR) | `gpt-6.1-sol`  | `medium` |

The user's Codex plan has a limited quota. Never raise the effort above these
values unless the user asks. If the user names another model or effort in the
request, use that instead.

## 2. How to call Codex

Use the first transport that is available:

1. **T3 Code:** call `delegate_task` with the Codex provider instance from
   `orchestrator_capabilities`, the model above, and
   `target.options: {"reasoningEffort": "<effort>"}`. Check that the returned
   provider, model, and options match. Start a new `delegate_task` for every
   round, with a distinct `clientRequestId` per round. Do not continue a round
   with `t3_thread_send`.
2. **Codex CLI:** run
   `codex exec -m gpt-6.1-sol -c model_reasoning_effort="<effort>" -s read-only -C <worktree> -o <tmpfile> -`
   with the review prompt on stdin, then read `<tmpfile>`.

If neither transport works, stop and report it. Do not implement without
review.

## 3. Review prompt

Every round is a fresh call, so each prompt must carry the full context:

- the original task, in the user's words
- the absolute path of the worktree and the base branch
- what to review: the plan text, or the commit range for `git diff`
- every earlier finding of this gate, your response to each one, and the
  objections still open
- the instruction to stay read-only and not edit files

Ask Codex to answer in this format:

```text
VERDICT: APPROVED | CHANGES_REQUESTED
FINDINGS:
- [blocker|major|minor] <file:line or plan step>: <problem>. <suggested fix>
```

Treat `APPROVED` with only `minor` findings as approved. Fix those minor
findings if they are cheap, but do not start another round for them.

## 4. Gates

### Plan

1. Write the plan.
2. Send it to Codex for review.
3. On `CHANGES_REQUESTED`, fix the plan, or answer the finding with a reason if
   you disagree. Then send a new round.
4. Repeat until Codex approves. Then implement.

### Implementation slices

Split the work into slices that each end in a green state (builds, tests pass).
After each slice:

1. Commit it with `my-commit`.
2. Send the slice's commit range to Codex.
3. Fix the findings in a new commit and send a new round, until Codex approves.
4. Move to the next slice.

### Final branch

When all slices are done, send the full diff against the base branch to Codex.
Loop the same way until it approves. Then open the pull request and stop.
Never merge. The user reviews and merges.

## 5. When the loop cannot end

There is no round limit. Only two conditions end a loop without approval:

- **Quota or rate limit:** Codex returns a usage-limit error. Record the gate
  and round where it happened, push what is committed, and stop. Do not go on
  without review.
- **Repeated finding:** Codex raises a finding again after you answered it with
  a reason in an earlier round. Record it as a divergence, with both positions,
  and continue. Do not loop on it.

## 6. Review log

Keep a log while you work. Put it in the pull request body under a
`## Codex review` heading, and include it in your final message. One line per
round is enough:

```text
- Plan, round 1: CHANGES_REQUESTED (2 major). Fixed: <short>.
- Plan, round 2: APPROVED.
- Slice "<name>", round 1: APPROVED.
- Divergence: <finding>. Codex: <position>. Agent: <position>.
```

End the final message with the pull request URL, the open divergences, and
anything that stopped early.
