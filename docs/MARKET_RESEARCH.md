# Marketplace positioning research — 2026-11-04

## Purpose

Define a defensible scope for AI Agent Insights by reviewing adjacent Agensi listings. Marketplace descriptions are competitive signals, not proof of implementation quality.

## Adjacent listings reviewed

### AI Observability Pro
https://www.agensi.io/skills/ai-observability-pro

Positioning: production observability design and diagnosis across traces, metrics, evaluations, SLOs, costs, incident workflows, instrumentation and rollout plans.

Boundary for AI Agent Insights: do not compete as an instrumentation architect or SLO/dashboard designer. Focus on forensic analysis of run evidence that already exists.

### Agent Reliability Audit
https://www.agensi.io/skills/agent-reliability-audit

Positioning: analyze raw agent traces and tool logs for loops, drift, latency hotspots and reliability failures across multiple runs; produce remediation reports.

Overlap: substantial. AI Agent Insights must avoid generic claims such as finding all hidden loops or providing a production-readiness audit without distinctive, testable methods.

Differentiation: explicit metric normalization and provenance, detailed session-level execution accounting, transparent handling of incomplete/mixed schemas, and first-class mapping for DeepSeek Harness Agent Insights metrics. Support cross-agent inputs where the source schema is available, but make no claim of universal parser coverage.

### AgentTrace MCP
https://www.agensi.io/skills/agenttrace-mcp-trace-runs-guard-schemas-catch-regressions

Positioning: trajectory reconstruction, MCP tool-schema validation, failure localization, and regression diffs.

Boundary: do not claim MCP schema validation, AgentTrace integration, or CI-ready regression gates unless separately implemented and tested.

### Benchmarking AI Agents Beyond Models
https://www.agensi.io/skills/benchmarking-ai-agents-beyond-models

Positioning: separate model capability from harness contribution through a benchmark protocol and task-set evaluation.

Boundary: AI Agent Insights analyzes run data; it is not a model evaluation suite, procurement benchmark, or universal model/harness score.

### AI Agent Product Analytics Workbench
https://www.agensi.io/skills/ai-agent-product-analytics-workbench

Positioning: determine whether an agent completed the user's task by connecting tool actions, product state, user effort and outcomes.

Boundary: do not claim product analytics or verified business outcome measurement from execution telemetry alone.

### AI Skill Performance Quality Auditor
https://www.agensi.io/skills/ai-skill-performance-quality-auditor

Positioning: evaluate agent behavior against a skill definition and expected behavior specification, generating alignment scorecards and regression tests.

Boundary: AI Agent Insights does not grade answer quality or prompt/spec alignment unless the user supplies a separate evaluation rubric and asks for that distinct analysis.

### Cut Context
https://www.agensi.io/skills/cut-context

Positioning: Claude Code-specific local session log analysis and token/context cost attribution.

Boundary: do not claim exact token or cost attribution for an agent whose log format and token records are unavailable. AI Agent Insights remains input-driven and cross-agent at the conceptual schema level.

## Positioning statement

AI Agent Insights is a cross-agent, evidence-first run performance profiler. It turns existing session exports, event traces, tool-call records and structured metrics into a transparent execution report: what happened, what can be measured, where the observed time/failures occurred, what remains unknown, and what to validate next.

## Differentiation that must be demonstrated in tests

1. Metric provenance: every value has a source field or visible calculation.
2. Comparability checks: it refuses unjustified run-to-run comparisons.
3. Session accounting: it distinguishes wall-clock duration, summed operation time, and concurrent spans.
4. Failure accounting: it distinguishes attempts, logical requests, retries, cancellations and failures when IDs allow.
5. Honest uncertainty: it will not invent missing telemetry, root causes, token usage, costs or benchmark scores.
6. DSH-native compatibility: it correctly interprets the existing dsh-plugin-agent-insights output without requiring the plugin for other input types.

## Market claims

The marketplace page showed a broad AI Agents & LLM Ops category and several adjacent listings on 2026-11-04. Category counts and listing order can change; do not hardcode them in product or listing copy.

The public Agensi docs currently describe the ZIP/SKILL.md packaging model, frontmatter listing fields, file limits and eight-part security review. Recheck before submission:
- https://www.agensi.io/docs/packaging
- https://www.agensi.io/docs/submit-on-the-website
- https://www.agensi.io/docs/review-and-approval
