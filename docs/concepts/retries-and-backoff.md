# Concept: Retries and backoff

## What it is

Automatically repeating a failed request when the failure is likely **transient**, waiting between attempts with a delay that grows (exponential backoff) and is randomised (jitter), and giving up once an attempt count or a time budget runs out. The other half is knowing which failures **must not** be retried.

## Why it matters here

Model provider APIs fail transiently all the time: rate limits (429), overload, 5xx errors, dropped connections. The [model gateway](gateway-pattern.md) owns one retry policy for every model call in ai-tutor and turns whatever is left after retrying into a typed exception the caller can act on. See [M01](../curriculum/01-model-gateway.md), stage 6 and the worked example.

## How it works

**1. Classify first.**

- Retryable: 429 rate limited, 5xx or "overloaded", connection errors, and (usually) your own [timeout](timeouts.md).
- Not retryable: 400/422 bad request, context too long, 401/403 auth, 404 unknown model. The identical request will fail identically, and retrying only adds latency (and, for auth, can look like abuse).

**2. Wait the right amount.**

- If the server sends `retry-after`, honour it. It knows when capacity returns.
- Otherwise use exponential backoff, `delay = min(cap, base × 2^attempt)`, with **full jitter**: sleep a random value in `[0, delay]`. Without jitter, many clients that failed together retry together, and the synchronised wave prolongs the overload ("thundering herd").

```python
delay = random.uniform(0, min(cap, base * 2 ** attempt))
```

**3. Stop on a budget, not just a count.** A per-call **deadline** keeps retries from running past the point where the result is still useful. For ai-tutor's live Tutor (`fast` tier) a few seconds is the whole budget. For the Lesson Builder running ahead of time, minutes are acceptable. Same mechanism, different [tier](model-tiers.md) policy.

**4. One owner.** Retry layers multiply. If an SDK retries 2 times inside a gateway that tries 3 times, one call can become 9 requests. Disable one layer.

**5. Mind idempotency and cost.** A model completion has no side effects at the provider, so retrying is safe in that sense. But a timed-out attempt may still have been generated and billed. With streaming, only retry before any tokens have reached the user.

Related patterns for later: circuit breakers (stop calling a provider that's clearly down for a while) and retry budgets shared across callers (so background work can't use up rate limits the live tier needs).

## Further reading

- AWS Architecture Blog, "Exponential Backoff And Jitter": https://aws.amazon.com/blogs/architecture/exponential-backoff-and-jitter/
- Google SRE Book, "Addressing Cascading Failures": https://sre.google/sre-book/addressing-cascading-failures/
- Anthropic API errors and rate limits: https://docs.anthropic.com/en/api/errors
