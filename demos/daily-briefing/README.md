# Daily Briefing Demo

A minimal, runnable version of the [Daily Briefing Bot](../../usecases/daily-briefing-bot.md) use case. Produces a morning brief every day at 8 AM and delivers it to Telegram (or a local file if you'd rather start without Telegram).

## What you'll end up with

A cron job, running unattended through the Hermes gateway, that:

1. Searches the web for news on topics you pick.
2. Summarizes the top stories into a clean brief with source links.
3. Delivers the brief to Telegram (or writes it to `~/.hermes/cron/output/`).

## Prerequisites

- Hermes Agent installed and a model configured (`hermes setup`).
- A Firecrawl API key (`FIRECRAWL_API_KEY`) for web search.
- (Optional) A Telegram bot token and your user ID, if you want delivery to Telegram.

If you don't have Telegram set up yet, run the local version first — same cron, delivered to a file — and add Telegram once you're happy with the output.

## Setup

1. Copy `.env.example` to `.env` and fill in the values you have:
   ```bash
   cp .env.example .env
   # edit .env
   ```

2. Start the Hermes gateway if it isn't already running:
   ```bash
   hermes gateway install       # as a user service
   ```

3. Create the cron job. Use the right version for your delivery target:

   **Local delivery (safest first run — writes to `~/.hermes/cron/output/`):**
   ```bash
   bash setup-local.sh
   ```

   **Telegram delivery (once Telegram is set up in `hermes setup`):**
   ```bash
   bash setup-telegram.sh
   ```

4. Wait until 8 AM, or trigger once manually to confirm:
   ```bash
   hermes cron run "Morning brief"
   ```

## Customizing

Edit `setup-local.sh` or `setup-telegram.sh` to change the topics, the time, or the format. The prompt is deliberately plain — tune it to what you actually want to read.

## Smoke test

`smoke.sh` verifies that Hermes and the gateway are available and that a one-shot non-scheduled run produces output. It doesn't need a Firecrawl key to check wiring (it will fail at the search step without one, which is expected).

```bash
bash smoke.sh
```

## Sources

- Official tutorial: <https://hermes-agent.nousresearch.com/docs/guides/daily-briefing-bot/>
