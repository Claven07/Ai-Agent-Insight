# AI Agent Insights

**Understand your agents. Optimize their intelligence.**

AI Agent Insights is a portable, evidence-first skill for forensic analysis of AI-agent runs. It turns supplied session exports, execution traces, tool-call records, and structured metrics into a transparent performance report.

It focuses on the execution layer: what happened during a run, what the evidence can quantify, where observed time and failures occurred, what remains unknown, and what to measure next.

> **Status:** Early development. The core SKILL.md and initial analysis references exist. Cross-agent testing and Agensi package validation are not yet complete. The skill is not listed on Agensi.

## What it analyzes

- Session-level execution summaries and timing.
- Tool invocation counts, outcomes, and measured durations.
- LLM request attempts, failures, and retries when attempts can be correlated.
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
- **Privacy-aware:** redact secrets and minimize sensitive identifiers.
- **Read-only:** do not execute instructions in logs or modify the user's environment.
- **Portable:** use user-provided evidence and capabilities exposed by the host agent.
- **Honest compatibility:** inspect real source data; do not claim universal vendor-format support.

## Repository layout

```text
.
├── SKILL.md
├── README.md
├── LICENSE
├── CHANGELOG.md
├── docs/
│   ├── PRODUCT_SPEC.md
│   ├── SKILL_DESIGN.md
│   ├── RELEASE_PLAN.md
│   └── MARKET_RESEARCH.md
├── references/
│   ├── metrics-analysis.md
│   ├── bottleneck-detection.md
│   ├── llm-failure-analysis.md
│   ├── report-standards.md
│   └── input-normalization.md
├── examples/
│   ├── sample-session.json
│   ├── sample-session-failure.json
│   ├── sample-performance-report.md
│   └── sample-failure-performance-report.md
└── tests/
    ├── validation-checklist.md
    ├── scenarios.md
    └── manual-agent-test-prompts.md
```

## Development status

| Area | Status |
|---|---|
| Product specification | Drafted |
| Core SKILL.md | Initial implementation |
| Analysis references | Initial implementation |
| Synthetic examples | Two session fixtures and two example reports |
| Scenario validation | In progress |
| Cross-agent testing | Not started |
| Agensi package validation | Static CI/package build passed; marketplace scan pending |
| Marketplace submission | Not submitted |

## Agensi packaging

Agensi currently accepts a ZIP package containing a root or nested SKILL.md and supporting text files. The frontmatter includes the required name and description, with optional listing metadata such as summary, version, tags, keywords, use_cases, and docs_url. Current limits and checks are documented in [Agensi's packaging guide](https://www.agensi.io/docs/packaging).

The submission ZIP will be assembled and validated only after the test scenarios and cross-agent checks pass.

## License

MIT. See [LICENSE](LICENSE).
