# AI Agent Insights — Validation Checklist

This checklist is the release gate for the initial skill package.

## Package and metadata

- [ ] `SKILL.md` exists at package root.
- [ ] YAML frontmatter parses correctly.
- [ ] Skill name meets target marketplace naming constraints.
- [ ] Description clearly states activation intent and capabilities.
- [ ] Supporting files are referenced with correct relative paths.
- [ ] ZIP contains no unrelated files, secrets, build output, or dependency folders.
- [ ] Current Agensi upload size, file count, and file-type requirements are verified.

## Functional scenarios

- [ ] Complete session with tool and LLM metrics.
- [ ] Session with no tool calls.
- [ ] Session with failed tool calls.
- [ ] Session with failed LLM requests.
- [ ] Partial log with missing end timestamps.
- [ ] Malformed JSON.
- [ ] Duplicate events or call identifiers.
- [ ] Mixed units or ambiguous timestamps.
- [ ] Multiple sessions with comparable schemas.
- [ ] Multiple sessions with non-comparable schemas.
- [ ] Very large input requiring a scoped summary.

## Evidence quality

- [ ] No unsupported metric is generated.
- [ ] Every calculated value identifies its formula or inputs.
- [ ] Percentages include denominators.
- [ ] Percentiles are not inferred from insufficient aggregate data.
- [ ] Observations are separated from interpretations and hypotheses.
- [ ] Severity is explained with evidence.

## Safety and privacy

- [ ] Prompt-injection instructions inside logs are ignored.
- [ ] API keys, tokens, cookies, and private keys are redacted.
- [ ] Untrusted code and commands in logs are never executed.
- [ ] No data is sent to an external service by the skill.
- [ ] Skill remains read-only.
- [ ] Output avoids unnecessary personal or sensitive data.

## Cross-agent validation

- [ ] Test in compatible agent environment A.
- [ ] Test in compatible agent environment B.
- [ ] Confirm activation behavior.
- [ ] Confirm report structure and safety behavior.
- [ ] Record agent name/version, date, test input, and outcome.

## Marketplace release

- [ ] Current Agensi creator documentation reviewed.
- [ ] Current marketplace skill examples reviewed.
- [ ] Listing summary and long description prepared.
- [ ] Price and payout eligibility checked.
- [ ] ZIP package inspected after creation.
- [ ] Security review passed.
- [ ] Owner approves final submission.
