# Input normalization and source coverage

## Supported input patterns

The skill can analyze supplied examples of the following, subject to actual field coverage:

- DSH Agent Insights JSON snapshots.
- General JSON session summaries.
- JSONL/NDJSON event streams.
- Tool-call records with outcomes and duration.
- LLM request records with outcome, error and duration.
- OpenTelemetry-like span exports when trace/span relationships and timestamps are present.
- Redacted text logs with recognizable timestamps and event boundaries.

This is a conceptual compatibility list, not a guarantee that every vendor's export format is supported. Inspect samples and document the fields actually recognized.

## Generic event mapping

| Concept | Common aliases (examples only) |
|---|---|
| Session/run ID | session_id, sessionId, run_id, runId, trace_id |
| Event time | timestamp, time, ts, start_time, started_at |
| End time | end_time, ended_at, finish_time |
| Duration | duration, duration_ms, durationMs, latency_ms |
| Operation name | name, tool, tool_name, operation, span_name |
| Outcome | status, result, outcome, isError, success |
| Error | error, exception, error_message, message |
| Parent relation | parent_id, parent_span_id, parent_call_id |
| Model | model, model_name, provider_model |
| Tokens | input_tokens, prompt_tokens, output_tokens, completion_tokens, total_tokens |

Never map a field based on its name alone if its meaning is ambiguous. Confirm using examples and surrounding structure.

## DSH Agent Insights source mapping

The DSH plugin's session snapshot fields can include:
- Session: sessionId, sessionStartTime, sessionDurationMs.
- Agent: totalSteps, totalLlmRequests, failedLlmRequests.
- Tools: totalToolCalls, successfulToolCalls, failedToolCalls, toolExecutions, slowestTool.

A snapshot with aggregate counts cannot reconstruct individual timestamps or missing call records. A per-tool execution list can support a more detailed breakdown only for the records it actually contains. A bounded history may omit older tool calls; check whether totals and retained records disagree.

## Time normalization

- Identify whether timestamps are epoch seconds, epoch milliseconds, or ISO strings.
- Convert only after the source unit is identified.
- Preserve timezone offsets.
- Do not assume a timezone for naive local timestamps.
- Flag negative durations and start/end inversions.
- Do not infer event ordering from file order when reliable timestamps conflict; report the discrepancy.

## Outcome normalization

Map only unambiguous values to success, failure, cancelled, timeout, pending, or unknown. Preserve original status. Do not count unknown as success or failure.

## Data-quality coverage table

For each analyzed dataset, report whether these are present:
- Stable session/run ID.
- Event timestamps.
- Start/end or measured duration.
- Tool names.
- Tool outcomes.
- Model request outcomes.
- Retry/correlation identifiers.
- Step events.
- Token usage.
- Cost and pricing basis.
- Parent/child trace structure.

This coverage table must be generated from the actual input, not copied from this document.
