# Concept: Gateway pattern

## What it is

An object or module that wraps access to an external system behind an interface **your application owns**. The rest of the code talks to the gateway in the application's own terms, and only the gateway knows the external system's API, types, quirks, and failure modes. Used as the *only* path to that system, it becomes a **chokepoint**: one place where cross-cutting policy is applied to every interaction.

## Why it matters here

ai-tutor's model gateway (PLAT-02) is the single module every agent and workflow uses for model calls ([architecture overview](../architecture/overview.md), [M01](../curriculum/01-model-gateway.md)). Because it is the only path, tier selection ([model tiers](model-tiers.md)), [timeouts](timeouts.md), [retries](retries-and-backoff.md), typed errors, [cost accounting](token-and-cost-accounting.md), and tracing ([observability](observability-and-tracing.md)) are implemented once and hold everywhere. A lint/grep check enforces that nothing bypasses it.

## How it works

- **Own the interface.** Callers pass and receive internal types (e.g. a `Completion`), never provider objects. That keeps provider details from leaking and makes swapping or adding a provider a local change.
- **Translate at the edge.** Inside, an adapter converts internal requests to the provider's wire format, and provider responses and errors back to internal types. One adapter per external system.
- **Apply policy centrally.** Anything that should be true of *every* call belongs here: auth, timeouts, retries, error mapping, metering, tracing.
- **Enforce exclusivity.** A gateway that can be bypassed decays. Back it with tooling, e.g. a ruff `banned-api` rule forbidding provider SDK imports outside the gateway package, or a CI grep for provider hostnames.
- **Keep it thin on domain logic.** The gateway handles transport. It shouldn't decide what to ask the model or interpret the answer. In ai-tutor specifically it does one round-trip and never runs tool loops, which belong to the hand-written agents ([ADR 0003](../decisions/0003-no-agent-frameworks-at-first.md)).
- **Testing seam.** A single interface is easy to replace with a fake or a recorded-response stub, which unit tests and the eval runner rely on.
- **In-process module vs service.** Large organisations often run "LLM gateways" as a network proxy shared by many apps (central keys, quotas, audit). For a single backend, an in-process module gives the same chokepoint without the extra hop, and can be extracted later precisely because it's already the only path.

## Further reading

- Martin Fowler, "Gateway": https://martinfowler.com/articles/gateway-pattern.html
- Martin Fowler, *Patterns of Enterprise Application Architecture*, "Gateway" and "Service Stub"
- Ruff `flake8-tidy-imports` banned-api setting: https://docs.astral.sh/ruff/settings/#lint_flake8-tidy-imports_banned-api
