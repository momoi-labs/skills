---
name: my-handoff
description: Compact the current conversation into a dated handoff document and return a ready-to-paste prompt for the next agent, wrapping the upstream handoff skill with personal conventions.
argument-hint: "What will the next session be used for?"
disable-model-invocation: true
---

# My Handoff

Orchestrate a personal handoff workflow without copying or replacing the
underlying handoff discipline.

Before starting, read and follow `~/.agents/skills/handoff/SKILL.md` completely.
Where this skill adds a convention or gate, apply it around that workflow.

## 1. Resolve focus and language

If the user passed arguments, treat them as the focus of the next session and
tailor both the handoff document and the paste prompt accordingly. If there is
no argument, derive a short focus title from the conversation theme.

Write the paste prompt in the same language as the current chat. If the
language is unclear, default to English.

## 2. Infer skills for the next agent

Discover which skills the next agent should actually invoke, in this order:

1. Skills explicitly invoked or attached in this session
2. Skills cited as the working method (for example, an in-progress grilling)
3. Skills clearly required for the stated next-session focus

Include only skills the next agent must invoke — not a generic inventory of
available skills. If the set is ambiguous, list 2–3 candidates and ask the user
to confirm **before** writing the handoff file.

## 3. Write the handoff document

Follow the upstream handoff skill for content, redaction, and references to
existing artifacts. Apply these path conventions on top:

- Save under the OS temporary directory (for example `/tmp` on macOS/Linux).
- Name the file `YYYY-MM-DD-<slug>-handoff.md` using today's local date and a
  lowercase kebab-case slug from the focus.
- Never overwrite an existing handoff. If that path already exists, append
  `-2`, `-3`, … before `.md` until the name is free
  (for example `2026-07-22-pgday-curitiba-talk-handoff-2.md`).

Keep a "suggested skills" section in the document, aligned with the skills
chosen for the paste prompt.

## 4. Emit the paste-ready prompt

After the handoff file is written, the primary user-facing deliverable is a
ready-to-paste prompt. Make it the **last** visible output, in a single easily
copyable fenced code block, using this fixed two-section template separated by
`---`:

1. An instruction to read the handoff at the absolute path and continue where
   the session left off (in the chat's language).
2. Synthesized operational instructions: skills to invoke, the next pending
   decision, and current guardrails (for example, what not to create yet).

Synthesize section 2 from conversation state and the optional focus argument.
Do not require the user to draft the operational block.

You may briefly confirm the handoff path before the fenced prompt, but the
copyable block is the main deliverable.

## Out of scope for v1

Do not add clipboard automation, a handoff index, or temporary-file cleanup.
