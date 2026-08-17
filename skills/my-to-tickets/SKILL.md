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

## 0. Modo de execução

Antes de iniciar qualquer trabalho, pergunte ao usuário se deseja o modo
`print` (comportamento existente: apenas exibir prompts copyable) ou
`dispatch` (disparar subagentes continuables hierárquicos além de printar
os prompts para registro).

Registre o modo escolhido e mantenha-o durante toda a execução do skill. O
modo afeta como o handoff é escrito (Seção 5) e como os prompts são emitidos
(Seção 6).

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
or another concrete acceptance outcome. Always add one conformance review issue
as a child of the epic too; it delivers ADRs and issue references, not ceremony
(section 4 defines it and its template). The only tickets you may never invent
are an empty commit or a ceremonial closer — a ticket whose sole deliverable is
being closed. If the work has no legitimate final slice, return to the
breakdown with the user instead of forcing one.

Make the epic the final node of the graph. It is blocked by every leaf whose
completion is necessary for that final slice, plus the conformance review issue,
including leaves already closed when a resumed run publishes the relationships.
The pull request produced from implementing the epic will close it through the
normal issue-backed `my-implement` workflow.

Before changing GitHub, show an approval preview containing:

1. Each proposed or reused sub-issue, its blockers, and what it delivers —
   including the conformance review issue.
2. The final implementation slice retained by the epic.
3. Existing sub-issue reconciliation decisions.
4. The resulting unlock waves, with the conformance review as its own wave and
   the epic as the final wave.

Retain the upstream granularity and blocking-edge quiz. Publish only after
explicit approval of the complete preview.

## 4. Publish resumably with native relationships

Create new issues in dependency order with `gh issue create --parent` and
`--blocked-by`. Apply the configured agent-ready triage label from
`to-tickets`. Include the upstream issue template, the epic reference, and the
hidden reconciliation marker.

Create the conformance review issue in the same pass, with `--parent <epic>` and
`--blocked-by` naming every other child (open or closed), using this body (fill
the drift examples with real gaps you can already see in the epic, or the
general inter-slice drift risk when the epic is new):

```markdown
Part of #<epic>. This issue is the epic's definition of done: #<epic> does not
close until this passes.

## Why this exists

Implementation slices can each close correctly while the epic drifts from its
specification, because drift accumulates *between* slices that are individually
coherent. Slice-by-slice review cannot catch it. <Concrete drift you can already
see in this epic, or the inter-slice drift risk when it is new.>

## What to do

Run `/code-review` on the **Spec** axis against the merge-base of the whole
epic, not per slice. Then walk every user story in #<epic> one at a time and
record, for each, either the evidence that satisfies it, or the issue that
tracks the gap.

Where the code deviates deliberately, record the deviation as an ADR in
`docs/adr/` — not silently accepted, and not "fixed" back to a specification
that is no longer the intent.

## Acceptance criteria

- [ ] Every user story in #<epic> is marked satisfied, deliberately deviated
  (with an ADR reference), or deferred (with an issue reference). None
  unaccounted for.
- [ ] No finding is closed by editing #<epic>'s history; the issues stay as the
  record of what was decided when.

<!-- my-to-tickets: epic=OWNER/REPO#NUMBER; key=conformance-review -->
```

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
- #<conformance-review>
<!-- my-to-tickets:final-slice:end -->
```

Append the section if absent; replace only the content between its markers on a
resume. Treat the blockers listed in the previous managed section as the set of
blocker edges managed by this skill, including the conformance review issue.
After approval, add native `blocked by` relationships from the epic to every
required leaf and to the conformance review issue, whether open or closed, and
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

No modo `dispatch`, registre também no handoff:

- O modo de execução escolhido (dispatch).
- A lista de subagentes disparados, com número do issue, label e subagent id.
- O status de cada wave (dispatched, completed, failed).

## 6. Emit every remaining implementation prompt

Write the response in the current chat language. First report the handoff path,
the current frontier, the complete wave order, and any safe parallelism.

### Modo print

No modo `print`, emita um bloco fenced copyable separado para cada sub-issue
aberto e, por último, o épico. Agrupe os blocos sob headings numerados de
unlock-wave. Inclua todas as waves agora, mas indique que um prompt de wave
futura não deve ser aberto até que todos os seus blockers estejam `CLOSED`.

Use este formato, adaptando a frase de escopo ao ticket:

```text
Leia <absolute-handoff-path> e continue de onde a sessão parou.

---
Invoque $my-implement no issue <canonical-issue-url>.
Base: <base>. Implemente somente <ticket-scope>.
Confirme com gh que <blocker-urls-or-numbers> estão CLOSED antes de começar.
Não antecipe tickets de ondas posteriores.
```

Para um issue sem blockers, substitua a linha de confirmação por
`Este issue não tem blockers e pode começar agora.` Para o conformance review
issue, adapte a frase de escopo para executar `/code-review` no eixo Spec e
registrar cada gap como um ADR ou issue — não é um ticket de implementação de
código. Para o prompt final do épico, nomeie todos os leaf blockers necessários
mais o conformance review e indique explicitamente que seu pull request deve
fechar o épico através do comportamento normal `$my-implement` issue-backed.

### Modo dispatch

No modo `dispatch`, para cada wave em ordem:

1. **Verificar blockers.** Confirme com `gh issue view <n> --json state` que
   todos os issues bloqueadores da wave estão CLOSED. Se algum estiver OPEN,
   pare e avise o usuário.

2. **Printar prompts.** Emita os prompts da wave em blocos fenced copyable
   (para registro), agrupados sob o heading da wave.

3. **Disparar subagentes.** Para cada ticket da wave, dispare um subagente
   continuable usando o tool `subagent` com `run_in_background: true`,
   `description` no formato `#<issue-number> <short-title>`, e `prompt`
   (o prompt completo do ticket incluindo o caminho absoluto do handoff).
   Use `maxDepth: 5` para acomodar delegações profundas
   (my-implement -> research -> etc.).

4. **Esperar settlement notices.** Aguarde as settlement notices de todos os
   subagentes da wave. O runtime notifica automaticamente quando cada
   subagente termina.

5. **Tratar erros.** Se um subagente falhar (erro, max-tokens, refusal),
   pergunte ao usuário: tentar novamente, pular, ou abortar a wave inteira.

6. **Próxima wave.** Repita para a próxima wave.

O prompt do épico (final slice) NÃO é disparado automaticamente. Após todas
as waves de leaves terminarem, avise o usuário: "Todos os leaves terminaram.
Dispare o épico manualmente quando pronto." O épico fecha via PR do
`my-implement`, não via subagente.

### Formato geral

Para um issue sem blockers, substitua a linha de confirmação por
`Este issue não tem blockers e pode começar agora.` Para o conformance review
issue, adapte a frase de escopo para executar `/code-review` no eixo Spec e
registrar cada gap como um ADR ou issue — não é um ticket de implementação de
código. Para o prompt final do épico, nomeie todos os leaf blockers necessários
mais o conformance review e indique explicitamente que seu pull request deve
fechar o épico através do comportamento normal `$my-implement` issue-backed.

Do not close the epic directly. No modo print, não abra agents ou inicie
implementação em nome do usuário; os prompts paste-ready são o deliverable do
handoff. No modo dispatch, os subagentes são disparados automaticamente, mas
o épico permanece para dispatch manual pelo usuário.