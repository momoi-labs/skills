# Pull Request Body

Use this reference only after user validation succeeds and the task commits are
ready for their first publication.

## Select a template

Check tracked files in this priority order:

1. `.github/pull_request_template.md`
2. `.github/PULL_REQUEST_TEMPLATE.md`
3. `docs/pull_request_template.md`
4. Files under `.github/PULL_REQUEST_TEMPLATE/`

Use `git ls-files` from the leased worktree so untracked or unrelated templates
cannot be selected accidentally.

If one of the first three templates exists, use the first match. Otherwise, if
the template directory contains one file, use it. If it contains multiple files,
show their names and ask the user which one to use.

Fill every section in place and preserve HTML comments unless the template
itself instructs otherwise. For issue-backed work, put
`Closes #<issue-number>` in the template's issue field when one exists; otherwise
append it to the body. For conversation-backed work, omit the issue link and fill
any required issue field truthfully, such as `N/A`.

Do not invent test results, security claims, screenshots, or rollout details. If
a required section cannot be filled truthfully, ask the user for the missing
information.

## Fallback template

When the repository has no pull request template, use exactly this structure:

```markdown
**Problem:**

<!-- What's broken, missing, or wrong? Why does this change need to exist? -->

**Solution:**

<!-- What does this change do to address the problem? -->

---
_Testing:_

<!-- Describe test cases, both automated and manual. -->
```

Fill the sections. Append `Closes #<issue-number>` only for issue-backed work.
