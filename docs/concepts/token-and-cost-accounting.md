# Concept: Token and cost accounting

## What it is

Recording, for every model call, how many tokens went in and came out, and converting those counts into money using the model's prices, attributed to who made the call and why. Model APIs bill per token, so this is the unit economics of an LLM system.

## Why it matters here

PLAT-02's acceptance criteria require that "usage is recorded per call". The [model gateway](gateway-pattern.md) captures usage and computes cost for every call, tagged with `caller` and [tier](model-tiers.md). [PLAT-03 / M02](../curriculum/02-tracing-and-observability.md) also puts it on Langfuse traces ([observability and tracing](observability-and-tracing.md)). The v2.x roadmap item "cost optimization" ([release plan](../release-plan.md)) is impossible without this data. Whether usage is also stored in a Postgres table is an **open choice** laid out in [M01](../curriculum/01-model-gateway.md#where-the-data-lives).

## How it works

- **Tokens, not characters.** Text is split into sub-word tokens by the model's tokenizer. A rough rule of thumb for English is about 4 characters per token, but it varies by model and language. Trust the provider's reported counts over estimates.
- **Counts come back on the response.** Typically `input_tokens` and `output_tokens`, plus, when prompt caching is in use, cache-write and cache-read tokens.
- **Different tokens, different prices.** Output tokens usually cost several times more than input tokens. Cached reads cost a fraction of normal input, and cache writes may cost a premium. So:

```python
cost = (inp * p_in + out * p_out + cache_read * p_cache_read + cache_write * p_cache_write) / 1_000_000
```

- **Price tables go stale.** Keep prices as configuration with an effective date, keyed by model. Computed cost is an estimate to reconcile against the invoice, not the invoice.
- **Attribution is the point.** Total spend is trivia. Spend by caller × tier × course is what tells you the Researcher is re-fetching things the knowledge store already caches, or that Reviewer prompts have bloated.
- **Failures and retries.** Record attempts and outcome for every logical call. Rejected requests (429, 400) generally aren't billed, but timed-out ones may have been.
- **Context is the cost driver.** Because each request resends the full context, input tokens usually dominate for agents with long tool loops. That's why ai-tutor uses compact context packets ([ADR 0001](../decisions/0001-agents-share-state-through-database.md)) rather than full histories.

## Further reading

- Anthropic pricing: https://www.anthropic.com/pricing
- Anthropic prompt caching (cache read/write accounting): https://docs.anthropic.com/en/docs/build-with-claude/prompt-caching
- Langfuse token and cost tracking: https://langfuse.com/docs/model-usage-and-cost
