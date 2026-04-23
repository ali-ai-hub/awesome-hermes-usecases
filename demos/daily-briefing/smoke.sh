#!/usr/bin/env bash
# Daily Briefing — smoke test.
# Verifies wiring without requiring real API calls to complete.
# Exits 0 if the expected commands exist and respond.

set -euo pipefail

fail() { echo "FAIL: $*" >&2; exit 1; }
pass() { echo "OK:   $*"; }

command -v hermes >/dev/null 2>&1 \
  || fail "hermes CLI not on PATH"
pass "hermes CLI present"

hermes --version >/dev/null 2>&1 \
  || fail "hermes --version failed"
pass "hermes --version runs"

hermes cron list >/dev/null 2>&1 \
  || fail "hermes cron list failed — is the gateway installed?"
pass "hermes cron list runs"

[[ -f .env ]] || fail ".env missing — copy .env.example to .env first"
pass ".env present"

echo
echo "Smoke test passed."
echo "Next: bash setup-local.sh  (or setup-telegram.sh if Telegram is configured)"
