#!/usr/bin/env bash
# Daily Briefing — Telegram delivery.
# Creates a cron job that delivers a morning brief to Telegram.
# Prereq: Telegram already configured in `hermes setup`.

set -euo pipefail

if [[ -f .env ]]; then
  # shellcheck disable=SC1091
  set -a; source .env; set +a
else
  echo "Missing .env — copy .env.example to .env and fill it in first." >&2
  exit 1
fi

for var in FIRECRAWL_API_KEY TELEGRAM_BOT_TOKEN TELEGRAM_ALLOWED_USERS; do
  if [[ -z "${!var:-}" ]]; then
    echo "$var is empty in .env — required for Telegram delivery." >&2
    exit 1
  fi
done

if ! command -v hermes >/dev/null 2>&1; then
  echo "hermes CLI not found on PATH." >&2
  exit 1
fi

# Parallel delegation variant — faster than serial search for multi-topic briefs.
hermes cron create "0 8 * * *" \
  "Create a morning briefing by delegating research to sub-agents.
   Delegate three parallel tasks:
   1. Delegate: top 2 AI/ML stories from the past 24 hours with links
   2. Delegate: top 2 developer-tools stories from the past 24 hours with links
   3. Delegate: top 2 general tech news stories from the past 24 hours with links
   Collect all results and combine them into a single clean briefing with
   section headers, emoji formatting, and source links.
   Add today's date as a header." \
  --name "Morning brief (telegram)" \
  --deliver telegram

echo
echo "Cron job 'Morning brief (telegram)' created — delivery: telegram."
echo
echo "Trigger once now to confirm delivery:"
echo "  hermes cron run \"Morning brief (telegram)\""
