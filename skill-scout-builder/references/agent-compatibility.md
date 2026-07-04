# Agent Compatibility

## Portability Contract

Treat the open Agent Skills format as the compatibility baseline:

```text
skill-name/
├── SKILL.md
├── scripts/       optional
├── references/    optional
└── assets/        optional
```

Require `SKILL.md` YAML frontmatter with a lowercase hyphenated `name` matching the directory and a useful `description`. Use relative links from `SKILL.md`. Keep scripts self-contained and declare runtime dependencies in the instructions.

Host-specific metadata may coexist with this baseline, but the core workflow must not require it. For example, `agents/openai.yaml` is an optional Codex enhancement; other hosts may ignore it.

## Capability Profile

Before discovery, record this internal profile using only observable evidence:

| Capability | Values |
| --- | --- |
| Host | known product and version / unknown |
| Explicit invocation | syntax or unavailable |
| Visible Skill inventory | available / unavailable |
| Project Skill roots | paths or unknown |
| User Skill roots | paths or unknown |
| Shell and filesystem | available / restricted / unavailable |
| Git hosting search | authenticated / public / unavailable |
| Public web search | available / unavailable |
| Native registry or marketplace | name / unavailable |
| Native installer | name / unavailable |
| Native creator | name / unavailable |
| Approval boundary | summary |

Do not ask the user to identify the host when it is already observable. Ask only when choosing an installation destination would otherwise be unsafe or ambiguous.

## Known Host Adapters

### Codex

- Explicit invocation commonly uses `$skill-name`.
- Project Skills commonly live under `.agents/skills/`.
- User Skills commonly live under `~/.agents/skills/`; existing installations may also expose Codex-managed Skill directories.
- Use Codex registries, plugins, installers, creators, apps, or tools only when they are actually available.
- Keep `agents/openai.yaml` optional. Never make another host depend on it.

### Claude Code

- Explicit invocation uses `/skill-name`.
- Project Skills live under `.claude/skills/`.
- Personal Skills live under `~/.claude/skills/`.
- Use Claude Code plugins, commands, tools, and permission controls only when they are actually available.
- Do not emit Codex invocation syntax or installation paths as Claude instructions.

### Other Agent Skills-Compatible Hosts

- Use the host's documented Skill directory, invocation syntax, and permission model.
- If no documented installer exists, deliver the portable directory and tell the user which destination still needs confirmation.
- If the host supports only part of the specification, distinguish readable instructions from unsupported automatic discovery, scripts, tool pre-approval, or UI metadata.
- Never invent a marketplace, creator command, installation path, or invocation syntax.

## Feature Adapters

### Discover

Use the visible inventory first. Scan known local roots when filesystem access exists. Search host-native catalogs only when exposed. Search Git hosting and public web with available tools. Mark every unavailable channel in the ledger.

### Install

Prefer the host's official installer when available and reviewed. Otherwise, after user approval, copy the audited Skill directory into a documented project or user Skill root. If the root is unknown, deliver without installing.

### Tailor

Create a portable copy first. Keep the core `SKILL.md`, scripts, references, and assets host-neutral. Isolate optional host adapters in clearly named metadata or reference files. Preserve license and attribution.

### Create

Prefer a trustworthy host-native creator when one exists. Otherwise:

1. Create a lowercase hyphenated directory.
2. Write `SKILL.md` with `name` and `description`.
3. Add only necessary `scripts/`, `references/`, or `assets/`.
4. Validate against the Agent Skills specification or the best available host validator.
5. Run trigger, boundary, task, and safety tests.

### Invoke

Show the syntax for the active host only when known. For cross-host delivery, document examples separately, such as `$skill-name` for Codex and `/skill-name` for Claude Code, while preserving natural-language implicit invocation where supported.

## Compatibility Reporting

At delivery, state:

- specification-level compatibility
- hosts actually tested
- host-specific optional files included
- unsupported or untested host features
- installation paths and invocation syntax only for verified hosts

Say “compatible with Agent Skills hosts” rather than “works with every agent.” Agents that do not implement the format may require a manual prompt, plugin wrapper, or product-specific conversion.
