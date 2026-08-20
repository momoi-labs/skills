# How to publish an Agent Skills repository and distribute it on ChatGPT

> Research performed on July 24, 2026, based on official documentation and source code.

## Short answer

You can create a public GitHub repository with one or more `skills/<name>/SKILL.md` folders. Without publishing an npm package, it can already be installed like this:

```bash
npx skills@latest add your-org/your-repo
```

That command belongs to the open source CLI [`vercel-labs/skills`](https://github.com/vercel-labs/skills), not to ChatGPT. It clones/reads the repository, discovers the skills, and installs them into the directories local agents expect. The CLI itself documents the `owner/repo` GitHub shorthand, full Git URLs, local paths, per-skill installation, and target agent selection ([CLI README](https://github.com/vercel-labs/skills#install-a-skill)).

To make those same skills available to a team on ChatGPT, the repository alone is not enough. There are two official routes today:

1. **Workspace skills:** upload/create the skill in ChatGPT and share it with people, groups, or the whole workspace.
2. **Plugin:** package one or more skills as a plugin and share it with the workspace; this is the route OpenAI recommends for reusable distribution, catalogs, and bundles that may also include apps/MCP.

OpenAI's documentation is explicit: skills are the authoring format; plugins are the preferred format when the goal is distributing to other people in the workspace ([OpenAI — Build skills](https://learn.chatgpt.com/docs/build-skills)).

## 1. Minimum repository structure

Recommended structure to start from:

```text
your-repo/
├── README.md
├── LICENSE
└── skills/
    ├── review-pr/
    │   ├── SKILL.md
    │   ├── references/       # optional
    │   ├── scripts/          # optional
    │   └── assets/           # optional
    └── write-adr/
        └── SKILL.md
```

The CLI looks for skills at the root and in well-known directories, including `skills/`, `.agents/skills/`, and several agent-specific directories. In the common layout it walks `skills/<name>/SKILL.md`; it also accepts one category level, such as `skills/<category>/<name>/SKILL.md` ([CLI discovery rules](https://github.com/vercel-labs/skills#skill-discovery)).

The Agent Skills format is a folder whose only required file is `SKILL.md`. Scripts, references, templates, and other resources may accompany the skill ([Agent Skills standard overview](https://agentskills.io/home)).

Minimal example:

```markdown
---
name: review-pr
description: Reviews pull requests against internal standards. Use when the user asks for a review of a PR, branch, or diff.
---

# Review PR

1. Read the repository's standards.
2. Inspect the full diff.
3. Rank findings by severity.
4. Cite file and line for every problem.
```

Per the open standard:

- `name` is required, is at most 64 characters, uses only lowercase ASCII letters, digits, and hyphens, does not start/end with a hyphen, does not contain `--`, and must match the folder name;
- `description` is required, is at most 1024 characters, and must explain both what the skill does and when it should be used;
- `license`, `compatibility`, `metadata`, and `allowed-tools` are optional; `allowed-tools` is still experimental and its support varies across clients;
- the body is free-form Markdown; long instructions should move details into `references/`.

These rules come from the [Agent Skills specification](https://agentskills.io/specification). The specification also recommends keeping `SKILL.md` under 500 lines and using references relative to the skill root.

## 2. Create, validate, and publish

The CLI offers a simple generator:

```bash
mkdir my-repo
cd my-repo
mkdir -p skills
cd skills
npx skills@latest init review-pr
```

You can also create the folder and `SKILL.md` by hand. For strict validation against the standard, the specification points to the reference validator:

```bash
skills-ref validate ./skills/review-pr
```

Then publish the repository on GitHub as usual. For the shorthand below to work without authentication setup, use a public repository:

```bash
npx skills@latest add your-org/your-repo --list
npx skills@latest add your-org/your-repo
```

Useful tests before announcing it:

```bash
# list what the CLI found
npx skills@latest add your-org/your-repo --list

# install a specific skill into Codex
npx skills@latest add your-org/your-repo \
  --skill review-pr \
  --agent codex

# install globally, without prompts (useful in automated setup)
npx skills@latest add your-org/your-repo \
  --skill review-pr \
  --agent codex \
  --global \
  --yes
```

The `--list`, `--skill`, `--agent`, `--global`, `--copy`, `--yes`, and `--all` options are documented in the [`vercel-labs/skills` README](https://github.com/vercel-labs/skills#options). The same document identifies Codex with `--agent codex`.

You do not need to "publish on skills.sh" for the `add owner/repo` command to work: the source of truth is the Git repository. The skills.sh directory/leaderboard is fed by anonymous telemetry from CLI installations; appearing and ranking there is therefore a consequence of installations, not a prerequisite for distribution ([skills.sh documentation](https://www.skills.sh/docs)).

### Private repository

The CLI accepts any Git URL, including SSH, for example:

```bash
npx skills@latest add git@github.com:your-org/internal-skills.git
```

That form is listed among the supported sources in the [official README](https://github.com/vercel-labs/skills#source-formats). In practice, the process needs valid Git credentials. For enterprise use, test authentication, CI, and telemetry policy before standardizing on this route; the project itself still has open discussions about the experience and documentation for private repositories ([official issue #381](https://github.com/vercel-labs/skills/issues/381)).

## 3. Local installation in Codex

Vercel's CLI and Codex are distinct projects:

- `npx skills add` resolves a repository and copies/creates links in the directories of the chosen agents;
- Codex discovers and runs skills installed in its own scopes.

According to OpenAI's current documentation, Codex reads skills from the repository, the user, the administrator, and the system. In repositories, it looks for `.agents/skills` from the current directory up to the Git root; OpenAI also documents `$HOME/.agents/skills` for the user and `/etc/codex/skills` for machine/container administration ([OpenAI — where to save skills](https://learn.chatgpt.com/docs/build-skills#where-to-save-skills)). The `skills` CLI, in turn, declares `.agents/skills/` as the project path and `~/.codex/skills/` as the global path for its `codex` target ([CLI agent table](https://github.com/vercel-labs/skills#supported-agents)). For that reason, pass `--agent codex` explicitly and confirm with Codex's skill listing after installing.

For an engineering team, there are two local strategies:

- **Repo-scoped:** install/commit the skills in `.agents/skills/` inside each project. Everyone who clones the project gets the same workflows.
- **User-scoped:** each person installs globally with `--global`. It is convenient, but it requires a per-machine update process.

The CLI provides `npx skills update` to update the installations it manages ([CLI commands](https://github.com/vercel-labs/skills#other-commands)).

## 4. Adding to ChatGPT as a personal skill

In ChatGPT:

1. Open **Plugins** in the sidebar.
2. Go to the **Skills** tab.
3. Select **Create**.
4. Use **Upload from your computer**, the editor, or "Create with chat".
5. Review the skill and install it.

These paths are documented in [Skills in ChatGPT](https://help.openai.com/en/articles/20001066-skills-in-chatgpt/). ChatGPT verifies uploaded skills; they may become available immediately, require review, or be blocked. Because a skill can include code and supporting files, OpenAI recommends reviewing the origin and the content before uploading.

Important points:

- Personal skills are generally available in ChatGPT Business, Enterprise, Healthcare, and Edu.
- Personal skills must be added separately on desktop and on web/mobile; they do not sync automatically across those surfaces.
- The format follows the open Agent Skills standard, but features specific to one client may not work in another. For example, the `skills` CLI maintains a [compatibility matrix](https://github.com/vercel-labs/skills#compatibility) and shows that some fields/hooks are specific to particular agents.

In other words: the same basic `SKILL.md` is portable, but scripts, tools, hooks, and local paths must be tested on each surface.

## 5. Making it available to the team on ChatGPT

### Option A — share/publish a Skill in the workspace

After creating or uploading the skill:

1. Open **Plugins → Skills**.
2. Open the skill's `•••` menu.
3. Select **Share**.
4. Share with people/groups or publish to the workspace, according to the permissions available.

Members find skills under **Shared with me** or **Shared by {workspace}** and can install them. Administrators can upload directly on the administrative Skills page, change access and owner, download, or delete a skill ([OpenAI — Skills in ChatGPT](https://help.openai.com/en/articles/20001066-skills-in-chatgpt/)).

For Enterprise and Edu, Skills are disabled by default at the time described by the documentation; admins can enable them per role. The permissions are separate:

- create and use skills;
- upload;
- share;
- publish to the whole workspace;
- install for other members.

These controls apply to Skills managed in ChatGPT. OpenAI notes that Skills in other products, including Codex, may have separate governance.

### Option B — package as a plugin

Use a plugin when you want to:

- distribute one or several skills as a versioned package;
- offer an installable catalog;
- later include an app, MCP connector, hooks, or visual identity;
- share the package between ChatGPT Work and Codex.

The official minimum structure is:

```text
my-plugin/
├── .codex-plugin/
│   └── plugin.json
└── skills/
    └── review-pr/
        └── SKILL.md
```

`.codex-plugin/plugin.json`:

```json
{
  "name": "team-skills",
  "version": "1.0.0",
  "description": "Reusable team workflows",
  "skills": "./skills/"
}
```

This structure and the minimum fields are shown in [OpenAI — Build plugins](https://learn.chatgpt.com/docs/build-plugins#create-a-plugin-manually). A repository whose root contains `.codex-plugin/plugin.json` and `skills/` can, in principle, serve simultaneously as:

- the source for `npx skills add owner/repo`, because the CLI discovers `skills/<name>/SKILL.md`;
- the root of an OpenAI plugin, because the manifest points to `./skills/`.

Even so, treat the two installations as independent pipelines and test both.

To speed up packaging, OpenAI provides `@plugin-creator` in ChatGPT and `$plugin-creator` in Codex. It generates the required manifest and can create a local marketplace entry ([OpenAI — creating plugins](https://learn.chatgpt.com/docs/build-plugins#create-a-plugin-with-plugin-creator)).

After adding the plugin in the desktop app:

1. switch to the Work workspace;
2. open **Plugins → Created by you**;
3. open the plugin and select **Share**;
4. choose members, groups, or copy the link.

Recipients find it under **Shared with you**. This does not publish the plugin to the public directory; it stays inside the organization ([OpenAI — share a local plugin](https://learn.chatgpt.com/docs/build-plugins#share-a-local-plugin-with-your-workspace)).

## 6. Git marketplace for Codex/desktop

If you want the repository itself to be a plugin catalog, OpenAI documents JSON marketplaces:

- repo: `$REPO_ROOT/.agents/plugins/marketplace.json`;
- personal: `~/.agents/plugins/marketplace.json`.

You can also register a Git marketplace:

```bash
codex plugin marketplace add your-org/your-repo
codex plugin marketplace list
codex plugin marketplace upgrade
```

Accepted sources include the GitHub shorthand, HTTPS/SSH Git URLs, and a local directory. This is a different distribution from `npx skills`: the `codex plugin marketplace add` command installs/tracks a **plugin catalog**, while `npx skills add` installs **skill folders** into local agents ([OpenAI — add a marketplace from the CLI](https://learn.chatgpt.com/docs/build-plugins#add-a-marketplace-from-the-cli)).

For teams using ChatGPT desktop, a repository marketplace is useful during development and curation. For managed organizational access in ChatGPT, prefer sharing/publishing inside the workspace, because that applies the organization's identity, groups, and permissions.

## 7. Recommended architecture for your case

### Phase 1 — installable repository

1. Create `github.com/your-org/skills`.
2. Keep the skills in `skills/<name>/SKILL.md`.
3. Use a `name` matching the directory and a precise `description`.
4. Include a license, README, examples, and a security policy.
5. Test `npx skills@latest add your-org/skills --list`.
6. Test explicit installation on each supported agent.
7. Version changes with tags/releases and a changelog, even though the CLI installs directly from Git.

### Phase 2 — ChatGPT pilot

1. Upload one skill to the workspace.
2. Share it with a pilot group only.
3. Test prompts that should and should not activate it.
4. Confirm that scripts/dependencies work on the chosen surface.
5. Publish to the workspace only after the security and content review.

### Phase 3 — organized distribution

If there are several skills or connectors, add `.codex-plugin/plugin.json`, turn the repository into a plugin/catalog, and use the workspace's sharing controls. If the goal is delivering a single, repeatable experience to users, you can also attach skills to a Workspace Agent and publish that agent in the organization's directory; the builder accepts skills that were created, uploaded, or already available ([OpenAI — Workspace Agents](https://help.openai.com/en/articles/20001143-chatgpt-workspace-agents-for-enterprise-and-business)).

## 8. Security and maintenance checklist

- Review every `SKILL.md`, script, and asset before installing or sharing.
- Do not put secrets, tokens, or internal data in the public repository.
- Declare dependencies and network requirements in `compatibility` and in the documentation.
- Prefer instructions over scripts when you do not need deterministic behavior.
- Pin the versions of dependencies used by scripts.
- Test positive and negative activations; the `description` drives implicit discovery.
- Define ownership and pull request review.
- Use tags/releases and a changelog for auditability.
- For managed ChatGPT, configure upload, sharing, publishing, and installation roles with least privilege.
- Treat local Codex installation and ChatGPT workspace distribution as separate channels.

## Primary sources

- [vercel-labs/skills — CLI code and README](https://github.com/vercel-labs/skills)
- [skills.sh — directory and telemetry documentation](https://www.skills.sh/docs)
- [Agent Skills — open specification](https://agentskills.io/specification)
- [OpenAI — Build skills](https://learn.chatgpt.com/docs/build-skills)
- [OpenAI — Build plugins](https://learn.chatgpt.com/docs/build-plugins)
- [OpenAI Help — Skills in ChatGPT](https://help.openai.com/en/articles/20001066-skills-in-chatgpt/)
- [OpenAI Help — ChatGPT Workspace Agents](https://help.openai.com/en/articles/20001143-chatgpt-workspace-agents-for-enterprise-and-business)
