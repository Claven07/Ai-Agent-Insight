# Metrics Analysis Methodology

## General rules

- Preserve the original metric name and unit.
- Record the source field or event used for every reported value.
- Do not infer missing values as zero.
- Distinguish a count of events from a count of unique operations.
- Distinguish attempted, completed, successful, failed, cancelled, and timed-out operations.
- State the sample size and time window when available.

## Duration

Prefer an explicit measured duration supplied by the source. If calculated from timestamps, require compatible timestamp units and a valid start/end pair.

Formula:

`duration = end_timestamp - start_timestamp`

Reject or flag negative durations. Do not assume timezone semantics for naive timestamps without source context.

Do not sum nested or concurrent durations and label the result as wall-clock elapsed time.

## Rates

A success rate may be calculated only when the denominator is known:

`success_rate = successful_count / eligible_completed_count * 100`

State the exact denominator. Exclude unknown or pending outcomes unless the source's definition explicitly includes them.

A failure rate must not combine request failures, tool failures, cancellations, and timeouts without explicitly defining the combined population.

## Latency distributions

Report percentiles only when individual observations or a valid pre-aggregated distribution is supplied. Never estimate p95/p99 from a minimum, maximum, and average.

For small samples, show sample count and avoid overstating statistical significance.

## Comparisons

Compare sessions only when:
- Units match.
- Metric definitions match.
- Measurement boundaries are comparable.
- Sampling and filtering are sufficiently similar.

Otherwise present side-by-side values with a comparability warning instead of declaring one faster or better.

## Missing and inconsistent data

Flag missing fields, duplicate identifiers, contradictory statuses, malformed timestamps, mixed units, and suspiciously impossible values. Explain how these affect conclusions.

## DeepSeek Harness mapping

When available, the DSH Agent Insights plugin may provide:
- totalToolCalls
- successfulToolCalls
- failedToolCalls
- toolExecutions with durationMs and outcome fields
- slowestTool
- totalSteps
- totalLlmRequests
- failedLlmRequests
- sessionStartTime
- sessionDurationMs

These are examples of one source schema, not universal fields. Preserve that distinction in reports.
