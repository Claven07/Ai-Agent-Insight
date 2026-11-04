# Performance Report Standards

## Required structure

# AI Agent Performance Audit

## 1. Executive summary
State the overall picture in plain language. Do not use a numeric score unless a documented and validated scoring system exists.

## 2. Scope and data coverage
List files/sources, time range, run count, available fields, missing fields, and parsing issues.

## 3. Session overview
Show supplied and validly calculated counts/durations with units and source notes.

## 4. Tool performance
Summarize tool call counts, outcomes, and duration evidence. Identify slow operations only when duration data exists.

## 5. LLM reliability
Summarize request outcomes and evidenced error categories. Distinguish attempts from logical requests.

## 6. Agent execution patterns
Describe step/event patterns only when ordering and event semantics support them.

## 7. Findings
For each finding include:
- ID and title.
- Severity.
- Evidence type: observed, calculated, interpretation, or hypothesis.
- Evidence and source.
- Confidence.
- Impact and limitations.

## 8. Recommendations
For each recommendation include:
- Priority.
- Action.
- Evidence-based rationale.
- Expected observable effect (not a promised result).
- Validation method.

## 9. Follow-up measurement plan
Specify what to capture and compare in the next run.

## Severity definitions

- **Critical:** strong evidence of severe correctness, reliability, or security impact.
- **High:** substantial measured failure or performance impact.
- **Medium:** recurring or meaningful issue with bounded impact.
- **Low:** minor improvement opportunity.
- **Informational:** useful context without a direct action.

## Writing standards

- Be specific and concise.
- State units.
- Show denominators for percentages.
- Include sample sizes where relevant.
- Never fabricate missing statistics.
- Avoid causal language when only correlation or timing is observed.
- Separate facts, calculations, interpretation, and hypotheses.
- Do not expose sensitive identifiers or secrets.
