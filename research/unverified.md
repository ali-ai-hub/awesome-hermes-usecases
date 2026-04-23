# Unverified Backlog

This file tracks use cases that have been proposed but don't yet meet the evidence bar defined in [CONTRIBUTING.md](../CONTRIBUTING.md). They live here — not in the main catalog — until we can point to a primary source.

An entry gets promoted to [`/usecases`](../usecases/) once one of the following exists:

- Official Hermes docs, repo, or release notes that cover the pattern.
- An official Nous Research companion repo or blog post.
- A GitHub issue or PR with concrete deployment details.
- A first-person third-party blog post or repo that explicitly shows Hermes in the architecture.

## Current backlog

The entries below are derived from the initial fact-check of candidate sources. Each row names what would need to land for the entry to move into the verified catalog.

| Candidate | Why it's here | What would promote it |
| --- | --- | --- |
| **Telegram universal interface** | Pattern is real, but early sourcing was mostly social posts rather than docs. | Re-source to the official Telegram gateway docs and the team-telegram tutorial. Likely promotable today — see the existing [Team Telegram Assistant](../usecases/team-telegram-assistant.md) entry. |
| **Hermes as MCP server** | Feature exists, but needs to be grounded in a specific docs page or release note, not a third-party summary. Note: Hermes *consuming* MCP is real and well-documented (see [YantrikDB](../usecases/yantrikdb-memory-mcp.md) for an example). The open question is Hermes *exposing* itself as an MCP server to external clients. | A link to Hermes release notes or docs describing MCP server mode end-to-end. |
| **Zouroboros swarm bridge** | Third-party integration, early sourcing was light. | A repo that explicitly shows Hermes bridging, plus a README describing the architecture. Would come in as ecosystem integration, medium confidence. |
| **YantrikDB memory engine plugin** | Possible ecosystem plugin, but the original reference didn't clearly target Hermes. | A plugin repo that names Hermes as the integration target, with install steps that drop into `~/.hermes/plugins/`. |
| **Obsidian LLM wiki** | Interesting pattern, but was sourced from X only in the initial bundle. | Replace with the eBourgess "intent-to-artifacts" blog and official sessions/memory docs. Partially covered already by [Intent-to-Artifacts Workflow](../usecases/intent-to-artifacts.md); a dedicated Obsidian variant needs its own first-person source. |
| **Multi-agent code review pipeline** | Marketing-style summary, not a verified field deployment. | A blog post or repo describing a real multi-agent pipeline built on top of the [PR review tutorials](../usecases/github-pr-review-cron.md), with actual team usage evidence. Until then, the official PR review demos stand on their own. |
| **Daily standup automation** | Reasonable demo pattern, but no primary source showing it running in the wild. | Someone implements and writes it up (issue, blog, or repo). Until then, it's derivative of [Daily Briefing Bot](../usecases/daily-briefing-bot.md) with a different prompt. |
| **Daily business intelligence** | Same as above — a prompt variation on the briefing pattern, not a standalone verified deployment. | Primary evidence of a team using it. |
| **Competitor price monitoring** | Works as a prompt pattern for [Zero-Token Notifications](../usecases/zero-token-notifications.md), but no one has publicly documented running it long-term. | A write-up (blog, issue, repo) showing it deployed. |
| **Other "Community Build" / X-only entries** | Couldn't be cross-checked against docs, companion repos, or first-person write-ups. | Any primary source pointing to the pattern. |
| **Auto-update docs on refactor** | Pattern is reasonable but submission cited a fabricated URL. | Write-up grounded in the official [PR review cron](../usecases/github-pr-review-cron.md) or [webhook](../usecases/github-pr-review-webhook.md) tutorials with a real blog or repo link. |
| **Competitor price monitoring** | Submission cited a fabricated URL; pattern already covered by [Zero-Token Notifications](../usecases/zero-token-notifications.md). | A first-person write-up that extends the zero-token pattern with browser automation, posted publicly. |
| **Daily business intelligence** | Submission cited a fabricated URL; pattern is a Daily Briefing variant. | A first-person write-up of someone running this against Stripe/GA for real, not a re-skinned tutorial. |
| **AI executive team on Discord** | Submission used OpenClaw-style profile vocabulary; `wanikua/become-ceo` reference needs to be verified as a real Hermes deployment. | A README in the referenced repo that names Hermes and shows Hermes-specific primitives (gateway, skills, delegation). |
| **Raspberry Pi / edge deployment** | Pattern is reasonable but submission was framework-agnostic. Hermes officially supports Android/Termux on ARM. | A first-person write-up of Hermes on a Pi (or Termux) with specific model, config, and operational notes. |
| **Sim (visual workflow engine) × Hermes** | Sim is a real project but the submission didn't document the Hermes integration path. | A write-up showing Sim's MCP export consumed by Hermes as an MCP server, with config and a concrete use case. |

See the triage files for full rationale:
- [`submissions-triage-2026-04.md`](./submissions-triage-2026-04.md) — first batch (20 candidates)
- [`submissions-triage-2026-04-batch2.md`](./submissions-triage-2026-04-batch2.md) — second batch (6 candidates)

## How to promote an entry

If you find primary evidence for anything above, open a PR that:

1. Adds a proper use case file under `/usecases/` following the template in [CONTRIBUTING.md](../CONTRIBUTING.md).
2. Adds a row in the appropriate category table in [README.md](../README.md).
3. Removes the row from this file.

## How to add a new unverified entry

If you want to track a candidate that doesn't yet meet the bar, open a PR that adds a row here with:

- The candidate name
- A one-sentence reason it's here (what's missing)
- The minimum evidence that would promote it

Keeping the backlog visible is part of the point. Things get picked up faster when they're listed somewhere.
