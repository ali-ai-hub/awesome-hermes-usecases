# Daily Briefing Bot

**Class:** First-party demo · **Confidence:** High · **Demo status:** [Runnable](../demos/daily-briefing/)

## Pain Point

Every morning you want to catch up on the 2–3 topics you actually care about — AI news, a specific subreddit, a company's releases — without wading through feeds, newsletters, and Twitter. Most RSS readers surface everything; most AI chatbots forget you tomorrow.

## What It Does

A Hermes cron job wakes at a set time, does its own web research across the topics you care about, summarizes the findings into a clean brief, and drops it into Telegram, Discord, or a local markdown file. You read it with your coffee. You never open a feed.

The upgraded pattern delegates each topic to a parallel sub-agent so the whole brief finishes in the time of the slowest single topic, not the sum.

## Setup

1. Install Hermes Agent and start the gateway so the cron scheduler runs unattended:
   ```bash
   curl -fsSL https://raw.githubusercontent.com/NousResearch/hermes-agent/main/scripts/install.sh | bash
   hermes setup
   hermes gateway install           # as a user service
   ```
2. Set `FIRECRAWL_API_KEY` in your environment so web search works.
3. Configure a delivery channel (Telegram or Discord) during `hermes setup`, or use `--deliver local` to write briefs to `~/.hermes/cron/output/`.

## Prompts

Single-topic version, scheduled daily at 8 AM:

```
/cron add "0 8 * * *" "Every morning at 8am, search the web for the latest
news about AI agents and open source LLMs. Summarize the top 3 stories in
a concise briefing with links. Use a friendly, professional tone. Deliver
to telegram."
```

Parallel delegation version (faster):

```
/cron add "0 8 * * *" "Create a morning briefing by delegating research
to sub-agents. Delegate three parallel tasks:
 1. Delegate: top 2 AI/ML stories from the past 24h with links
 2. Delegate: top 2 crypto stories from the past 24h with links
 3. Delegate: top 2 space exploration stories from the past 24h with links
Collect results and combine into a single clean briefing with section
headers, emoji, and source links. Add today's date as a header."
```

Weekdays-only: swap `0 8 * * *` for `0 8 * * 1-5`.

## Skills Needed

- Web search (Firecrawl)
- Delegation (for the parallel variant)
- Messaging gateway (Telegram or Discord)

## Notes

- Cron jobs run in fresh agent sessions with no memory of your chat — prompts must be self-contained.
- Output `[SILENT]` in the prompt's final response to suppress delivery on quiet days.

## Sources

- Official tutorial: <https://hermes-agent.nousresearch.com/docs/guides/daily-briefing-bot/>
- Cron reference: <https://hermes-agent.nousresearch.com/docs/guides/automate-with-cron>
- Automation templates catalog (weekly digests, backlog triage, docs drift, security audits, and more): <https://hermes-agent.nousresearch.com/docs/guides/automation-templates>
