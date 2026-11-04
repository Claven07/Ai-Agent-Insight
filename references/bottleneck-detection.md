# Bottleneck Detection Guidance

## Purpose

Identify operations that plausibly dominate agent execution time or create repeated work, while avoiding unsupported causal claims.

## Evidence hierarchy

1. Direct per-operation duration measurements.
2. Valid timestamped event sequences.
3. Repeated patterns across comparable runs.
4. Aggregate counts and summary metrics.
5. User-provided qualitative descriptions.

Higher-level evidence can support investigation, but should not be presented as a measured timing bottleneck.

## Candidate patterns

- One tool call with unusually high measured duration.
- Repeated slow calls to the same tool.
- High failure rates for a tool or request category.
- Repeated equivalent calls where inputs and outputs support equivalence.
- Long gaps between events, only when timestamps and event semantics permit interpretation.
- High tool-call volume relative to completed agent tasks, only when task boundaries are known.

## Ranking

For each candidate, record:
- Observed evidence.
- Number of affected calls or runs.
- Measured duration or frequency.
- Potential impact.
- Confidence.
- Validation needed.

Do not rank by a fabricated composite score. If a heuristic ranking is useful, explain its inputs and that it is not a benchmark score.

## Recommendations

Prefer testable recommendations, such as:
- Cache a demonstrably repeated deterministic lookup.
- Reduce duplicate calls after verifying equivalence.
- Add timeout or retry policy when failure patterns support it.
- Profile a suspected slow tool before rewriting it.
- Improve instrumentation where current data cannot localize the delay.

Never recommend suppressing retries or reducing tool usage without considering correctness and task success.
