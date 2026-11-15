# Implementation and Release Plan

## Phase 0 — Repository foundation
- [x] Create public repository.
- [x] Add product specification.
- [x] Define evidence-first analysis scope.
- [x] Verify current Agensi packaging requirements.
- [x] Inspect representative marketplace skill packages.
- [x] Record competitor boundaries and product positioning.

## Phase 1 — Skill contract
- [x] Write root SKILL.md with required name and description frontmatter.
- [x] Add listing metadata fields supported by Agensi.
- [x] Define activation intent and product boundaries.
- [x] Implement the analysis workflow and default report contract.
- [x] Link supporting methodology documents.

## Phase 2 — Analysis methodology
- [x] Define metric provenance and calculation rules.
- [x] Document duration, concurrency, and percentile caveats.
- [x] Define bottleneck evidence and ranking rules.
- [x] Define LLM failure and retry interpretation.
- [x] Define evidence types, severity, and redaction standards.
- [x] Document DSH-native fields and retention caveats.

## Phase 3 — Examples and fixtures
- [x] Create synthetic successful-session data.
- [x] Create synthetic timeout/retry data.
- [x] Create example performance reports.
- [x] Define expected behavior for core edge-case scenarios.
- [x] Prepare manual test prompts for cross-agent validation.
- [x] Add shared Windows PowerShell workspace installer for Codex and Antigravity.
- [x] Add setup and manual-testing instructions for Codex and Antigravity IDE.
- [x] Verify shared workspace installation in Windows CI.
- [ ] Add additional partial, malformed, duplicate, and multi-run fixtures.

## Phase 4 — Validation
- [x] Verify required SKILL.md frontmatter fields are present.
- [x] Verify all referenced methodology files exist.
- [x] Parse the supplied JSON fixtures and inspect expected retry counts.
- [x] Validate YAML frontmatter with a standards-compliant parser (PyYAML in Windows CI).
- [x] Complete, partial-timestamp/concurrency, aggregate-only DSH, untrusted-log, incompatible-run, and no-evidence manual cases reported passing across Codex, VS Code, and Antigravity (18/18 owner-reported passes).
- [ ] Run a dedicated malformed JSON / truncated JSONL case and archive the results.
- [x] Untrusted-log / prompt-injection handling reported passing across Codex, VS Code, and Antigravity (Test 4; owner-reported).
- [ ] Archive the detailed test outputs, exact agent/provider versions, and execution dates.
- [x] Run all six manual tests in three environments (Codex, VS Code, Antigravity): 18/18 owner-reported passes.
- [ ] Review all marketplace claims and metadata.

## Phase 5 — Marketplace release
- [x] Confirm creator account and publishing eligibility.
- [x] Submit the six-file Agensi skill package.
- [x] Prepare listing name, summary, Markdown description, sample input/output, compatibility note, categories, use cases, limitations, and FAQ.
- [x] Declare read-only file scope and no external hosts or additional tools.
- [x] Set initial price to $4.99 one-time.
- [x] Submit after owner approval.
- [x] Pass Agensi security review.
- [x] Confirm marketplace listing is live.
- [x] Record listing URL: https://agensi.io/skills/ai-agent-insights
- [x] Record published version: 0.1.0

## Phase 6 — Post-launch maintenance
- [ ] Confirm GitHub Actions validation on the latest `main` revision.
- [ ] Archive detailed per-agent test reports, exact provider/model versions, and execution dates.
- [ ] Run and record a dedicated malformed JSON / truncated JSONL validation case.
- [ ] Monitor Agensi uses, reviews, and buyer feedback.
- [ ] Prioritize and validate improvements for the next version.
- [ ] Publish future updates with an incremented version and changelog.

## Release record

- Marketplace: https://agensi.io/skills/ai-agent-insights
- Status: Live
- Security: Approved
- Version: 0.1.0
- Price: $4.99 one-time

The initial public release is complete. Remaining checklist items are post-launch maintenance and reproducibility improvements, not blockers to the already-live listing.
