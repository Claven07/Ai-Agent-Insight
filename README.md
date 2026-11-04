# AI Agent Insights

**Understand your agents. Optimize their intelligence.**

AI Agent Insights is a portable, cross-agent skill for analyzing AI agent execution data and producing evidence-based performance reports.

It helps developers understand what happened during an agent run, where time or tool activity was spent, which model requests failed, and what can be improved.

> **Current status:** Product foundation / pre-release. This repository is being prepared for an Agensi-compatible skill release. No marketplace listing or runtime instrumentation is implied by this repository alone.

## What it analyzes

- Session-level execution summaries and timing
- Tool invocation counts, outcomes, and durations
- LLM request attempts and failures
- Agent step counts and execution patterns
- Slow operations and likely bottlenecks
- Repeated or potentially unnecessary tool calls, when the input contains enough evidence

## What it produces

A structured performance audit containing:

1. Executive summary
2. Input coverage and data-quality notes
3. Session and agent statistics
4. Tool performance breakdown
5. LLM reliability analysis
6. Evidence-backed findings with severity
7. Prioritized optimization recommendations
8. Suggested next steps and measurement plan

## Design principles

- **Evidence first:** never invent metrics or imply unavailable telemetry exists.
- **Cross-agent:** analyze supplied or accessible data, not one vendor's private runtime.
- **Privacy-aware:** avoid reproducing secrets, credentials, tokens, or unnecessary personal data.
- **Read-only by default:** do not modify projects, execute supplied commands, or change agent settings.
- **Explicit limitations:** distinguish observed facts, derived calculations, hypotheses, and unknowns.
- **Useful outputs:** recommendations should be actionable and tied to supporting evidence.

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
│   └── RELEASE_PLAN.md
├── references/
│   ├── metrics-analysis.md
│   ├── bottleneck-detection.md
│   ├── llm-failure-analysis.md
│   └── report-standards.md
├── examples/
│   ├── sample-session.json
│   └── sample-performance-report.md
└── tests/
    └── validation-checklist.md
```

## Development status

| Area | Status |
|---|---|
| Product specification | In progress |
| Skill interface and workflow | In progress |
| Analysis references | Planned |
| Example dataset and report | Planned |
| Cross-agent testing | Planned |
| Agensi package validation | Planned |
| Marketplace submission | Not submitted |

## Compatibility

The intended deliverable is an instruction-based skill using a `SKILL.md` entry point and supporting Markdown/JSON files. Final compatibility must be tested against the current Agensi packaging requirements and at least two supported agent environments before release.

## License

MIT. See [LICENSE](LICENSE).
