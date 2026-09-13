---
name: focus-buddy
description: Generate or refresh a focus doc with Focus Buddy, an ADHD-friendly HTML summary with a living TODO list. Use when the user asks for a summary or recap of the session or work, or to update the plan, the TODO list, or the focus doc.
---

# Focus Buddy

Focus Buddy creates a focus doc: one self-contained HTML file that turns scattered work into three things the reader can act on in seconds: one sentence of state, one next action, and a checklist that remembers what got checked. The page does the remembering; the reader holds nothing in their head.

## Pick the mode

- **Summary or recap requested** → create a new doc.
- **Update requested** ("atualiza o plano", "refresh my TODOs") and a focus doc for this work already exists under `docs/focus/` → update it. Several files and no clear match → ask which one. No file yet → create.

## Create

1. Mine the conversation (or the files the user pointed at) for, in order: everything that happened, decisions made and why, discoveries worth keeping, artifacts produced (with paths), work pending, work blocked.
2. Pick a kebab-case slug for the topic and write `docs/focus/<slug>.html` from [references/template.html](references/template.html). The `data-plan-id` on `<body>` equals the slug; it keys the saved checkbox state, so it stays fixed for the life of the doc.
3. Fill it following the writing rules below.
4. Open the file in the browser (`open` on macOS, `xdg-open` on Linux) and give the user the absolute path.

Done when every mined item is visible somewhere in the doc (current tasks or source context), the page opens showing the TL;DR, the current checklist and its progress count, with the source hidden until requested. Information the reader could act on tomorrow never gets dropped for brevity.

## Update

1. Read the existing file first. Every task has a `data-task` id; carry ids over unchanged for tasks that survive, so checked state in the browser survives the rewrite. New tasks get new ids.
2. Infer from the conversation which tasks finished and remove them from the refreshed checklist. Keep the IDs and saved state of surviving tasks. Ask the user when completion is ambiguous. Historical completion belongs in the source context only when needed to understand current work.
3. **Handle pasted feedback.** Every doc carries a Comment mode (footer): the user clicks an element, writes a note, and copies the "Focus doc feedback" block into chat. Map each note to its target: `title`, `facts`, `tldr`, `next`, `progress`, `tasks`, `source`, `context`, `footer`, or a task id. Fix the doc, and confirm each note in the reply. Notes live in the user's browser until cleared in the panel.
4. Re-derive the TL;DR and the task order from current reality, then regenerate the whole file from the template. The header date is the update date.
5. Open it and give the path.

Done when the rewritten page loads with the previous checked state intact (same plan id, same task ids).

## Writing rules

The format carries the cognitive load:

- **Conclusion first.** Use at least two short paragraphs in the TL;DR. Open with a bolded status sentence, then recap what changed. Add paragraphs when they carry useful information, with one idea per paragraph.
- **Header carries the facts.** Under the title sit chips: the remaining count for the current checklist, the project or repo, and one or two scope chips (branch, worktree, epic). Reader orientates before reading a word of prose.
- **One next action, when it helps.** Order the task list in do-order; with the card present, the first pending task becomes the "Do this now" card and the page advances it as boxes get checked. Include the card only when a single action clearly leads; omit it when tasks are parallel or the user drives by clicking the list. Decide rather than list options: when two tasks compete, pick one and note the loser under Context.
- **Tasks are starts, not epics.** Each begins with a verb and fits in one sitting. Split anything bigger until it does. A task has a bold action title and short detail paragraphs covering where to act, how to start, dependencies and what counts as done. Include the facts needed to act without opening another document; use as many detail paragraphs as needed, without repetition (file paths, scope, command, link). Render commands as HTML `<code>` inside the detail line, keeping explanations outside the code element.
- **Source beside tasks.** Open with only the current tasks visible. Provide a "Show details" checkbox that reveals or hides the source column; start unchecked on every opening rather than persisting this preference. When details are open, show the source document on the left and tasks in the right margin. Include its original link, section headings and snapshot date; translate it to the conversation language and distinguish later notes from source content. Each task points to the relevant section through `data-source`. Clicking its title, details or surrounding area opens the source column, checks "Show details", highlights and scrolls to that section; only its checkbox changes completion. Support Enter and Space on the task body. On narrow screens, stack tasks above the source. For conversation-only sources, embed the relevant conversation context and identify it as such rather than inventing a document link.
- **Chunk everything.** Context lives in collapsible sections, usually three to five, each with a plain-language summary; context chunks render open, the session log renders collapsed. One idea per paragraph.
- **Cut repetition, keep facts.** Prune wording, not content: every decision, discovery, artifact path, and pending item appears somewhere in the doc, usually as a muted detail line or a Context chunk. Lists over prose.
- **Close with a session log.** When the session was dense, the last Context chunk is a Session log: one line per thing that happened, in order. It is the proof that nothing was dropped, and it collapses away.
- **Count only current work.** The checklist contains the tasks to act on in this summary. Exclude historical completed tasks and omit a separate Done section. Display remaining tasks against this checklist total, such as "3 of 3 remaining". Checking a task changes this to "2 of 3 remaining" and advances the completion bar; it stays in the current checklist until the next document refresh.
- **Meaning-only color.** Accent marks the next action, green marks done, and no other decoration ships.
- **Match the conversation's language.** On creation and every update, write the entire focus doc in the current conversation's language. Translate existing content when it uses another language, in either direction. This includes headings, tasks, context, history, buttons, placeholders, accessible labels, JavaScript messages and copied feedback. Set `<html lang>` accordingly. Preserve commands, paths, product names, technical identifiers, stable task IDs and storage keys. This rule applies to the generated focus doc, not the source files it summarizes.
