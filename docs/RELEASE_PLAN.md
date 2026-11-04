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
- [ ] Add additional partial, malformed, duplicate, and multi-run fixtures.

## Phase 4 — Validation
- [x] Verify required SKILL.md frontmatter fields are present.
- [x] Verify all referenced methodology files exist.
- [x] Parse the supplied JSON fixtures and inspect expected retry counts.
- [ ] Validate YAML frontmatter with a standards-compliant parser.
- [ ] Test complete, partial, and malformed input cases.
- [ ] Test secret redaction and prompt-injection resistance in an agent.
- [ ] Test with at least two compatible agent environments.
- [ ] Review all marketplace claims and metadata.

## Phase 5 — Marketplace release
- [ ] Confirm creator account and publishing eligibility.
- [ ] Prepare final ZIP package.
- [ ] Inspect ZIP contents and file types.
- [ ] Run Agensi security and submission checks.
- [ ] Set initial listing price to free.
- [ ] Submit for review after owner approval.
- [ ] Record listing URL and approved version after publication.

## Release gates

No release is considered ready merely because the Markdown files exist. Release requires package validation, functional scenario testing, security review, and confirmation that the target marketplace requirements are current.
