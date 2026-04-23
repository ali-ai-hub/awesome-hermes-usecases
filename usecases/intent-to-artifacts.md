# Intent-to-Artifacts Workflow

**Class:** Independent deployment · **Confidence:** Medium · **Demo status:** Blog-based pattern

## Pain Point

You have more rough prompts than polished outputs. "I should write a runbook for this." "I want an RSS digest of these sources." "Let me sketch a diagram of this system." Each one is a 20-minute task that takes an hour once you open the right tools. You want the path from a sentence in your head to a useful artifact on disk to be one message long.

## What It Does

eBourgess documented their personal Hermes workflow in a first-person blog post. The pattern: rough prompts in, structured artifacts out — runbooks, personal notes, RSS curation, diagrams, Telegram outputs. The agent writes to local files (so everything's grep-able and git-able) and pings Telegram when something's ready.

It's not a product. It's a disciplined setup that turns Hermes into a pipeline from intent to saved artifact, with the author's own conventions encoded in prompts and skills.

## Pattern

- **One agent, many output channels.** Same Hermes instance, different tools: local file output for notes, Telegram for "done" notifications, research tools for digests, a diagram tool for sketches.
- **Prompts that always end in a file.** "Write this as `~/notes/2026-04-22-X.md`" instead of "write this and show me." Forces the artifact-on-disk habit.
- **Scheduled curation.** Cron jobs pulling from RSS or the web and writing markdown to a notes folder, so the morning brief is ready before it's asked for.

## Reproducing It

You don't need the author's private config. The ingredients are all first-party:

- [Daily Briefing](daily-briefing-bot.md) for scheduled research output.
- Telegram gateway for ping-on-done.
- A simple file-output habit in your prompts — always end with "save to `~/notes/<filename>.md`".
- Optional: a small skill that enforces your filename conventions and folder structure.

## Skills Needed

- Terminal and file tools (built in)
- Web search / research tools
- Telegram gateway (for delivery pings)
- A notes folder with a convention you'll actually follow

## Notes

- This is a pattern, not a demo. The value is in the habits — file-first outputs, scheduled curation, one agent in front of many tools — not a specific repo to clone.
- The original blog post is concrete enough to adapt; source is below.

## Sources

- Blog post: <https://ebourgess.dev/posts/how-i-use-hermes-agent-to-turn-intent-into-artifacts/>
