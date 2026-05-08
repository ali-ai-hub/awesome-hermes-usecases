# X Social Automation Toolset

**Class:** Ecosystem integration · **Confidence:** Medium-High · **Demo status:** Published plugin + runbook

## Pain Point

Hermes can research and write, but X/Twitter workflows usually force the agent
to leave the Hermes tool model. Teams need a controlled way to search posts,
read account state, check trends, and perform approved social actions without
handing the agent a generic browser session.

## What It Does

Hermes Tweet installs as a native Hermes Agent plugin backed by Xquik. It
registers a dedicated `hermes-tweet` toolset with separate exploration, read,
and action tools:

- `tweet_explore` searches the generated Xquik endpoint catalog without network
  credentials.
- `tweet_read` calls safe read-only endpoints after an API key is configured.
- `tweet_action` is blocked unless the operator explicitly enables write
  actions with `HERMES_TWEET_ENABLE_ACTIONS=true`.

The same package also bundles a Hermes skill and slash commands for account
status and trends, so an operator can use natural language, direct tool calls,
or `/xstatus` and `/xtrends` inside an active Hermes session.

## Setup

Install and enable the plugin from the public repository:

```bash
hermes plugins install Xquik-dev/hermes-tweet --enable
```

For non-interactive hosts, install the Python package inside the Hermes
environment and enable it:

```bash
~/.hermes/hermes-agent/venv/bin/python -m pip install hermes-tweet
hermes plugins enable hermes-tweet
hermes tools list
```

Set `XQUIK_API_KEY` in `~/.hermes/.env` before using `tweet_read`. If Hermes is
already running, use `/reload` in the interactive CLI, or restart gateway and
cron sessions so the updated environment is loaded. Leave
`HERMES_TWEET_ENABLE_ACTIONS` unset unless the current run is allowed to perform
write actions.

## Prompts

Explore the available X endpoints without credentials:

```text
Use tweet_explore to find X/Twitter search endpoints. Do not call tweet_action.
Return the safest read endpoint and required query fields.
```

Read account state after configuring `XQUIK_API_KEY`:

```text
Use tweet_explore, then read /api/v1/account with tweet_read.
Summarize the account status and do not call tweet_action.
```

Monitor trends from an interactive session:

```text
/xtrends
```

Operator-approved posting flow:

```text
Draft a short product update for X. Before any write, show the exact endpoint,
method, and JSON body you would send through tweet_action. Wait for approval.
```

## Skills Needed

- Hermes plugin system
- `hermes-tweet` toolset
- Xquik API key for read calls
- Optional: Hermes cron or gateway for scheduled monitoring

## Notes

- The default posture is read-first. Write actions require a separate
  environment flag and an explicit operator-approved payload.
- `hermes tools list` is the scriptable diagnostics command for current Hermes
  v0.12.x runtimes; bare `hermes tools` opens an interactive UI.
- This is a focused Xquik integration, not a general social scheduler. Use it
  when Hermes needs direct X data and action endpoints.

## Sources

- Hermes Tweet repository: <https://github.com/Xquik-dev/hermes-tweet>
- Hermes Tweet guide: <https://docs.xquik.com/guides/hermes-tweet>
- PyPI package: <https://pypi.org/project/hermes-tweet/>
- AgentSkill listing: <https://agentskill.sh/@xquik-dev/hermes-tweet>
