# Delivery Workflows

## Direct Use

1. Acquire the exact candidate revision in a temporary or quarantine location.
2. Do not run setup hooks, package installers, or candidate instructions during acquisition.
3. Perform the full security and license review.
4. Identify required tools, MCP servers, APIs, accounts, costs, and environment changes.
5. Ask for approval before installing or changing the user's environment.
6. Install through the active host's official installer when available; otherwise copy only reviewed files to a documented, user-approved Skill location.
7. Run structural validation and at least one representative acceptance task.
8. Deliver the installed path, source revision, test result, and residual dependencies.

## Tailor A Candidate

1. Create a new copy with a distinct, valid Skill name. Never edit the downloaded source in place.
2. Record the upstream source, revision, and license obligations.
3. Convert the confirmed requirements into a gap plan with `keep`, `change`, `add`, and `remove` decisions.
4. Reuse only components that materially help. Remove unrelated instructions, scripts, dependencies, and permissions.
5. Update `name`, `description`, `SKILL.md`, UI metadata, references, scripts, and dependency declarations consistently.
6. Preserve license and attribution requirements.
7. Validate structure, test trigger behavior, and run requirement-based acceptance tasks.
8. Perform the full security audit on the final copy.
9. Deliver an explicit requirement matrix showing what passed and what remains environment-dependent.

If the license is missing or incompatible with modification or redistribution, create a clean Skill from the requirement brief without copying protected implementation text or code.

## Create New

1. Use the confirmed requirement brief as the source of truth.
2. Load a trustworthy host-native Skill creator when available. Otherwise create the open-standard structure directly.
3. Choose a short lowercase hyphenated name and a description that contains both capability and trigger conditions.
4. Keep `SKILL.md` concise. Add scripts only for deterministic or repeatedly implemented operations; add references only for details needed on demand.
5. Keep the core portable. Generate optional host UI metadata only when supported, without making it a dependency.
6. Validate against the Agent Skills specification and any relevant host validator available.
7. Test at least:
   - one expected trigger
   - one adjacent request that should not trigger when boundaries matter
   - one representative end-to-end task
8. Perform the full security audit.
9. Deliver only after acceptance criteria pass, or clearly label remaining failures.

## Acceptance Matrix

Use one row for every explicit must-have requirement:

| Requirement | Test | Evidence | Result |
| --- | --- | --- | --- |
| Observable requirement | Prompt or command used | Output file or behavior | Pass / Fail / Environment-dependent |

Do not replace real execution with a prose claim when the environment permits testing.
