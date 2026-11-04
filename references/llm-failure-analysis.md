# LLM Request and Failure Analysis

## What to inspect

When present, inspect:
- Request timestamp and duration.
- Provider and model identifier.
- Outcome/status.
- Error category and message.
- Retry attempt and correlation identifiers.
- Token usage and finish reason.

## Classification

Use source evidence to classify failures, for example:
- Authentication or authorization.
- Rate limiting or quota.
- Timeout or network failure.
- Provider/server error.
- Invalid request or schema.
- Content/policy refusal.
- Cancellation.
- Unknown or unclassified.

Do not infer a provider root cause from a generic error string. Preserve unknown when evidence is insufficient.

## Retries

Distinguish attempts from logical requests. Group retries only when correlation identifiers or clear source semantics support grouping.

Do not describe retries as successful recovery unless a later attempt is demonstrably successful.

## Latency and tokens

Only report latency if measured per request or supplied as a valid aggregate. Only report token use if the source provides it and indicates what the count represents.

Do not estimate token counts from text length and present them as provider usage.

## Security

Redact authorization headers, API keys, bearer tokens, cookies, private keys, and secret-like values. Include only the minimum error excerpt needed for diagnosis.
