# Production Software-Dev Workflow

**Class:** Independent deployment · **Confidence:** Medium-High · **Demo status:** Case study

## Pain Point

"Can you actually ship production code with an agent, or is this just autocomplete on steroids?" The honest way to answer is a public field report — someone using Hermes day in, day out on real paying work, telling you what held up and what didn't.

## What It Does

GitHub user `JuanDragin` filed [issue #5563](https://github.com/NousResearch/hermes-agent/issues/5563) describing three weeks of daily production development on Hermes. It's the most detailed third-party field report currently public. The workflow runs on a real (private) pipeline touching DBOS, Postgres, S3, and Gmail-style integrations. It's not a toy demo.

Key ingredients from the report:

- Long CLI sessions — hours, not minutes. One session ran ~12 hours and logged roughly 2.6M replay tokens.
- Heavy use of persistent sessions and memory so context survives across days.
- `delegate_task` to split work into isolated sub-agents and keep the main session's context tight.
- Standard tools — terminal, file, search — not exotic setups.

The private stack means you can't clone and run their exact workflow, but the patterns are reproducible.

## What to Take From It

- **Memory is the unlock for daily work.** If your agent forgets yesterday, you're not doing production dev — you're pair-programming with goldfish. Configure `~/.hermes/` and the memory/session tools as a first-class part of setup, not an afterthought.
- **Delegate aggressively.** Sub-agents keep the parent session's context lean. That report's 12-hour session wouldn't have survived in a single flat context window.
- **Budget for replay tokens.** 2.6M tokens in a session means memory compression, context rehydration, and skill loads are the actual cost — not individual messages.

## Reproducing It

You can't replicate the author's private pipeline, but you can build a sibling setup:

- A toy DBOS or Postgres project with a few real workflows.
- Memory and session persistence enabled from day one.
- A `delegate` habit — encode it in a skill so the agent reaches for it automatically on multi-part tasks.

## Skills Needed

- Persistent sessions and memory (`~/.hermes/` state)
- `delegate_task`
- Terminal, file, search tools
- Habits: long sessions, explicit goals, delegation on anything non-trivial

## Reported Metrics

- 3 weeks of daily use
- 8+ hours/day
- One ~12-hour session with ~2.6M replay tokens

## Notes

This is first-person evidence, not a runnable demo. Treat it as a pattern guide, not a template.

A complementary field report comes from **Mark Watson**, who documents daily Hermes use across dev, research, writing, and business analysis, paired with VM/sandbox patterns for containing security risk. Different in emphasis — security posture rather than a specific architecture — but useful as a second data point that serious daily use is happening. Watson publishes on his personal site and in self-published books; the specific Hermes writeup was referenced in research notes but is not yet pinned to a canonical URL in this catalog.

## Sources

- GitHub issue (JuanDragin): <https://github.com/NousResearch/hermes-agent/issues/5563>
