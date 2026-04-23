# Self-Evolution

**Class:** Official companion · **Confidence:** High · **Demo status:** Companion repo

## Pain Point

Your Hermes skills work, but you suspect they're not optimal — the prompt could be tighter, the tool descriptions could be clearer, the few-shot examples could be better chosen. Hand-tuning each skill is slow and you don't have a principled way to tell whether an edit actually helped or just felt better.

## What It Does

The `hermes-agent-self-evolution` repo wraps GEPA and DSPy into an optimization loop for Hermes skills. You give it a skill, an eval set, and a metric. It runs mutation rounds — varying the skill text, tool descriptions, and sometimes code — and measures each variant against the eval. The output is a PR-ready improvement you can inspect and apply.

In other words: the agent gets better at its own skills, on its own, for a few dollars per run.

## Setup

```bash
git clone https://github.com/NousResearch/hermes-agent-self-evolution
cd hermes-agent-self-evolution
export HERMES_AGENT_REPO=/path/to/your/hermes-agent-clone
# follow the repo's setup for uv / dependencies
```

Run an optimization on an existing skill:

```bash
evolve_skill \
  --skill pr-review \
  --eval-set eval/pr-review.jsonl \
  --rounds 5
```

The repo ships a toy skill optimization you can run first to confirm the loop works end-to-end before pointing it at a real skill.

## What a Run Produces

- A diff against the original skill
- Eval scores per round (baseline vs. each variant)
- Optional session history of the optimizer itself

Inspect the diff. Apply it if it's genuinely better. Ignore it if the metric is gaming.

## Reported Cost

The repo estimates roughly **$2–$10 per run** depending on model and eval size. That's cheap enough to run routinely on the skills you depend on most.

## Skills Needed

- A clone of `hermes-agent` pointed to by `HERMES_AGENT_REPO`
- An eval set for the skill you're optimizing (this is the hard part — the optimizer is only as good as what you measure)
- An LLM provider key

## Notes

- **Evals matter more than the optimizer.** A sloppy eval lets the optimizer find loopholes instead of real improvements. Write evals that capture the cases where the current skill fails.
- Treat the output as a PR, not an auto-apply. Review the diff. Sometimes the "better" variant overfits to the eval.

## Sources

- Companion repo: <https://github.com/NousResearch/hermes-agent-self-evolution>
