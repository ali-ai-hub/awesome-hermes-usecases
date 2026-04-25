# Multi-Platform Social Media Research (last30days)

**Class:** Independent deployment · **Confidence:** Medium-High · **Demo status:** Custom skill + runbook

## Pain Point

When you need to understand what people are *actually* saying about a topic — not curated blog posts or press releases — you face a wall. Reddit requires browsing hostile mobile designs. X/Twitter gates search behind a login wall. YouTube has great content but no transcript search. Hacker News has signal but requires constant monitoring. Each platform has its own friction, and there's no unified way to pull them all at once.

## What It Does

A Hermes skill that runs a single query against five platforms simultaneously — Reddit, X/Twitter, YouTube, Hacker News, and Polymarket — and returns a unified digest of what people have been talking about in the last 30 days. No platform accounts needed: X authentication uses the agent's own Firefox cookie store directly from WSL.

The research engine is a well-structured Python script that orchestrates parallel web searches, deduplicates results, enriches posts with comment threads and video transcripts, and renders a single markdown brief. The agent can then route that brief to Telegram, Discord, an Obsidian vault, or local storage.

A typical session looks like this:

```
> /last30days "nvidia earnings" --x-handle=AlphaSignalAI,exelsiorai \
    --subreddits=investing,wallstreetbets,technology \
    --emit=compact
```

The agent delegates the heavy lifting to the Python engine, parses the results, and delivers a formatted brief with sentiment, key quotes, and source links.

## Setup

1. **Install the skill**: Clone the last30days skill into your Hermes skill directory:

   ```bash
   git clone https://github.com/mvanhorn/last30days-skill \
     ~/.hermes/skills/research/last30days
   ```

2. **Configure Firefox cookie access**: In WSL, point to your Windows Firefox profile so the engine can authenticate to X without a separate API key:

   ```bash
   mkdir -p ~/.config/last30days
   cat > ~/.config/last30days/.env <<'EOF'
   SETUP_COMPLETE=true
   X_BACKEND=bird
   # Adjust path to your Firefox profile
   FIREFOX_COOKIE_PATH=/mnt/c/Users/$USER/AppData/Roaming/Mozilla/Firefox/Profiles/*.default-release/cookies.sqlite
   EOF
   ```

3. **Verify the engine runs standalone**:

   ```bash
   /usr/bin/python3.12 ~/.hermes/skills/research/last30days/scripts/last30days.py \
     --help
   ```

4. **Register the skill in Hermes**: Ensure `SKILL.md` is present in the skill directory so Hermes auto-discovers the `last30days` command.

## Prompts

Single-topic research, delivered to Telegram:

```
Run last30days research on "AI coding agents" and deliver a compact digest
with the top Reddit threads, X posts, and YouTube videos from the last 30
days. Include one sentence summary per source, sentiment, and a link.
Send to telegram.
```

Targeted research with subreddit and X handle filters:

```
/last30days "scrolling LLM benchmarks"
  --subreddits=LocalLLaMA,machinelearningnews
  --x-handle=teortaxes
  --emit=compact
  --deliver telegram
```

Scheduled weekly competitor monitoring (cron):

```
/cron add "0 9 * * 1" "Run last30days research on 'nous research hermes agent'
for the past week. Focus on Reddit, Hacker News, and X. Deliver a summary
brief with top 5 sources and sentiment to telegram."
```

## Skills Needed

- `last30days` (Python research engine wrapper)
- Web search / Firecrawl (for enrichment fallback)
- Messaging gateway (Telegram / Discord for delivery)
- Optional: Obsidian Note-Taking skill (for persistent vault storage)

## Notes

- The Bird authentication backend reads Firefox profile cookies directly — no X API key needed, but you must have a logged-in Firefox session on the host machine.
- This works best from a WSL + Windows Firefox setup because the cookie path is a transparent mount. On pure Linux, you need a separate cookie jar or Bird auth.
- For topics where X and Reddit are blocked, YouTube auto-generated transcripts are the best fallback (install `yt-dlp` + `ffmpeg`).
- Polymarket data is included to gauge sentiment from prediction markets (useful for financial, political, or product topics).

## Sources

- last30days skill repository (runbook + Python engine): <https://github.com/mvanhorn/last30days-skill>
- Bird browser-cookie Twitter/X search library: vendored in the skill at `scripts/lib/vendor/bird-search/` — reads Firefox cookies directly without a separate X API
- YouTube transcript extraction (`yt-dlp`): <https://github.com/yt-dlp/yt-dlp>
