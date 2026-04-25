<p align="center">
  <img src="assets/hermes-agent-usecases.png" alt="Hermes Agent — Real-World Use Cases" width="800">
</p>

# Awesome Hermes Agent Use Cases

[![Awesome](https://awesome.re/badge.svg)](https://awesome.re)
![Use Cases](https://img.shields.io/badge/usecases-23-blue?style=flat-square)
![Last Update](https://img.shields.io/github/last-commit/ali-erfan-dev/awesome-hermes-usecases?label=Last%20Update&style=flat-square)
![Stars](https://img.shields.io/github/stars/ali-erfan-dev/awesome-hermes-usecases?style=flat-square)
![License](https://img.shields.io/badge/license-MIT-green?style=flat-square)

**A community collection of real-world [Hermes Agent](https://github.com/NousResearch/hermes-agent) use cases — each one backed by public evidence.**

| | This Catalog | Official Docs | X Threads | Reddit |
|---|---|---|---|---|
| Organized by category | ✅ | Partial | ❌ | ❌ |
| Runnable demos included | ✅ | ❌ | ❌ | ❌ |
| Primary source required | ✅ | ✅ | ❌ | ❌ |
| Community-maintained | ✅ | ❌ | ❌ | ❌ |

> [!NOTE]
> **Evidence rule.** Every use case here links to a primary source: an official Hermes doc, a Nous Research companion repo, a GitHub issue with deployment details, or a first-person blog post. If the only evidence is a tweet or "community build" marketing page, it lives in [`research/unverified.md`](research/unverified.md) instead — not in the catalog below.

## Quick start

New to Hermes Agent? The fastest path:

```bash
curl -fsSL https://raw.githubusercontent.com/NousResearch/hermes-agent/main/scripts/install.sh | bash
hermes setup
```

Then pick a use case below. The [`/demos`](demos/) folder has three runnable starters: [Daily Briefing](demos/daily-briefing/), [Open WebUI](demos/openwebui/), and [Team Telegram](demos/team-telegram/).

## Categories

- [Automation & Scheduling](#automation--scheduling)
- [Messaging & Team Bots](#messaging--team-bots)
- [Coding & Developer Workflows](#coding--developer-workflows)
- [Frontends & UIs](#frontends--uis)
- [Home & Device Control](#home--device-control)
- [Content & Creative Pipelines](#content--creative-pipelines)
- [Orchestration & Multi-Agent](#orchestration--multi-agent)
- [Memory & Context](#memory--context)
- [Deployment Patterns](#deployment-patterns)
- [Research & Training](#research--training)

## Automation & Scheduling

| Name | Description |
| --- | --- |
| [Daily Briefing Bot](usecases/daily-briefing-bot.md) | A scheduled agent that researches topics every morning and delivers a summary to Telegram or Discord. The canonical "hello world" of Hermes automation. |
| [Zero-Token Notifications](usecases/zero-token-notifications.md) | Cron jobs that only wake the LLM when something actually changed — pre-filter with a Python script, only pay for tokens on meaningful signal. |
| [Intent-to-Artifacts Workflow](usecases/intent-to-artifacts.md) | A personal workflow for turning rough prompts into runbooks, RSS curation, diagrams, and notes — delivered to Telegram + markdown files. |

## Messaging & Team Bots

| Name | Description |
| --- | --- |
| [Team Telegram Assistant](usecases/team-telegram-assistant.md) | Always-on shared bot for a small team — coding, research, ops — with per-user sessions, Docker-isolated terminal, and an allowlist. The gateway also supports Discord, Slack, WhatsApp, Signal, Matrix, Email, SMS, and more; the Telegram flow is the cleanest starting point for any of them. |
| [Enterprise Messaging (Feishu / WeCom)](usecases/enterprise-messaging-feishu-wecom.md) | Production-style Hermes deployments on Chinese enterprise chat platforms — Feishu managed under `launchd`, WeCom with native media-and-vision analysis. |
| [Voice Assistant Workflows](usecases/voice-assistant.md) | Three modes: CLI mic loop, voice notes in Telegram/Discord, and a Discord voice-channel bot. Same agent, same memory, voice-only I/O. |

## Coding & Developer Workflows

| Name | Description |
| --- | --- |
| [GitHub PR Review (cron)](usecases/github-pr-review-cron.md) | Periodic PR review without opening a webhook endpoint. Authenticated `gh`, a review skill, and a cron job. |
| [GitHub PR Review (webhook)](usecases/github-pr-review-webhook.md) | Real-time PR comments via a signed GitHub webhook. End-to-end event-driven code review. |
| [Production Software-Dev Workflow](usecases/production-software-dev-workflow.md) | A field report of daily production development on Hermes — long sessions, delegation, memory, one 12-hour run with ~2.6M replay tokens. |

## Frontends & UIs

| Name | Description |
| --- | --- |
| [Open WebUI Frontend](usecases/open-webui-frontend.md) | Point Open WebUI at the Hermes API server to get a full browser chat frontend for the agent, with session continuity. |

## Home & Device Control

| Name | Description |
| --- | --- |
| [Home Assistant Control](usecases/home-assistant-control.md) | Conversational control of a smart home via four built-in HA tools — list entities, read state, call services. |
| [Android Device Control](usecases/android-device-control.md) | Remote phone control from a Hermes chat — 36 `android_*` tools for taps, swipes, screenshots, and screen reading via a relay app. |

## Content & Creative Pipelines

| Name | Description |
| --- | --- |
| [Autonovel — House of Bells](usecases/autonovel-house-of-bells.md) | End-to-end autonomous novel, art, and audiobook production. Nous Research's own pipeline shipped a 19-chapter, 79,456-word book with an audiobook and a website. |
| [Printing-Factory Task Memory](usecases/printing-factory-task-memory.md) | A custom skill that fixes long-context slowness and forgetting during daily factory operations. Local JSON index with sub-second retrieval. |

## Orchestration & Multi-Agent

| Name | Description |
| --- | --- |
| [Paperclip Managed Employee](usecases/paperclip-managed-employee.md) | Hermes running as a worker inside Nous Research's Paperclip task-orchestration system, with persistent sessions and checkpoints. |
| [Self-Evolution](usecases/self-evolution.md) | A GEPA + DSPy loop that optimizes your Hermes skills, prompts, and tool text, producing PR-ready improvements for a few dollars per run. |
| [Zouroboros Swarm Bridge](usecases/zouroboros-swarm-bridge.md) | Hermes as one of four interchangeable executors (Claude Code, Codex, Gemini, Hermes) inside a third-party multi-agent orchestrator. Bash-bridge adapter pattern with shared identity. |

## Memory & Context

| Name | Description |
| --- | --- |
| [YantrikDB Cognitive Memory (via MCP)](usecases/yantrikdb-memory-mcp.md) | Replace or augment native memory with a dedicated cognitive DB — vector + knowledge graph + temporal decay + contradiction detection. Integrates over MCP, so no Hermes plugin needed. |

## Deployment Patterns

| Name | Description |
| --- | --- |
| [Hermes on Fly.io](usecases/hermes-on-flyio.md) | Official Fly-apps deployment guide — run Hermes as a Fly Machine with a volume-backed `/opt/data`, daily snapshots, and ~$15/month baseline. |
| [Local & Proxy Model Backends](usecases/local-and-proxy-models.md) | Run Hermes against Ollama, vLLM, oMLX, or a custom OpenAI-compatible proxy — for cost control, data locality, or model choice beyond the defaults. |

## Research & Training

| Name | Description |
| --- | --- |
| [Multi-Platform Social Media Research](usecases/multi-platform-research.md) | Run a single query across Reddit, X/Twitter, YouTube, Hacker News, and Polymarket via a single Python engine. Firefox-cookie auth for X, no API key needed on WSL. Delivered as a unified markdown brief to Telegram or local storage. |
| [RL Training & Benchmarks](usecases/rl-training-benchmarks.md) | Use Hermes environments to train and evaluate tool-calling models. The TBLite benchmark covers 100 tasks with strong correlation to TB2. |
| [Browser & Admin UIs](usecases/browser-admin-uis.md) | The official web dashboard plus community UIs — browser access to sessions, files, cron, and control plane. |

## Runnable demos

Three starter demos live in [`/demos`](demos/). Each has a `README.md`, a `.env.example`, and a one-command setup:

- [**daily-briefing**](demos/daily-briefing/) — cron + web search + Telegram delivery
- [**openwebui**](demos/openwebui/) — Hermes API server + Open WebUI via Docker Compose
- [**team-telegram**](demos/team-telegram/) — gateway + Telegram + Docker terminal backend

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md). The short version: **one primary source minimum** — official docs, a Nous companion repo, a GitHub issue with real deployment detail, or a first-person blog post. X posts and "community build" marketing pages don't count as primary evidence.

> Please only submit use cases you have personally run (at least once) or that you can trace to a primary public source. No crypto use cases.

## License

[MIT](LICENSE) for code and configs. Docs and diagrams under [CC BY 4.0](LICENSE-docs).

## Acknowledgements

Catalog format inspired by [awesome-openclaw-usecases](https://github.com/hesamsheikh/awesome-openclaw-usecases). Hermes Agent is built by [Nous Research](https://nousresearch.com).
