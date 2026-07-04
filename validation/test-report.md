# Skill Scout Builder Validation Report

Date: 2026-06-17

## Result

The cross-Agent working version passes its deterministic structure, discovery, ranking, portability, and static safety tests. Its complete interactive workflow has also passed a live end-to-end trial. The Skill is ready for packaging and publication preparation from its local path. It has not been installed globally.

## Automated Tests

Command:

```bash
PYTHONPYCACHEPREFIX=/private/tmp/skill-scout-builder-pycache \
python3 -m unittest -v "validation/test_skill_scout_builder.py"
```

Result: 9 tests passed.

| Scenario | Expected behavior | Result |
| --- | --- | --- |
| High match | `skill-creator` ranks first for creating a Skill | Pass |
| Partial match | a video-cover Skill ranks first for Chinese and English cover terms | Pass |
| No match | an unrelated spectrometer request has no positive local match | Pass |
| Unsafe candidate | download-and-execute command is marked critical and returns failure | Pass |
| Simple safe candidate | no static findings and returns success | Pass |
| Structure | required metadata, references, scripts, and UI file exist | Pass |
| Host-adaptive workflow | core instructions do not require Codex-only discovery or creation tools | Pass |
| Cross-host roots | standard Agent Skills, Claude Code, and Codex directories are included | Pass |
| Cross-host discovery | the same Skill format is found across all three directory conventions | Pass |

## Cross-Agent Compatibility Checks

- Agent Skills-compatible directory format: pass.
- Codex CLI detected: `codex-cli 0.140.0-alpha.19`.
- Claude Code detected: `2.1.174`.
- Codex, Claude Code, and standard Agent Skills discovery roots: covered by regression tests.
- `agents/openai.yaml`: retained as an optional Codex enhancement; the portable core does not depend on it.
- Live Claude Code invocation: not run because it could use the user's authenticated account or incur external usage. Installation and invocation remain host-level acceptance checks.

## Real Environment Checks

### Local Skills

- Query: `create skill, skill creation`
- Result: local `skill-creator` ranked first.
- Query: `短视频封面, video cover, thumbnail`
- Result: local `cover-director` ranked first with a clear score lead.
- Query: `spectrometer calibration laboratory instrument`
- Result: zero positive candidates.

### Plugin Marketplaces

The Codex CLI reported three configured marketplaces:

- `openai-primary-runtime`
- `openai-bundled`
- `openai-curated`

### Official Curated Skills

The OpenAI Skills GitHub API was reachable and returned the current curated directory. The response included examples such as `cli-creator`, `linear`, `pdf`, `playwright`, `security-best-practices`, `speech`, and `transcribe`.

The bundled `list-skills.py` helper timed out in this environment, so the test used the official GitHub repository API as the fallback source.

### GitHub And Public Web Search

- GitHub repository contents were reachable.
- GitHub code search returned `401 Requires authentication` because `gh` is not installed and no authenticated code-search route was available.
- The general web-search route returned `403` during this run.

This is an expected operational boundary. The Skill is instructed to report unavailable channels and lower confidence rather than falsely claim complete coverage.

## Security Review

The final Skill directory was scanned by `scripts/audit_skill.py`.

- Critical findings: 0
- High findings: 0
- Medium findings: 0
- Low findings: 1

The low finding is the local scanner's read-only lookup of `/etc/codex/skills`, an official admin Skill location. The auditor skips its own rule definitions to avoid self-matching, and that skip is reported explicitly.

Manual review confirmed:

- no installation or environment mutation occurs during discovery
- no candidate code is executed during search
- the original candidate must remain unchanged
- consequential installation and credential use require approval
- a full audit and acceptance test are required on the final artifact

## Validation Limitation

The official `quick_validate.py` script could not start because its runtime dependency `PyYAML` is absent from both the system Python and the bundled Codex Python runtime. A temporary dependency installation was attempted earlier but the network request did not complete. Equivalent frontmatter checks passed with the system Ruby YAML parser, and the Python files passed compilation and unit tests. No `skills-ref` executable was present on this host.

An independent model-level conversational forward test was not launched because this session did not have user authorization to start subagents. The next validation step is an interactive trial using a real user need, covering requirement clarification, confirmation, search, comparison, user choice, execution, and final audit.

## Interactive End-to-End Trial

An interactive trial was completed in the main thread with this real need: download one public Douyin or Xiaohongshu link, save video or images plus caption metadata, and prefer no-watermark Douyin video.

The Skill successfully:

1. Asked focused clarification questions.
2. Produced and confirmed a structured requirement brief.
3. Searched local Skills, configured marketplaces, official sources, GitHub, and the available public-web route.
4. Reported unavailable search coverage rather than claiming full-web completion.
5. Found and inspected two GitHub candidates.
6. Recommended `zyipeng/video-downloader` as a 69% tailoring candidate.
7. Presented a requirement comparison and safety pre-screen.
8. Waited for the user to select tailoring.
9. Created and audited `douyin-xhs-downloader` with the upstream MIT license preserved.
10. Passed six offline tests, one real Xiaohongshu video download, and one real Xiaohongshu image-post download.

The live file was verified as an ISO MP4 with 5,167,843 bytes, and its metadata was verified after one iteration that removed duplicate topic suffixes and temporary share parameters.

The Xiaohongshu image-post test downloaded four valid 1080 x 1440 JPEG images and preserved the full article plus seven normalized hashtags.

The Douyin live test resolved a public short link, downloaded a valid 32,733,918-byte ISO MP4 through the preferred no-watermark source, and preserved the title, author, description, five hashtags, canonical URL, and source variant without credentials or Cookies.

This proves the complete `clarify -> search -> compare -> choose -> tailor -> audit -> test` workflow across all confirmed target media types. The Skill Scout Builder interactive trial is complete.
