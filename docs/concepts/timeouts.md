# Concept: Timeouts

## What it is

An explicit upper bound on how long the caller waits for a request before giving up and treating it as a failure. Without one, a hung connection or a stalled server can block the caller indefinitely.

## Why it matters here

Every call through the ai-tutor [model gateway](gateway-pattern.md) carries a timeout set by its [tier](model-tiers.md). The live Tutor has to start replying within about 1–2 s ([product spec](../product-spec.md)), while background workflows can wait much longer. See [M01](../curriculum/01-model-gateway.md), stage 4.

## How it works

- **Kinds of timeout.** *Connect* (reaching the server), *read/idle* (no bytes for N seconds), and *total* (the whole request). For streaming responses there's also **time-to-first-token**, which is what a learner actually feels.
- **LLM latency scales with output.** Generation time is roughly proportional to output tokens, so a fixed timeout that suits a 50-token reply will kill a legitimate 4,000-token lesson draft. Size the timeout from the tier *and* `max_tokens`, or use an idle timeout while streaming.
- **Timeouts vs deadlines.** A timeout bounds one attempt. A deadline bounds the whole logical call, retries included. Retries should never push past the deadline (see [retries and backoff](retries-and-backoff.md)).
- **Client timeouts don't cancel server work.** When you give up, the provider may keep generating and may still bill. Timeouts protect *your* latency and resources, not your spend.
- **Check SDK defaults.** Official SDKs often default to timeouts of several minutes, which is far too long for a live tutor. Set them explicitly.
- **Map to a typed error.** A fired timeout should come out of the gateway as something like `GatewayTimeout`, so callers can choose a fallback (e.g. the Tutor apologising and keeping the turn resumable).

## Further reading

- HTTPX timeouts (the client most Python provider SDKs use): https://www.python-httpx.org/advanced/timeouts/
- Google SRE Book, "Handling Overload" (deadlines and propagation): https://sre.google/sre-book/handling-overload/
