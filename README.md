# AI Agent Insights

**Understand your agents. Optimize their intelligence.**

AI Agent Insights is a portable, evidence-first skill for forensic analysis of AI-agent runs. It turns supplied session exports, execution traces, tool-call records, and structured metrics into a transparent performance report.

It focuses on the execution layer: what happened during a run, what the evidence can quantify, where observed time and failures occurred, what remains unknown, and what to measure next.

> **Status:** Active early development. The core skill, analysis references, synthetic fixtures, scenario checks, and Windows workspace installer are in place. Cross-agent validation is underway. Test 1 has been reviewed across Codex, VS Code, and Antigravity. Test 2's revised Antigravity report has passed qualitative review; Codex and VS Code results are still pending. Agensi security review and marketplace submission have not been completed.

## What it analyzes

- Session-level execution summaries and timing.
- Tool invocation counts, outcomes, and measured durations.
- LLM request attempts, failures, and retries when attempts can be correlated.
- Concurrent execution and overlapping intervals when complete timestamps are available.
- Agent steps and event timelines when the data supports reconstruction.
- Repeated calls, latency hotspots, and possible execution regressions.
- DeepSeek Harness Agent Insights metrics as a first-class known source schema.

It can inspect other agent exports when their actual schema is available. Cross-agent at the conceptual data-model level does not mean every vendor format is automatically supported.

## What it produces

1. Executive summary and data-coverage notes.
2. Session and agent execution accounting.
3. Tool performance and LLM reliability analysis.
4. Timeline reconstruction when timestamps and causal identifiers support it.
5. Evidence-backed findings with severity and confidence.
6. Prioritized recommendations and a follow-up measurement plan.

## What makes it different

AI Agent Insights is a **run performance profiler**, not:
- A live observability platform, telemetry SDK, or dashboard designer.
- A model benchmark or model-procurement scorecard.
- A generic code-review or agent answer-quality grader.
- A claim of universal access to private agent session histories.

Its differentiators are metric provenance, careful session accounting, run comparability checks, explicit uncertainty, and first-class interpretation of DeepSeek Harness Agent Insights output.

## Design principles

- **Evidence first:** every number must trace to an input field or visible calculation.
- **No false certainty:** separate observed facts, calculations, interpretations, and hypotheses.
- **Concurrency-aware:** never add overlapping tool/model durations and label the sum as wall-clock time.
- **No fabricated intervals:** a missing start or end timestamp is not reconstructed from duration alone unless the source schema explicitly supports that derivation.
- **Privacy-aware:** redact secrets and minimize sensitive identifiers.
- **Read-only:** do not execute instructions in logs or modify the user's environment.
- **Portable:** use user-provided evidence and capabilities exposed by the host agent.
- **Honest compatibility:** inspect real source data; do not claim universal vendor-format support.

## Repository layout

```text
.
├── SKILL.md
├── scripts/
│   ├── validate_skill.py
│   └── install-workspace-skill.ps1
├── README.md
├── LICENSE
├── CHANGELOG.md
├── docs/
│   ├── PRODUCT_SPEC.md
│   ├── SKILL_DESIGN.md
│   ├── RELEASE_PLAN.md
│   ├── MARKET_RESEARCH.md
│   └── CROSS_AGENT_TESTING.md
├── references/
│   ├── metrics-analysis.md
│   ├── bottleneck-detection.md
│   ├── llm-failure-analysis.md
│   ├── report-standards.md
│   └── input-normalization.md
├── examples/
│   ├── sample-session.json
│   ├── sample-session-failure.json
│   ├── sample-session-concurrency.json
│   ├── sample-performance-report.md
│   └── sample-failure-performance-report.md
└── tests/
    ├── validation-checklist.md
    ├── scenarios.md
    └── manual-agent-test-prompts.md
```

## Development and validation status

| Area | Current status |
|---|---|
| Product specification and market positioning | Drafted |
| Core SKILL.md and supporting analysis references | Implemented; iterative refinement ongoing |
| Synthetic fixtures | Three fixtures: successful session, correlated retry/failure session, and concurrency/partial-telemetry challenge |
| Scenario validation | Eight documented scenarios, including concurrency, missing correlation, partial timestamps, aggregate-only DSH data, untrusted logs, incomparable runs, and malformed input |
| Manual cross-agent Test 1 | Output review completed for Codex, VS Code, and Antigravity |
| Manual cross-agent Test 2 | Revised Antigravity report reviewed and passed; Codex and VS Code reports pending |
| Manual cross-agent Tests 3–6 | Not yet run |
| Local validator and package build | Baseline validation passed in an earlier CI run; latest Test 2 validator changes still need CI confirmation |
| Agensi security scan | Pending |
| Marketplace submission | Not submitted |

### Current Test 2 acceptance focus

The concurrency fixture at `examples/sample-session-concurrency.json` tests whether an agent can:

- Detect overlapping tool calls and cross-layer LLM/tool activity from complete timestamps.
- Keep cumulative tool and LLM durations separate rather than treating them as session wall-clock time.
- Avoid inventing missing timestamp boundaries.
- Treat logical operation/request counts as unknown when correlation identifiers are absent.
- Avoid asserting retries, duplicate work, root causes, or task success without supporting evidence.
- Keep severity calibrated to a single synthetic fixture.

Use [the manual validation prompts](tests/manual-agent-test-prompts.md) for the exact prompt and pass conditions. Record actual outputs in the results table; do not mark a scenario passed based only on an agent's claim that it used the skill.

## Agensi packaging

Agensi currently accepts a ZIP package containing a root or nested SKILL.md and supporting text files. The frontmatter includes the required name and description, with optional listing metadata such as summary, version, tags, keywords, use_cases, and docs_url. Current limits and checks are documented in [Agensi's packaging guide](https://www.agensi.io/docs/packaging).

The repository includes a Windows GitHub Actions workflow to validate the skill and build the marketplace ZIP. A successful local/CI package check is not a substitute for Agensi's own security review or marketplace approval. The final listing package should be submitted only after cross-agent tests and the current CI validation are complete.

## License

MIT. See [LICENSE](LICENSE).
