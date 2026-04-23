# Team Telegram Demo

A runnable setup for the [Team Telegram Assistant](../../usecases/team-telegram-assistant.md) use case. Gets a Hermes Telegram bot running on a VPS with the Docker terminal backend (so shell tools are sandboxed) and a user allowlist.

## What you'll end up with

- A Telegram bot that responds only to users on your allowlist.
- Per-user sessions — each teammate has their own memory and context.
- Docker-backed terminal tool — `rm -rf` at worst destroys a container.
- Optional home channel for cron delivery and alerts.

## Prerequisites

- A VPS (or any Linux/macOS machine) running Hermes Agent, reachable on the internet.
- Docker installed on the host (required for the Docker terminal backend).
- A Telegram bot from [@BotFather](https://t.me/BotFather) — save the token.
- Your Telegram user ID from [@userinfobot](https://t.me/userinfobot) (and the IDs of anyone else you want to allow).

## Setup

1. Copy `.env.example` to `.env` and fill it in:
   ```bash
   cp .env.example .env
   # edit .env
   ```

2. Apply the config and install the gateway as a service:
   ```bash
   bash setup.sh
   ```

   The script:
   - Sets `TELEGRAM_BOT_TOKEN`, `TELEGRAM_ALLOWED_USERS`, and (if provided) `TELEGRAM_HOME_CHANNEL` via `hermes config`.
   - Switches the terminal backend to Docker.
   - Installs the gateway as a user systemd service so it survives reboot.

3. DM your bot on Telegram. It should respond. If you added teammates to the allowlist, they can DM it too — each gets their own session.

## Adding a home-channel cron job

Once the home channel is set, any cron job with `--deliver telegram` will post there. Example: a nightly PR digest for a repo you maintain.

```bash
hermes cron create "0 22 * * *" \
  "List PRs on YOUR_ORG/YOUR_REPO merged in the last 24h. Group by
   author. Keep under 300 words." \
  --name "Nightly PR digest" \
  --deliver telegram
```

## Security checklist before you share this

- [ ] `TELEGRAM_ALLOWED_USERS` contains only people you trust to run arbitrary code.
- [ ] Terminal backend is `docker`, not `local`. Check: `hermes config get terminal.backend`.
- [ ] Model provider keys are in Hermes config, not in the Telegram chat.
- [ ] If the bot is in a group, the group is private and limited to allowlisted members.

## Sources

- Official tutorial: <https://hermes-agent.nousresearch.com/docs/guides/team-telegram-assistant/>
