# Dev: Local Model Quantization with TurboQuant

**Class:** Community showcase · **Confidence:** High · **Demo status:** Verified workflow

## Pain Point

Running large models locally on Apple Silicon is attractive for privacy and cost, but stock models are often memory-hungry and slow without quantization. The optimization path — picking the right quantization scheme, validating output quality, documenting the config — is technical enough that most users skip it and default to cloud APIs.

## What It Does

@alexcovo_eth built TurboQuant skills for Hermes Agent, then used them to optimize Qwen3.5-9B-MLX for local inference on Apple Silicon. The workflow covers the full path: apply quantization, run benchmarks, document results, and publish the optimized weights back to HuggingFace — all orchestrated through Hermes.

The published model ([qwen35-9b-mlx-turboquant-tq3](https://huggingface.co/alexcovo/qwen35-9b-mlx-turboquant-tq3)) is a concrete artifact of the workflow; it's not just a config discussion.

## Setup

1. Hermes Agent with local model access and Apple Silicon environment.
2. MLX and MLX-LM installed.
3. Hermes TurboQuant skills loaded (domain-specific optimization skills).
4. HuggingFace token for publishing.

The agent is given a goal like *"make Qwen3.5-9B-MLX better for local inference with TurboQuant."* It then:
- Selects the quantization strategy
- Runs conversion
- Validates with test prompts
- Documents memory usage and speed
- Packages and uploads the result

## Prompts

**Direct optimization request:**
```
Take the Alibaba Qwen3.5-9B-MLX model and apply TurboQuant so it runs better on my Mac. Validate that quality doesn't drop, then upload the optimized version to HuggingFace.
```

**Iterative refinement:**
```
The previous TQ3 setting is fast but I see quality loss on coding tasks. Try TQ4 on the code eval subset and compare.
```

## Skills Needed

- huggingface (search/download/upload)
- turboquant (domain-specific quantization skill)
- mlx (local model execution)
- Optional: evaluating-llms-harness for benchmark validation

## Notes

- This is a concrete example of Hermes "growing with you" — a skill set built by the community that the agent can compose with built-in tools. The agent didn't just run a script; it made decisions about quantization level, validated, and published.
- The MLX ecosystem on Apple Silicon is a sweet spot: unified memory means you can run 9B models on a MacBook Pro without thrashing.
- LinkedIn and HuggingFace presence confirm this is a real model in use, not a hypothetical workflow.

## Sources

- @alexcovo_eth on X (verified): https://x.com/alexcovo_eth/status/2038464904806453260
- LinkedIn article: https://www.linkedin.com/pulse/hermes-agent-turboquant-making-qwen35-9b-mlx-better-local-alex-covo-zpixe
- HuggingFace model: https://huggingface.co/alexcovo/qwen35-9b-mlx-turboquant-tq3
