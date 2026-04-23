# Team Telegram Assistant

**Class:** First-party demo · **Confidence:** High · **Demo status:** [Runnable](../demos/team-telegram/)

## Pain Point

A small team wants a shared always-on assistant for coding, research, and ops — one that anyone can DM or mention in the group chat, with per-user context, without paying for a SaaS and without exposing a raw shell to everyone.

## What It Does

Hermes runs on a VPS with the Telegram gateway enabled. Authorized users DM the bot directly for private sessions, or mention it in a shared group for collaborative work. Each user gets their own session state and memory. Commands that touch the terminal are routed through the Docker backend, so a `rm -rf` at worst destroys a container, not the host.

A home channel collects cron output and alerts; daily briefings, GitHub triage, and backup reports all flow there.

## Setup

1. Create a bot with [@BotFather](https://t.me/BotFather) on Telegram. Save the token.
2. Get your Telegram user ID from `@userinfobot` for the allowlist.
3. Install Hermes and run the wizard:
   ```bash
   curl -fsSL https://raw.githubusercontent.com/NousResearch/hermes-agent/main/scripts/install.sh | bash
   hermes setup
   ```
4. In `.env` (or via `hermes config set`):
   ```
   TELEGRAM_BOT_TOKEN=123456789:AAH...
   TELEGRAM_ALLOWED_USERS=123456789,987654321
   TELEGRAM_HOME_CHANNEL=-1001234567890     # optional — cron delivery target
   ```
5. Switch the terminal backend to Docker so shell tools run in isolation:
   ```bash
   hermes config set terminal.backend docker
   ```
6. Start the gateway:
   ```bash
   hermes gateway install           # user service
   # or: sudo hermes gateway install --system   (systemd, boot-time)
   ```

## Prompts

Once the gateway is running, just DM the bot normally. Some patterns that work well on a shared bot:

```
@your_bot_name help me draft a reply to this customer:
> [paste customer message]
```

```
/cron add "0 9 * * 1" "Weekly status: pull last 7 days of merged PRs
from gh pr list --repo YOUR_ORG/YOUR_REPO --state merged, group by
author, and post to the home channel."
```

## Skills Needed

- Telegram gateway
- Docker terminal backend (recommended)
- Delegation (for longer-running research tasks)
- Cron (for scheduled team reports)

## Security Notes

- Keep the allowlist tight. Anyone in `TELEGRAM_ALLOWED_USERS` gets full agent access.
- Docker backend is not optional for a shared bot — a local backend means any authorized user can run anything as the VPS user.
- A $5 VPS is sufficient per the docs; the constraint is RAM for the model's context, not CPU.

## Sources

- Official tutorial: <https://hermes-agent.nousresearch.com/docs/guides/team-telegram-assistant/>
- Gateway docs: <https://hermes-agent.nousresearch.com/docs/user-guide/messaging/>
