# Printing-Factory Task Memory

**Class:** Independent deployment · **Confidence:** Medium-High · **Demo status:** Custom skill + case study

## Pain Point

Use Hermes day to day on operational work — scheduling print jobs, tracking machine state, handling recurring customer requests — and the problems the stock agent has become sharp: context gets long, the agent slows down, and it starts forgetting what it did an hour ago. Native memory compression helps, but it compresses broadly; what you want is fast retrieval of *specific prior tasks* without rehydrating a giant history.

## What It Does

GitHub user `Xwm1234` filed [issue #11653](https://github.com/NousResearch/hermes-agent/issues/11653) describing a custom task-memory skill for daily use in a printing factory. The skill maintains a local JSON index of tasks the agent has completed, so the agent can look up "what did I do for customer X last week" in sub-second time without paging back through the entire session. Retrieval hooks inject the relevant history into the agent's context only when it's needed, keeping the live context small.

The author reports noticeably better recall and faster responses once the skill was installed, and the issue includes a link to the skill code.

## Setup

Sketch of the pattern (the author's exact skill is linked from the issue):

1. Create a skill directory:
   ```
   ~/.hermes/skills/task-memory/
     SKILL.md                # describes when and how to use the skill
     task_index.py           # maintains a local JSON index of tasks
     retrieve.py             # pulls relevant past tasks on demand
   ```
2. The skill's `SKILL.md` tells the agent: "Before starting a task similar to one you've done before, call `retrieve` to pull the last 3 matching tasks." Hermes loads this on every relevant turn.
3. Restart Hermes so the skill is picked up:
   ```bash
   hermes tools       # confirm the skill shows up
   ```

## What to Take From It

- **Skills can be your retrieval layer.** You don't need a vector DB to solve "the agent forgot what it did last week" — a local JSON index keyed on task type can be sub-second and zero-ops.
- **Hermes's skill system is the extension point for exactly this kind of domain memory.** Drop it in `~/.hermes/skills/` and it's loaded without code changes to Hermes itself.
- **Generalizes.** The same pattern works for a CRM log, a support-ticket archive, a research notebook — any domain where "what did I do with this thing before?" is the recurring question.

## Skills Needed

- A custom skill in `~/.hermes/skills/`
- A local JSON index (no external DB required)
- Retrieval hooks called from the skill

## Reported Metrics

- Sub-second retrieval on the author's dataset
- Noticeably reduced slowness on long-running sessions (per the issue)

## Notes

Review the linked skill code before running it — it's a community contribution, not audited.

## Sources

- GitHub issue: <https://github.com/NousResearch/hermes-agent/issues/11653>
