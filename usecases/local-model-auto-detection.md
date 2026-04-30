# Infrastructure: Local Model Auto-Detection

**Class:** Community showcase · **Confidence:** High · **Demo status:** Verified workflow

## Pain Point

Setting up Hermes with a local model means manually specifying the model name, inference endpoint, and — critically — the context window size. Get the context window wrong and multi-step tool workflows fail silently. First-time users often give up before they get a single successful turn because the configuration is opaque and the errors are misleading.

## What It Does

@sudoingX (the same user who opened PRs for local-runner improvements) documented a workflow where Hermes now auto-detects the running local model during setup: it probes the endpoint, identifies what's running, asks for confirmation, and configures the context window automatically.

The patch covers three layers:
1. **Endpoint probing** — Hermes queries `/v1/models` on the local server and maps the response to known model metadata.
2. **Context-window detection** — derives the correct context length from model info rather than relying on defaults.
3. **Setup wizard trigger** — on fresh installs, the wizard now properly activates when a local server is detected.

## Setup

1. Install Hermes via the standard installer:
   ```bash
   curl -fsSL https://raw.githubusercontent.com/NousResearch/hermes-agent/main/scripts/install.sh | bash
   ```
2. Start your local inference server (Ollama, llama.cpp server, MLX server, etc.).
3. Run `hermes setup` and select the local option when prompted.
4. Hermes probes `http://localhost:YOUR_PORT/v1/models`, lists detected models, and asks you to confirm.
5. The configuration is written automatically with correct context window and endpoint.

**Supported local runners:**
- Ollama (`ollama serve`)
- llama.cpp server (`llama-server`)
- MLX server (`python -m mlx_lm.server`)
- vLLM
- Any OpenAI-compatible local endpoint

## Prompts

**Post-setup validation:**
```
Let's test the local model: write a haiku, then run `ls -la`, then check what time it is. I want to see tool chaining working.
```

**Context validation:**
```
How many tokens of context does my current model have? Confirm from the local endpoint.
```

## Skills Needed

- Local LLM inference server (Ollama, llama.cpp, MLX, or vLLM)
- Hermes setup wizard (v0.7.0+)
- Optional: local-llm skill for advanced configuration

## Notes

- The auto-detection works best with well-known models in the local server's registry. Unusual or custom fine-tunes may report generic IDs that can't be mapped to known context windows — in those cases, manual override is still needed.
- Context-window mismatch is the #1 reason local setups feel broken. If Hermes thinks your model has 8K context but it really has 128K, nothing works. If it thinks 128K but you only have 8K, the model truncates and produces garbage. This patch eliminates that class of error.
- @sudoingX's third PR on this topic suggests the community has iterated on the detection logic across multiple edge cases.

## Sources

- @sudoingX on X (verified): https://x.com/sudoingX/status/2038895651266973860 (434 likes, 40 replies)
- Hermes Agent Use Cases site: https://ai-hermes-agent.com/use-cases
- Hermes docs — Quickstart (context requirements): https://hermes-agent.nousresearch.com/docs/getting-started/quickstart/
