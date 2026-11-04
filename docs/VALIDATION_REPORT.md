# Validation Report — 2026-11-04

## Current result

**Static validation and package build: PASS**  
**Cross-agent behavioral validation: NOT RUN**  
**Agensi upload/security scan: NOT RUN**  
**Marketplace approval: NOT submitted**

## GitHub Actions evidence

- Workflow: Validate AI Agent Insights
- Run: https://github.com/Claven07/Ai-Agent-Insight/actions/runs/41830302750
- Run ID: 41830302750
- Commit: 0bb6eed7c77c1c50777bf119c8289cfa9d6b5125
- Runner: windows-latest
- Result: success

Completed steps:
1. Checkout repository.
2. Set up Python 3.12.
3. Install PyYAML validation dependency.
4. Parse and validate SKILL.md frontmatter.
5. Check linked methodology files exist and are in the package allowlist.
6. Parse both synthetic JSON fixtures and verify retry-accounting expectations.
7. Run local package-source preflight for UTF-8 text, known secret patterns, selected prompt-injection scan signals, and selected dangerous-command patterns.
8. Build ZIP and validate archive integrity, root SKILL.md, file paths, file types, file count, and website-upload size.
9. Upload GitHub Actions artifact.

## Package inspection

The generated marketplace ZIP contains exactly seven entries:

- SKILL.md
- LICENSE
- references/metrics-analysis.md
- references/bottleneck-detection.md
- references/llm-failure-analysis.md
- references/report-standards.md
- references/input-normalization.md

Inspection result:
- ZIP CRC check: passed.
- Root SKILL.md count: one.
- File count: seven.
- File types: UTF-8 text.
- Compressed package size: 12,619 bytes.
- Known local preflight patterns: no matches.

Development docs, sample datasets, and test prompts are intentionally excluded from the marketplace upload.

## Fixture checks

### Successful session fixture
- 12,000 ms session duration.
- Three steps.
- Three tool calls.
- run_tests is the longest supplied tool call at 4,100 ms.

### Retry and failure fixture
- Three tool attempts: two successful, one failed.
- Two logical tool operations.
- Two LLM attempts linked to one logical request.
- run_tests is the longest supplied tool call at 4,500 ms.
- Attempt-level tool success rate: 2/3 (66.7%); not a task-completion rate.

## Current Agensi requirement check

Based on the current public packaging guide and review documentation checked on 2026-11-04:
- A ZIP upload is used.
- The main SKILL.md must have a name; every skill needs a description.
- summary, version, tags, keywords, use_cases, and docs_url are read as optional listing metadata.
- Website upload limit: 50 MB and 1,000 files.
- A package with one SKILL.md is one skill; multiple SKILL.md files make a skill pack.
- The security review checks file structure, file types, dangerous commands, secrets, environment harvesting, network access, obfuscation, and prompt injection.
- An automated scan is followed by AI and human review for new listings.

This report records our local preflight, not Agensi's own security verdict. Agensi's scan can warn or fail for signals beyond the local patterns tested here.

## Outstanding release gates

1. Load the skill in at least two compatible agent environments.
2. Run every prompt in tests/manual-agent-test-prompts.md and record actual outputs.
3. Add regression fixtures for partial, malformed, duplicate, and incomparable runs.
4. Re-check marketplace metadata and package rules immediately before submission.
5. Upload from the Creator Dashboard and review the actual Agensi security scan.
6. Submit only after owner review of the uploaded listing and scan report.
