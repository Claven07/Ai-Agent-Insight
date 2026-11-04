# AI Agent Insights — Run Performance Report

> Synthetic demonstration only. This report describes the fixture in sample-session-failure.json; it is not a measurement of a real system.

## 1. Executive summary

The sample run reports 9,000 ms elapsed session duration, three tool attempts across two logical tool operations, and two LLM attempts associated with one logical request. One search_code attempt timed out and a correlated retry succeeded. run_tests is the longest supplied tool operation at 4,500 ms. The evidence is too small to establish a recurring performance regression or a root cause for the timeout.

## 2. Scope and data coverage

| Evidence | Coverage |
|---|---|
| Session start/end and duration | Present |
| Tool names, attempts, durations, outcomes | Present |
| Logical tool-operation IDs | Present |
| LLM attempt IDs and logical request ID | Present |
| LLM attempt durations and outcomes | Present |
| Token usage and cost | Not supplied |
| Per-event parent/child trace graph | Not supplied |
| Repeated runs or baseline | Not supplied |

## 3. Run overview

| Metric | Value |
|---|---:|
| Session duration | 9,000 ms |
| Tool attempts | 3 |
| Logical tool operations | 2 |
| Successful tool attempts | 2 |
| Failed tool attempts | 1 |
| Tool-attempt success rate | 66.7% (2/3) |
| LLM attempts | 2 |
| Logical LLM requests | 1 |

The tool-attempt success rate is not a task-completion rate and is not the success rate of unique logical operations.

## 4. Tool execution analysis

| Tool | Attempts | Outcomes | Durations |
|---|---:|---|---|
| search_code | 2 | 1 timeout, 1 success | 500 ms, 900 ms |
| run_tests | 1 | 1 success | 4,500 ms |

**Observed:** The two search_code records share logical_operation_id search-op-1. The first attempt timed out; the later correlated attempt succeeded.

**Observed:** run_tests is the longest supplied tool call at 4,500 ms.

The sum of the listed tool durations is 5,900 ms. This sum is not a wall-clock duration and must not be interpreted as the portion of session time spent sequentially without checking event overlap and timing semantics.

## 5. LLM request analysis

Two attempts share logical_request_id llm-request-1. The first attempt timed out after 1,200 ms; the second succeeded after 1,500 ms.

The fixture therefore demonstrates a timed-out attempt followed by a successful correlated attempt. It does not establish why the first attempt timed out or whether the retry policy is appropriate.

No token usage or pricing data is present, so token consumption and cost are unavailable.

## 6. Findings

### F-01 — Search operation recovered after a timeout

- Severity: Informational
- Evidence type: Observed
- Evidence: Two attempts share logical_operation_id search-op-1. Attempt one ended in a timeout; attempt two succeeded.
- Confidence: High for the sequence shown in the fixture.
- Limitation: A single logical operation cannot establish a recurring timeout pattern.

### F-02 — Test execution is the longest supplied tool call

- Severity: Informational
- Evidence type: Observed
- Evidence: run_tests took 4,500 ms, compared with 500 ms and 900 ms for search_code attempts.
- Confidence: High for the ranking in this fixture.
- Limitation: No baseline, suite size, or repeated-run distribution is supplied.

### F-03 — Tool-attempt success rate is 2/3

- Severity: Informational
- Evidence type: Calculated
- Calculation: 2 successful tool attempts / 3 total tool attempts × 100 = 66.7%.
- Limitation: This is attempt-level only. It is not a unique-operation or task-completion rate.

## 7. Recommendations

1. Capture several comparable runs of the same test workload before optimizing run_tests. Record test count and duration so the result can be interpreted against workload.
2. Review the search_code timeout threshold and retry behavior if the same pattern appears in more runs. Preserve the successful retry path while investigating.
3. Retain logical-operation and attempt identifiers in future exports so retries can be separated from independent calls.
4. Add token usage and provider-reported cost only if those measurements are available from the source.

## 8. Follow-up data needed

- Several comparable runs of the same task and agent configuration.
- Tool-level baselines and workload size.
- Retry policy configuration and timeout source.
- LLM provider/model and error classification, if available.
- Token usage and pricing basis, only if cost analysis is required.
