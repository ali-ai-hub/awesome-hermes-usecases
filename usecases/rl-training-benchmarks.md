# RL Training & Benchmarks

**Class:** Official core capability · **Confidence:** High · **Demo status:** Developer docs + code

## Pain Point

If you're training or evaluating a tool-calling model, you need thousands of realistic agent trajectories — not synthetic prompt-completion pairs. Building a trajectory-generation environment from scratch is months of infrastructure work: tool sandboxing, eval scoring, trajectory export, parallelism, deduplication.

## What It Does

Hermes ships first-class support for agent research:

- **`HermesAgentBaseEnv`** is an environment class you subclass to define a task, its tools, and a success metric.
- Batch runners generate thousands of trajectories in parallel with automatic checkpointing.
- **Atropos** integration plugs trajectories into reinforcement learning loops.
- Eleven tool-call parsers cover common model architectures so you can train across different families.
- Trajectories export to ShareGPT format for SFT, with compression to fit token budgets.

The **TBLite** benchmark is the lightweight reference: 100 tasks reported to correlate strongly with the larger TB2 benchmark, useful for fast iteration on a model without running the full thing.

## Setup

Developer docs cover the full environment API; the fast-path for trying it is to run the eval-only TBLite reference or one of the data-generation examples in the repo.

```bash
git clone https://github.com/NousResearch/hermes-agent
cd hermes-agent
uv venv venv --python 3.11
source venv/bin/activate
uv pip install -e ".[all,dev]"

# RL / Atropos integration (optional)
git submodule update --init tinker-atropos
uv pip install -e "./tinker-atropos"
```

Then follow the environments docs for running an eval or spawning a trajectory batch.

## Use Cases

- **Evaluate a new model.** Point it at TBLite, get a tool-calling score.
- **Generate SFT data.** Run thousands of parallel tasks with a strong model, export trajectories, fine-tune a smaller one.
- **RL on agent behavior.** Use Atropos to do RL on multi-turn tool-using trajectories, not single-turn completions.

## Metrics

- TBLite: 100 tasks, strong correlation with TB2 per Nous documentation.
- Batch runner scales with worker count and model throughput; automatic checkpointing means interrupted runs resume.

## Skills Needed

- Familiarity with the Hermes environment class pattern
- Optional: W&B for run tracking, Tinker key for Atropos integration
- Non-trivial compute for large batches or RL runs

## Sources

- Environments developer guide: <https://hermes-agent.nousresearch.com/docs/developer-guide/environments/>
- Main repo: <https://github.com/NousResearch/hermes-agent>
