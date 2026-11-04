# Implementation and Release Plan

## Phase 0 — Repository foundation
- [x] Create public repository.
- [x] Add product specification.
- [x] Define safety and evidence principles.
- [ ] Verify current Agensi packaging requirements.
- [ ] Inspect representative marketplace skill packages.

## Phase 1 — Skill contract
- [ ] Write `SKILL.md` with valid frontmatter.
- [ ] Define activation description and scope boundaries.
- [ ] Implement the complete analysis workflow.
- [ ] Link supporting reference documents.

## Phase 2 — Analysis methodology
- [ ] Define metric formulas and aggregation rules.
- [ ] Document duration and concurrency caveats.
- [ ] Define bottleneck ranking rules.
- [ ] Define LLM failure classification limits.
- [ ] Define evidence, confidence, and severity standards.

## Phase 3 — Examples and fixtures
- [ ] Create synthetic sample session data.
- [ ] Create complete example report.
- [ ] Include partial, malformed, duplicate, and mixed-unit fixtures.
- [ ] Ensure all example data is synthetic and contains no real credentials.

## Phase 4 — Validation
- [ ] Validate SKILL.md frontmatter and package structure.
- [ ] Test complete and incomplete input cases.
- [ ] Test malformed JSON and ambiguous units.
- [ ] Test secret redaction.
- [ ] Test prompt-injection resistance in logs.
- [ ] Test with at least two compatible agent environments.
- [ ] Review all marketplace claims and metadata.

## Phase 5 — Marketplace release
- [ ] Confirm creator account and publishing eligibility.
- [ ] Prepare ZIP package.
- [ ] Run Agensi's current security and submission checks.
- [ ] Set initial listing price to free.
- [ ] Submit for review.
- [ ] Record listing URL and approved version after publication.

## Release gates

No release is considered ready merely because the Markdown files exist. Release requires package validation, functional scenario testing, security review, and confirmation that the target marketplace requirements are current.
