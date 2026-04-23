# Local & Proxy Model Backends

**Class:** Independent deployment · **Confidence:** High · **Demo status:** Config patterns

## Pain Point

The default "point Hermes at OpenRouter" works but has two real problems for some users: cost at scale, and data leaving your machine. You want to run Hermes against a **local model** (Ollama, vLLM, oMLX) or a **proxy** that routes requests through your own infrastructure — while keeping the full Hermes feature surface (skills, memory, cron, gateways).

## What It Does

Hermes is model-agnostic and supports arbitrary OpenAI-compatible endpoints. Multiple first-person GitHub issues document real configurations beyond the defaults:

- **oMLX on macOS** (`xiaoyin1993`) — running `Qwen3.5-122B-A10B-8bit` through oMLX 0.3.5 on Apple Silicon, configured as a custom provider pointing at the local endpoint.
- **Anthropic-compatible proxies** (`michealmachine`) — routing Hermes through an OpenAI-compatible proxy that forwards to Anthropic, surfacing the custom provider and model list in the Telegram `/model` picker.
- **Ollama** — first-class support via the `hermes model` wizard; Ollama's own docs include a Hermes integration walkthrough.
- **Ollama Cloud** — same catalog as local Ollama but hosted; auto-discovers models when you paste the API key.

These aren't hypothetical — they're live user configurations surfaced in bug reports.

## Setup

The wizard path:

```bash
hermes model        # interactive — pick "Custom endpoint" or a specific provider
```

Pick a provider type and the wizard walks through credentials and model selection. For a completely custom endpoint, use the triple syntax once it's configured:

```bash
/model custom:local:qwen-2.5     # local custom provider, specific model
/model custom:work:llama3         # "work" custom provider
/model openrouter:claude-sonnet-4 # switch back to cloud
```

Config can also be written directly into `~/.hermes/config.yaml`.

### Ollama (local, quickest path)

```bash
ollama pull qwen2.5-coder:32b
ollama serve                      # listens on :11434
```

Then in `hermes model`, pick **Custom endpoint**, enter `http://localhost:11434/v1`, skip the API key, enter the model name. **Increase the context window** — Hermes's system prompt, tools, and memory all need to fit.

### Custom OpenAI-compatible proxy

```yaml
# ~/.hermes/config.yaml
providers:
  work-proxy:
    base_url: https://proxy.internal.example.com/v1
    key_env: WORK_PROXY_KEY
    model:
      default: anthropic/claude-3.7-sonnet
```

Anything speaking the OpenAI `/v1/chat/completions` shape works. Common patterns: a LiteLLM gateway, a self-hosted vLLM instance, or a private proxy that does cost/auditing in front of Anthropic or OpenAI.

### Fallback configuration

Hermes supports a fallback model that swaps in automatically on rate-limit or auth failure:

```yaml
# ~/.hermes/config.yaml
fallback_model:
  provider: openrouter
  model: anthropic/claude-sonnet-4
```

Fires at most once per session and keeps the conversation intact. Useful when your primary is a local or rate-limited provider.

## Hardware Notes for Local

Community reports put the **minimum viable local model at ~32B parameters** for reliable multi-step agent work — anything smaller handles basic automations but gets shaky on delegation and tool chains. That translates to **at least 24 GB of VRAM** for comfortable operation.

Apple Silicon users running oMLX have gotten useful work out of Qwen3.5-122B at 8-bit quant on M-series machines with unified memory.

## Skills Needed

- A local inference engine (Ollama, vLLM, oMLX, llama.cpp) or a custom proxy
- Model that fits your hardware's memory budget with room for Hermes's system prompt
- `hermes model` to configure the provider, or `config.yaml` for fully declarative setup

## Notes

- **Context window matters more than parameter count for Hermes.** If your model supports 32K but the skill set plus memory plus the current task's context push past that, you'll see truncation. Community minimum is 64K context.
- **Long-context instability exists and is reported.** The oMLX issue thread includes stability observations at long context — worth reading before committing to a specific local model for serious work.
- Local models bypass cloud costs but not energy costs. A GPU running 24/7 at load is not free.
- The `/model` slash command lets you hot-swap providers mid-session without restarting — handy when you hit a local-model limit and want to finish a task on a cloud backend.

## Sources

- AI Providers docs: <https://hermes-agent.nousresearch.com/docs/integrations/providers/>
- Ollama × Hermes integration: <https://docs.ollama.com/integrations/hermes>
- Community setup walkthrough (LinkedIn, linked to by Nous): <https://www.linkedin.com/pulse/getting-started-hermes-agent-your-self-improving-ai-assistant-maio-tys6e>
