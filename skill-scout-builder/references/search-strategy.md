# Search Strategy

## Search Ledger

Maintain an internal ledger throughout discovery:

| Channel | Status | Queries or method | Results inspected |
| --- | --- | --- | --- |
| Current session | searched / unavailable | visible skill metadata | count |
| Local filesystem | searched / unavailable | scanner roots | count |
| Host-native catalogs | searched / unavailable | registries, marketplaces, plugins, curated sources | count |
| Git hosting | searched / unavailable | query families | count |
| Public web | searched / unavailable | query families | count |

Report unavailable channels. Do not silently convert partial coverage into “all channels searched.”

## Query Expansion

Derive several small query families from the confirmed brief:

1. Core outcome in the user's language.
2. English translation of the core outcome.
3. Common synonyms and adjacent professional terms.
4. Input + transformation + output.
5. Required platform, API, MCP, framework, or file type.
6. Workflow verbs such as analyze, extract, generate, review, publish, monitor, or convert.
7. Structural markers: `SKILL.md`, `.agents/skills`, `.claude/skills`, and host-specific plugin manifests.

Do not make one oversized query. Use focused combinations and adapt based on results.

## Channel Procedures

### Current Session

Inspect the available Skill list and compare full descriptions. Read the selected Skill's `SKILL.md` before claiming a match.

### Local Filesystem

When shell access is available, run:

```bash
python scripts/scan_local_skills.py --format json --query "<terms>"
```

Add explicit `--root` values when the relevant repository uses nonstandard locations. Inspect the best-scoring local files manually.

### Host-native Catalogs

Use registries, marketplaces, plugin catalogs, curated lists, or installers exposed by the active host. Treat listing and searching as discovery actions; downloading or installing is a later action.

Do not assume a catalog exists or reuse one host's commands on another host. Prefer primary source files over third-party summaries. Search repository contents when names alone are insufficient.

### Git Hosting

Use authenticated GitHub, GitLab, or other Git-host tools when available; otherwise use public repository or web search. Combine domain terms with structural queries such as:

```text
"SKILL.md" "<capability>"
path:SKILL.md "<tool-or-output>"
".agents/skills" "<workflow-term>"
".claude/skills" "<workflow-term>"
```

Search syntax varies by host and tool. Adapt the query rather than assuming every operator is supported.

For each serious candidate, inspect the exact revision, `SKILL.md`, scripts, dependencies, license, and recent maintenance signals. Record a commit or version when possible.

### Public Web

Use web search to find Skill catalogs, repository pages, author documentation, and compatible Agent Skills projects. Prefer primary source repositories and official documentation. Reject results that do not expose inspectable contents.

## Shortlisting

Deduplicate forks and mirrors. Prefer the upstream source unless a fork contains material, documented improvements.

Keep candidates only when:

- their actual contents are inspectable
- the core task is supported by evidence
- dependencies can be identified
- provenance is clear enough for a safety pre-screen

Inspect the strongest 3-5 candidates deeply rather than reporting a large list of weak title matches. Show the user one primary recommendation and only decision-relevant alternatives.
