# Requirements And Scoring

## Requirement Brief

Collect only fields that affect discovery, implementation, or acceptance.

| Field | Meaning | Required |
| --- | --- | --- |
| Goal | The outcome the user wants | Yes |
| Trigger | What the user is likely to say or provide | Usually |
| Inputs | Files, links, text, services, or context | When relevant |
| Outputs | The concrete deliverable | Yes |
| Workflow | Essential stages or decisions | Yes |
| Environment | Agent host, OS, repository, platform | When relevant |
| Integrations | APIs, MCP, apps, accounts, external tools | When relevant |
| Constraints | Privacy, language, cost, speed, no-go actions | When relevant |
| Examples | One representative real task | Strongly preferred |
| Acceptance | Observable evidence that the Skill worked | Yes |

Mark each statement as one of:

- `explicit`: directly stated by the user
- `inferred`: safe working assumption; show it during confirmation
- `unknown`: material gap requiring one focused question

Stop questioning when remaining unknowns would not materially change search terms, candidate selection, implementation, or acceptance tests.

## Candidate Evidence

Accept capability evidence only from inspectable sources:

- `SKILL.md` instructions and metadata
- bundled scripts and references
- plugin manifest and declared dependencies
- repository documentation when consistent with the actual files
- tests or examples that demonstrate the behavior

Do not treat repository names, tags, stars, search snippets, or promotional claims as proof.

## Weighted Score

Score each category from 0 to 5, then calculate the weighted percentage.

| Category | Weight | Question |
| --- | ---: | --- |
| Goal and output fit | 30 | Does it produce the required outcome? |
| Workflow fit | 20 | Does its process match the must-have stages? |
| Inputs and integrations | 15 | Can it accept the required inputs and use available tools? |
| Environment compatibility | 10 | Can it run in the user's actual environment? |
| Adaptability | 10 | Are gaps local and straightforward to change? |
| Evidence and maintainability | 5 | Are files, docs, tests, and ownership inspectable? |
| Safety and trust | 10 | Is the source auditable with acceptable permissions and provenance? |

Use this formula:

`score = sum((category_score / 5) * category_weight)`

Apply hard gates after scoring:

- Exclude from direct use if the contents cannot be inspected.
- Exclude from direct use if critical dependencies are unavailable.
- Exclude from recommendation when severe unresolved security findings exist.
- Do not redistribute a tailored copy when its license forbids it or cannot be established.

## Recommendation Bands

Use bands as guidance, not a substitute for evidence.

- `85-100`: strong direct-use candidate if all hard gates pass
- `65-84`: likely tailoring candidate
- `40-64`: use only for isolated reusable ideas; usually create new
- `0-39`: reject

Even a high total score may require tailoring when one explicit must-have requirement is missing. State that exception clearly.

## Comparison Format

Keep the user-facing comparison compact:

| Requirement | Candidate evidence | Status |
| --- | --- | --- |
| One requirement per row | File or behavior proving it | Met / Partial / Missing |

After the table, state:

- overall fit percentage
- critical gaps
- required dependencies
- recommendation and reason
- confidence based on channels searched and evidence inspected
