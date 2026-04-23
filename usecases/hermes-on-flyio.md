# Hermes on Fly.io

**Class:** Ecosystem integration · **Confidence:** High · **Demo status:** Official Fly-apps repo

## Pain Point

You want to run Hermes on real infrastructure — not your laptop — without managing a full VPS, Docker orchestration, and volume backups yourself. Hermes's own docs recommend a $5 VPS; that works, but it's all manual. You want something closer to "push a config, get a persistent agent with a durable volume."

## What It Does

Fly.io maintains an official deployment example at `fly-apps/hermes-flyio` that stands Hermes up as a Fly Machine with a volume-backed home directory, cost estimates, and a documented update path. Everything Hermes learns — memories, skills, `SOUL.md`, session DB, cron jobs — lives on the `/opt/data` volume, which Fly snapshots daily. The gateway runs continuously so Telegram/Discord/etc. stay reachable while you're offline.

This isn't a hosted Hermes SaaS — you're running your own agent. Fly just provides the infrastructure primitives (Machines, volumes, snapshots, secrets).

## Setup

Full flow from the `fly-apps/hermes-flyio` README, summarized:

1. Install `flyctl` and log in:
   ```bash
   brew install flyctl    # or platform equivalent
   fly auth login
   ```

2. Clone the example repo and pick a globally-unique app name:
   ```bash
   git clone https://github.com/fly-apps/hermes-flyio.git
   cd hermes-flyio
   git clone https://github.com/NousResearch/hermes-agent.git
   export APP="hermes-$(whoami)-$(openssl rand -hex 3)"
   sed -i.bak "s/my-hermes/$APP/" fly.toml && rm fly.toml.bak
   ```

3. Set secrets (LLM provider key + Telegram bot token, at minimum):
   ```bash
   fly secrets set OPENROUTER_API_KEY=sk-or-... --app $APP
   fly secrets set TELEGRAM_BOT_TOKEN=123456:ABC... --app $APP
   ```

4. Deploy:
   ```bash
   fly deploy hermes-agent/ --app $APP
   ```

First deploy takes a few minutes (Docker build). After that, you're reachable on Telegram from anywhere.

## Cost

Roughly **~$15/month** on the default config (shared-cpu-2x / 2 GB RAM / 10 GB volume running 24/7), per the repo. Scales down if you don't need 24/7 availability — stop the Machine, Fly only charges for volume storage.

Volume snapshots are free for the first 10 GB and $0.08/GB/month beyond that.

## Persistence and Recovery

Everything durable lives on the Fly volume at `/opt/data`. That includes:

- `~/.hermes/` config, skills, memory files
- The SQLite session database
- Cron job definitions and output

Daily snapshots run automatically with 5-day retention (configurable up to 60 days). To restore:

```bash
fly volumes snapshots list <volume-id> --app $APP
fly volumes create hermes_data_restored \
  --snapshot-id <snapshot-id> --size 10 --app $APP
```

## Running the TUI

The main interface is still whichever messaging gateway you configured (Telegram, Discord, etc.). But if you need a CLI session — to run `hermes doctor`, inspect state, or do ad-hoc work — SSH into the Machine:

```bash
fly ssh console --app $APP
hermes    # native TUI, shares the same /opt/data as the gateway
```

TUI and gateway share state, so a conversation you start over SSH shows up in history the same as one you had on Telegram.

## Skills Needed

- Fly.io account with a card on file (Machines and volumes aren't always-free)
- `flyctl` installed locally
- An LLM provider key (OpenRouter works well)
- A messaging gateway credential (Telegram is easiest)

## Notes

- `shared-cpu-2x / 2 GB` fits one person with a few platforms. Heavy browser automation, Playwright, or RL work wants `shared-cpu-4x / 4 GB`:
  ```bash
  fly scale vm shared-cpu-4x --memory 4096 --app $APP
  fly volumes extend <volume-id> --size 20 --app $APP
  ```
- Bundled Hermes skills reconcile on boot without overwriting your edits — safe to `fly deploy` a new Hermes version.
- This is a Fly-maintained example, not a Nous Research product. If it falls behind Hermes releases, check the `hermes-agent` clone step and pull the latest manually.

## Sources

- Fly-apps example repo: <https://github.com/fly-apps/hermes-flyio>
- Hermes official deployment docs: <https://hermes-agent.nousresearch.com/docs/>
