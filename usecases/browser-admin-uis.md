# Browser & Admin UIs

**Class:** Ecosystem integration · **Confidence:** Medium · **Demo status:** Multiple UIs, uneven maturity

## Pain Point

The Hermes CLI is the primary interface, but teams want a browser view of what's happening — active sessions, session history, files in `~/.hermes/`, running cron jobs, a place to edit skills without touching the filesystem. A control plane, in other words.

## What It Does

Several browser frontends exist with different focuses:

- **Official web dashboard.** First-party, tracks the latest Hermes releases. Start here.
- **hermes-webui** (community). Session-centric UI with chat history and inspection.
- **hermes-control-interface** (community). Control-plane-style dashboard for state, cron, and files.
- **[Open WebUI](open-webui-frontend.md).** Not admin-focused but the cleanest chat experience; covered in its own page.

The ecosystem is real but uneven — some community UIs have multiple releases and real screenshots, others are early. Start official, fall back to community for the specific capability you need.

## Setup

**Official dashboard** — covered in the main docs. Enable it via Hermes config, visit the dashboard URL the gateway prints at startup.

**Community UIs** — each has its own install. Generally the pattern is: Hermes API server enabled, UI points at the Hermes endpoint with the same `API_SERVER_KEY`. Check the repo README for specifics.

## Recommendation

Adopt in this order:

1. **Official dashboard** — lowest risk, tracks upstream.
2. **Open WebUI** — if you want a polished chat experience shareable with non-technical users.
3. **Community admin UIs** — only if you need a specific capability the official dashboard doesn't cover yet.

Don't install three at once. Pick the one that solves your actual problem.

## Skills Needed

- Hermes API server enabled (for most UIs)
- Docker (recommended for community UIs)
- A reverse proxy with TLS if you expose any of these beyond localhost

## Security Notes

- A UI with control-plane access (edit files, create cron jobs, install skills) is a superuser surface. Protect it with TLS and auth at least as strong as SSH to the host.
- Community UIs haven't been audited by Nous. Review before you run.

## Sources

- Official web dashboard: <https://hermes-agent.nousresearch.com/docs/user-guide/features/web-dashboard>
- `hermes-webui`: <https://github.com/nesquena/hermes-webui>
- `hermes-control-interface`: <https://github.com/xaspx/hermes-control-interface>
