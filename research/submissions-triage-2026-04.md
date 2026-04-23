# Submission Triage — April 2026

A verdict on 20 candidate use cases submitted for inclusion. Each was evaluated against the evidence rule in [CONTRIBUTING.md](../CONTRIBUTING.md) and against a second test the rule doesn't explicitly cover: **does the write-up describe Hermes Agent specifically, or is it framework-agnostic?**

The second test matters. Many of the submissions use vocabulary like "the agent framework," "isolated profiles," and "the model" without any Hermes-specific primitive (`hermes gateway`, `~/.hermes/`, `hermes cron create`, `SKILL.md`, the Docker terminal backend, delegation, `[SILENT]`, MCP mode, `~/.hermes/skills/`). Applying that test surfaces a pattern: most entries could describe any agent framework, and a few are demonstrably about other systems.

Three terms recur in the submissions — **agent profiles**, **memory namespaces**, **Commander/Architect/Engineering** roles — that are not Hermes primitives. They're OpenClaw vocabulary. Several submissions appear to be OpenClaw use cases with the product name swapped out. That's a specific red flag to watch for in future contributions.

## Summary

| # | Submission | Verdict |
|---|---|---|
| 1 | `agentcash-autonomous-wallet` | **Reject** — crypto (off-limits per CONTRIBUTING) |
| 2 | `ai-executive-team-discord` | **Reject** — framework-agnostic, not Hermes-specific |
| 3 | `arxiv-research-loop` | **Reject** — "Community Build" source, framework-agnostic |
| 4 | `auto-update-docs-on-refactor` | **Reject as submitted** — fabricated source (`hermes-agent.ai`); keep as backlog candidate |
| 5 | `client-pre-call-research` | **Reject** — "Community Build" source, framework-agnostic |
| 6 | `competitor-price-monitoring` | **Reject as submitted** — fabricated source; already covered by [Zero-Token Notifications](../usecases/zero-token-notifications.md) |
| 7 | `daily-business-intelligence` | **Reject as submitted** — fabricated source; already covered by [Daily Briefing Bot](../usecases/daily-briefing-bot.md) |
| 8 | `daily-standup-automation` | **Reject** — "Community Build" source, derivative of Daily Briefing |
| 9 | `decision-game-theory-agent` | **Reject** — "Community Build" source, framework-agnostic |
| 10 | `flyhermes-webui` | **Accept as ecosystem mention** — real third-party hosting service; not a use case per se |
| 11 | `formal-verification-specialist` | **Reject** — "Community Build" source, no Hermes specificity |
| 12 | `hermes-as-mcp-server` | **Keep in backlog** — pattern is real, needs primary docs source |
| 13 | `hermes-control-interface` | **Already in catalog** — covered by [Browser & Admin UIs](../usecases/browser-admin-uis.md) |
| 14 | `hermes-mini-app-telegram` | **Reject** — "Community Build" source |
| 15 | `hermes-top-terminal-monitor` | **Reject** — "Community Build" source; touches internals (SQLite path) without a primary ref |
| 16 | `hindsight-supermemory` | **Reject as submitted** — source doesn't mention Hermes |
| 17 | `multi-agent-code-review-pipeline` | **Reject** — "Community Build" source; superseded by [PR review cron](../usecases/github-pr-review-cron.md) |
| 18 | `multi-agent-orchestration` | **Reject** — X-only source, OpenClaw-style vocabulary |
| 19 | `multi-node-home-cluster` | **Reject** — X-only source, no primary evidence |
| 20 | `obsidian-llm-wiki` | **Keep in backlog** — pattern is real, X-only source; see [Intent-to-Artifacts](../usecases/intent-to-artifacts.md) |

**Net result: 0 accepted to the main catalog, 1 ecosystem mention worth adding, 2 kept in the unverified backlog, 17 rejected.**

There's also a **new discovery** worth adding that emerged from this review: the official **`fly-apps/hermes-flyio`** repo is a primary-sourced Hermes-on-Fly.io deployment guide from Fly.io itself. See the recommendation at the bottom of this file.

## Per-entry rationale

### 1. `agentcash-autonomous-wallet` — Reject

Crypto use cases are off-limits per `CONTRIBUTING.md`. That's the end of the analysis regardless of source quality.

### 2. `ai-executive-team-discord` — Reject

The source (`wanikua/become-ceo`) needs verification, but the deeper issue is the write-up: "agent profiles mapped to channels," "restricts tool access per profile," "Commander profile," "Engineering profile." Those are OpenClaw primitives. Hermes has one agent with skills and memory, plus subagent delegation; it doesn't have the profile-and-channel-mapping architecture this describes. This reads like an OpenClaw use case with the product name swapped. If the `become-ceo` repo does exist and does use Hermes, a rewrite grounded in actual Hermes primitives (one gateway, multiple Discord channels, skill-scoped delegation) could work — but as submitted, it's not Hermes.

### 3. `arxiv-research-loop` — Reject

Source is "Community Build" — not a primary source per CONTRIBUTING. The write-up is also generic: "the agent queries the API," "the agent writes the algorithmic implementation," "sandboxed execution environment (Docker)." Nothing here couldn't describe AutoGPT, OpenClaw, or plain LangChain. No mention of Hermes's actual code-execution path (the `execute_code` tool, Docker/Singularity/Modal terminal backends, RPC subagents).

### 4. `auto-update-docs-on-refactor` — Reject as submitted, backlog candidate

The pattern is reasonable and maps cleanly to the existing PR review demos, but the source `hermes-agent.ai/` is a third-party commercial marketing site — there is no documented Hermes tutorial at that URL. **Official docs live at `hermes-agent.nousresearch.com`.** Citing `hermes-agent.ai` as a primary source is the same mistake the original research report flagged: treating marketing pages as documentation.

If someone writes up this workflow grounded in the actual [PR review cron](../usecases/github-pr-review-cron.md) and [webhook](../usecases/github-pr-review-webhook.md) tutorials, it could earn a spot. Filed to backlog.

### 5. `client-pre-call-research` — Reject

"Community Build" source fails the evidence rule. Write-up is also framework-agnostic — no Hermes cron, no skill, no gateway delivery. This is a prompt pattern, not a Hermes use case.

### 6. `competitor-price-monitoring` — Reject as submitted

Same problem as #4: `hermes-agent.ai` isn't the docs site. The submitted pattern (browser + selectors + SQLite diff + notification) is also just a manual reimplementation of the `--script` pre-filter already documented in the [Zero-Token Notifications](../usecases/zero-token-notifications.md) entry. If someone uses Hermes's native pattern (script fetches, agent reasons, `[SILENT]` on no-change) and documents it publicly, that's a different submission.

### 7. `daily-business-intelligence` — Reject as submitted

Same fabricated source (`hermes-agent.ai`). And the described pattern is "cron + API fetch + format + send" — which is the [Daily Briefing Bot](../usecases/daily-briefing-bot.md) applied to Stripe/Analytics instead of news. Nothing Hermes-specific, no distinct architecture worth a new entry.

### 8. `daily-standup-automation` — Reject

"Community Build" source. Content-wise, this is another Daily Briefing variant: query an API, format, post to chat. No new pattern, no primary evidence of someone running it. The original research report flagged this one too.

### 9. `decision-game-theory-agent` — Reject

"Community Build" source. Content is literally "put game-theory frameworks in the system prompt." That's prompt engineering, not an agent use case. The write-up is also cautious about saying anything Hermes-specific — no skill file, no memory pattern, no tools.

### 10. `flyhermes-webui` — Accept as ecosystem mention

FlyHermes (`flyhermes.ai`) is a real paid hosting service for Hermes. Verified: the landing page markets itself as cloud-hosted Hermes, and a separate marketing site advertises it at $29.50/first month. But:

- This isn't a *use case* — it's a paid deployment option.
- It's a commercial third-party product, not an official Nous offering.
- The official doc page [`hermes-agent.org`](https://hermes-agent.org/) and the [Nous docs](https://hermes-agent.nousresearch.com/) already cover self-hosting thoroughly; this is a paid alternative.

**Recommendation:** add a one-line mention under "Browser & Admin UIs" as a commercial hosting option, not a standalone use case.

### 11. `formal-verification-specialist` — Reject

"Community Build" source. The pattern (agent drafts Certora specs, runs prover, parses errors, iterates) is plausible but entirely framework-agnostic — "shell execution for CLI," "file read/write for specs," "git access." Could be anything.

### 12. `hermes-as-mcp-server` — Keep in backlog

MCP support is real in Hermes (confirmed in the official docs: "MCP support — Connect to any MCP server for extended tool capabilities"). But the submission describes Hermes *as* an MCP server (Hermes exposing its own tools via MCP transport to external clients). That's a different capability. It's plausible — Nous has hinted at this direction — but the submission cites "Community Reports," which is not a primary source. Needs a specific docs page or release note to promote.

Already listed in [`unverified.md`](./unverified.md).

### 13. `hermes-control-interface` — Already covered

The submission is mostly accurate (confirmed against the real `xaspx/hermes-control-interface` repo) and is already covered by the [Browser & Admin UIs](../usecases/browser-admin-uis.md) entry. No action needed.

### 14. `hermes-mini-app-telegram` — Reject

"Community Build" source. The pattern (embed a Telegram Mini App in front of a Hermes instance) is technically plausible but there's no evidence anyone has actually built and published it. Pure speculation.

### 15. `hermes-top-terminal-monitor` — Reject

"Community Build" source. The submission also advises reading Hermes's state database directly with SQL — Hermes does use SQLite, but "write bash commands against `sessions.db`" is the kind of advice that ages poorly as internals change. The [docs](https://hermes-agent.nousresearch.com/docs/) expose session state through documented commands (`hermes` CLI, API server, dashboard), not through raw DB reads. Not a pattern to promote.

### 16. `hindsight-supermemory` — Reject as submitted

Cites `vectorize.io` as the source. That page is real but doesn't mention Hermes Agent. The write-up asserts an integration ("Update the agent's `config.yaml`") that isn't documented anywhere primary. If Vectorize, Supermemory, or Hindsight publish a Hermes integration, that integration becomes citable; until then, this is speculation.

### 17. `multi-agent-code-review-pipeline` — Reject

"Community Build" source. The pattern (three profiles: diff-reader, test-runner, synthesizer) is already superseded by the official PR review demos, which achieve the same thing with one agent and subagent delegation — which is how Hermes is actually designed to work. Rebuilding it as three separate "profiles" is an OpenClaw-style approach misapplied to Hermes. Original research report already rejected this one.

### 18. `multi-agent-orchestration` — Reject

X-only source (`canghe on X`). The vocabulary is explicitly OpenClaw: "Commander profile," "Architect Veto," "Market/Product/Architect/Dev/Test profiles." That five-role pipeline is a known OpenClaw pattern. Hermes's equivalent is the single-agent-plus-subagent-delegation architecture; they solve the same problem but the terminology doesn't transfer. This is almost certainly an OpenClaw use case with names swapped.

### 19. `multi-node-home-cluster` — Reject

X-only source (`@sephmartinmusic`). Pattern is "run Docker containers on multiple mini-PCs behind a reverse proxy." That's a deployment pattern for any containerized service, not a Hermes-specific use case. No primary evidence of someone running it.

### 20. `obsidian-llm-wiki` — Keep in backlog

X-only source (`shouyi111111 on X`) fails the evidence rule, but the underlying pattern is real and partially covered by [Intent-to-Artifacts](../usecases/intent-to-artifacts.md) — which has a first-person blog source. If someone writes up a dedicated Hermes + Obsidian workflow with a blog or repo, that can become its own entry. Already listed in [`unverified.md`](./unverified.md).

## Worth adding: Hermes on Fly.io

A better use of the time spent reviewing these 20 submissions is the accidental discovery during fact-checking: **`github.com/fly-apps/hermes-flyio`** is an official Fly.io deployment guide for Hermes Agent, published by Fly itself. It describes the complete flow — `flyctl` setup, volume-backed persistence at `/opt/data`, Telegram gateway, cost estimates (~$15/month), daily snapshots, scale commands. That's a primary source from a major infrastructure provider.

Recommended new use case: **Hermes on Fly.io (Serverless Deployment)**, class: ecosystem integration, confidence: High. It would fit naturally under a new "Deployment Patterns" category alongside the existing self-host documentation. If you want, I can draft that entry and add it to the catalog.

## Recurring patterns to reject quickly in future submissions

1. **"Community Build" or "Community Reports" as source.** Not a primary source. Reject unless paired with a real repo or blog.
2. **X / Twitter as sole source.** Goes to the unverified backlog, not the catalog.
3. **`hermes-agent.ai` as a cited docs URL.** It's a marketing site, not the docs. The real docs are `hermes-agent.nousresearch.com`.
4. **OpenClaw vocabulary.** "Agent profiles mapped to channels," "Commander/Architect profiles," "profile isolation," "strict role separation with sequential handoffs" — these are OpenClaw-native concepts. Hermes uses single-agent-plus-subagent-delegation. Submissions that describe multi-profile architectures are almost certainly OpenClaw patterns with the product name swapped.
5. **Framework-agnostic language only.** If the write-up works equally well for LangChain or AutoGPT, it's not a Hermes use case — it's generic agent talk.
