---
name: my-commit
description: Create a well-formatted git commit following conventional commit standards
disable-model-invocation: true
allowed-tools: Bash(git *)
---

Create well-formatted git commits following project commit conventions.

## Instructions

When invoked, create a git commit following these steps:

1. **Analyze changes**: Run `git status` and `git diff --staged` to understand what will be committed
2. **Determine type**: Choose the appropriate commit type based on changes:
   - `feat`: New feature or capability
   - `fix`: Bug fix
   - `docs`: Documentation-only changes
   - `style`: Formatting, whitespace (no code change)
   - `refactor`: Code restructuring without behavior change
   - `perf`: Performance improvement
   - `test`: Test additions or modifications
   - `build`: Build system or external dependency changes
   - `ci`: CI configuration and scripts
   - `chore`: Maintenance tasks, dependency updates
   - `revert`: Revert a previous commit

3. **Format commit message**:
   ```
   <type>[optional scope][!]: <subject line (max 50 characters)>

   <body: lines wrapped at 80 columns, focus on WHY not WHAT>
   ```

4. **Create commit**: Use `git commit -s` with the formatted message

## Rules

- **Title**: Maximum 50 characters, lowercase, no period
- **Optional scope**: Add a `(scope)` after the type when it helps, e.g. `feat(api): ...`
- **Breaking change**: Append `!` before the colon, e.g. `feat(api)!: ...`
- **Body**: Lines wrapped at 80 columns maximum
- **Sign-off required**: Always use `-s` flag
- **Focus on problem solved**: Describe why, not implementation details
- **No AI references**: Never add AI assistant names as co-author or in commit messages
- **No AI attribution**: Never include "Generated with", "Assisted-by", or similar lines

## Example

```
feat: add crush ai assistant and fix build limits

Enable AI-powered CLI assistant for enhanced terminal productivity
and code assistance. Fix "too many open files" errors during
large local development workflows by raising file descriptor limit to 10240.
```

## Workflow

1. Check staged changes with `git status` and `git diff --staged`
2. If nothing staged, show error and suggest `git add`
3. Generate commit message following format above
4. Execute: `git commit -s -m "$(cat <<'EOF'
<formatted message>
EOF
)"`
5. Confirm with `git log -1 --oneline`
