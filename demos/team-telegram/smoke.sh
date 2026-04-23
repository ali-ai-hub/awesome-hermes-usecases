#!/usr/bin/env bash
# Team Telegram — smoke test.
# Verifies prerequisites and that the security-relevant config is in place.

set -euo pipefail

fail() { echo "FAIL: $*" >&2; exit 1; }
pass() { echo "OK:   $*"; }
warn() { echo "WARN: $*" >&2; }

command -v hermes >/dev/null 2>&1 || fail "hermes CLI not on PATH"
pass "hermes CLI present"

command -v docker >/dev/null 2>&1 || fail "docker not on PATH"
pass "docker present"

[[ -f .env ]] || fail ".env missing — cp .env.example .env and fill it in"
pass ".env present"

# shellcheck disable=SC1091
set -a; source .env; set +a

[[ -n "${TELEGRAM_BOT_TOKEN:-}" ]] || fail "TELEGRAM_BOT_TOKEN empty in .env"
pass "TELEGRAM_BOT_TOKEN set"

[[ -n "${TELEGRAM_ALLOWED_USERS:-}" ]] || fail "TELEGRAM_ALLOWED_USERS empty in .env"
pass "TELEGRAM_ALLOWED_USERS set"

# Confirm Docker backend is selected — shared bots should never run the local backend.
backend="$(hermes config get terminal.backend 2>/dev/null || echo unknown)"
if [[ "$backend" != "docker" ]]; then
  warn "terminal.backend is '$backend' — expected 'docker' for a shared bot."
  warn "Run bash setup.sh to switch it."
  exit 2
fi
pass "terminal.backend is docker"

echo
echo "Smoke test passed. DM the bot on Telegram to confirm it responds."
