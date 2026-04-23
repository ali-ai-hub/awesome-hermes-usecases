# Zero-Token Notifications

**Class:** Ecosystem integration · **Confidence:** Medium · **Demo status:** Community repo

## Pain Point

Cron-based alerts are expensive if they wake the LLM every run. "Check this RSS feed every 15 minutes" at $X per agent turn gets pricey fast — and 99% of the time there's nothing to report. You want the agent to only pay token cost when something *actually* changed.

## What It Does

The `agent-notifications` community repo uses Hermes's `--script` parameter to front-load the mechanical work: a Python script runs first, does the fetching and diffing, and writes its output to the agent's context. The agent only activates — and only produces a message — when the script output indicates a real change. If nothing changed, the prompt instructs the agent to return `[SILENT]`, which suppresses delivery entirely.

Net result: a GitHub-star checker, an RSS watcher, or a price monitor can poll every few minutes with near-zero token cost on quiet runs, and full agent reasoning on meaningful ones.

## Setup

1. Write a checker script. Drop it in `~/.hermes/scripts/`:

   ```python
   # ~/.hermes/scripts/watch-stars.py
   import json, os, urllib.request

   REPO = "NousResearch/hermes-agent"
   STATE = os.path.expanduser("~/.hermes/scripts/.stars-state.json")

   def get_stars():
       req = urllib.request.Request(
           f"https://api.github.com/repos/{REPO}",
           headers={"User-Agent": "hermes-watcher"},
       )
       return json.loads(urllib.request.urlopen(req).read())["stargazers_count"]

   prev = json.load(open(STATE))["count"] if os.path.exists(STATE) else None
   curr = get_stars()
   json.dump({"count": curr}, open(STATE, "w"))

   if prev is None:
       print("INITIAL", curr)
   elif curr == prev:
       print("NO_CHANGE")
   else:
       print(f"CHANGE {prev} -> {curr}")
   ```

2. Create a cron job that runs the script and only talks to the LLM on real change:

   ```bash
   hermes cron create "*/15 * * * *" \
     "If the script output starts with CHANGE, summarize in one line what
      changed and deliver. If it starts with NO_CHANGE or INITIAL, respond
      with only [SILENT]." \
     --script ~/.hermes/scripts/watch-stars.py \
     --name "Star watcher" \
     --deliver telegram
   ```

3. When the agent's reply contains `[SILENT]`, the gateway suppresses delivery — no Telegram message, no email, nothing.

## Pattern

The trick is separation:

- **Script handles the mechanical part.** Fetching, diffing, state tracking — all in Python, no LLM involved. Cheap, fast, deterministic.
- **Agent handles the reasoning.** Only when the script says something's different does the LLM get called to explain what and why.

## Skills Needed

- Cron with `--script` support (built in)
- A checker script in `~/.hermes/scripts/`
- Any messaging delivery target

## Sources

- Community repo: <https://github.com/Kuberwastaken/agent-notifications>
- Cron reference: <https://hermes-agent.nousresearch.com/docs/guides/automate-with-cron>
