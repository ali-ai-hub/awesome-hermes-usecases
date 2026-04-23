#!/usr/bin/env bash
# Open WebUI demo — smoke test.
# Confirms Docker, compose file, .env, and Hermes API server are ready.

set -euo pipefail

fail() { echo "FAIL: $*" >&2; exit 1; }
pass() { echo "OK:   $*"; }

command -v docker >/dev/null 2>&1 || fail "docker not on PATH"
pass "docker present"

docker compose version >/dev/null 2>&1 || fail "docker compose plugin missing"
pass "docker compose present"

[[ -f .env ]] || fail ".env missing — cp .env.example .env and set HERMES_API_KEY"
pass ".env present"

# shellcheck disable=SC1091
set -a; source .env; set +a

[[ -n "${HERMES_API_KEY:-}" ]] || fail "HERMES_API_KEY empty in .env"
pass "HERMES_API_KEY set"

# Check the Hermes API server is reachable and the key matches.
# If the gateway isn't running yet, this will fail and tell the user so.
if ! curl -sS --max-time 3 http://localhost:8642/v1/models \
     -H "Authorization: Bearer $HERMES_API_KEY" \
     -o /dev/null -w "%{http_code}" 2>/dev/null | grep -qE "^(200|204)$"; then
  echo "WARN: Hermes API server not reachable at http://localhost:8642/v1/models"
  echo "      Start it with: hermes gateway install"
  echo "      And: hermes config set api_server.enabled true"
  echo "           hermes config set api_server.key \"\$HERMES_API_KEY\""
  exit 2
fi
pass "Hermes API server responds to /v1/models"

echo
echo "Smoke test passed. Start Open WebUI with:"
echo "  docker compose up -d"
echo "Then visit http://localhost:3000"
