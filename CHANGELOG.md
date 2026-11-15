# Changelog

All notable changes to AI Agent Insights are documented here.

## 0.1.0 — Initial development foundation

- Initialize repository and product specification.
- Add the Agensi-compatible root SKILL.md and supported listing metadata.
- Define evidence-first run forensics, session accounting, and comparison boundaries.
- Add analysis references for metrics, bottlenecks, LLM failures, reporting, and input normalization.
- Document marketplace positioning and adjacent products.
- Add synthetic successful and timeout/retry fixtures with example reports.
- Add expected-behavior scenarios and release validation checklist.

## Unreleased

- Complete six manual validation tests across Codex, VS Code, and Antigravity; all 18 agent/test combinations are owner-reported as passing.
- Add concurrency and partial-timestamp analysis acceptance checks.
- Strengthen evidence rules against fabricated intervals, unsupported retry classification, and cross-layer duration addition.
- Continue release-candidate verification: confirm current CI/package build, archive detailed per-agent test evidence, run Agensi security checks, and submit for marketplace review only after owner approval.
