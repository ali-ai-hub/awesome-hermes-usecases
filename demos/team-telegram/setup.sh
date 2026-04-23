#!/usr/bin/env bash
# Team Telegram — setup.
# Applies config from .env, switches terminal backend to Docker,
# and installs the gateway as a user service.

set -euo pipefail

if [[ -f .env ]]; then
  # shellcheck disable=SC1091
  set -a; source .env; set +a
else
  echo "Missing .env — copy .env.example to .env and fill it in first." >&2
  exit 1
fi

for var in TELEGRAM_BOT_TOKEN TELEGRAM_ALLOWED_USERS; do
  if [[ -z "${!var:-}" ]]; then
    echo "$var is empty in .env — required." >&2
    exit 1
  fi
done

if ! command -v hermes >/dev/null 2>&1; then
  echo "hermes CLI not on PATH. Install it first:" >&2
  echo "  curl -fsSL https://raw.githubusercontent.com/NousResearch/hermes-agent/main/scripts/install.sh | bash" >&2
  exit 1
fi

if ! command -v docker >/dev/null 2>&1; then
  echo "docker not on PATH — the Docker terminal backend requires Docker." >&2
  echo "Install Docker and re-run." >&2
  exit 1
fi

echo "Applying Telegram config..."
hermes config set platforms.telegram.bot_token "$TELEGRAM_BOT_TOKEN"
hermes config set platforms.telegram.allowed_users "$TELEGRAM_ALLOWED_USERS"

if [[ -n "${TELEGRAM_HOME_CHANNEL:-}" ]]; then
  hermes config set platforms.telegram.home_channel "$TELEGRAM_HOME_CHANNEL"
  echo "Home channel set — cron jobs with --deliver telegram will post there."
fi

echo "Switching terminal backend to Docker (sandboxed shell tools)..."
hermes config set terminal.backend docker

echo "Installing gateway as a user service..."
hermes gateway install

echo
echo "Done. DM your bot on Telegram to test. Allowed user IDs:"
echo "  $TELEGRAM_ALLOWED_USERS"
echo
echo "Verify the backend is Docker (not local) before sharing the bot:"
echo "  hermes config get terminal.backend"
