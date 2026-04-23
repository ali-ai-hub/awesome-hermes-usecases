#!/usr/bin/env bash
# Daily Briefing — local delivery.
# Creates a cron job that writes a daily brief to ~/.hermes/cron/output/.
# Run from this directory after editing .env.

set -euo pipefail

if [[ -f .env ]]; then
  # shellcheck disable=SC1091
  set -a; source .env; set +a
else
  echo "Missing .env — copy .env.example to .env and fill it in first." >&2
  exit 1
fi

if [[ -z "${FIRECRAWL_API_KEY:-}" ]]; then
  echo "FIRECRAWL_API_KEY is empty. Web search won't work without it." >&2
  exit 1
fi

if ! command -v hermes >/dev/null 2>&1; then
  echo "hermes CLI not found on PATH. Install it first:" >&2
  echo "  curl -fsSL https://raw.githubusercontent.com/NousResearch/hermes-agent/main/scripts/install.sh | bash" >&2
  exit 1
fi

hermes cron create "0 8 * * *" \
  "Every morning at 8am, search the web for the latest news about AI agents,
   open-source LLMs, and agentic coding tools. Find 5 recent articles from
   the past 24 hours. Summarize the top 3 in a concise briefing with links.
   Use a friendly, professional tone. Add today's date as a header." \
  --name "Morning brief" \
  --deliver local

echo
echo "Cron job 'Morning brief' created — delivery: local."
echo "Brief will write to: ~/.hermes/cron/output/"
echo
echo "Trigger once now to confirm it works:"
echo "  hermes cron run \"Morning brief\""
