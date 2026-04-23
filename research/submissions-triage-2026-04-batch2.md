# Submission Triage — April 26, 2026 (Batch 2)

A verdict on 6 additional candidate use cases submitted after the first batch. Same rules as [`submissions-triage-2026-04.md`](./submissions-triage-2026-04.md): evidence rule + Hermes-specific vs. framework-agnostic + no OpenClaw vocabulary.

## Summary

| # | Submission | Verdict |
|---|---|---|
| 1 | `raspberry-pi-edge-deployment` | **Reject** — "Community Build" source, framework-agnostic write-up |
| 2 | `second-brain-does-things` | **Reject** — "Community Reports" source, ignores Hermes's native memory |
| 3 | `sim-visual-workflow` | **Reject** — describes Sim, not a Hermes use case |
| 4 | `telegram-universal-interface` | **Reject** — redundant with existing [Team Telegram Assistant](../usecases/team-telegram-assistant.md) |
| 5 | `yantrikdb-memory-engine` | **Rewrite and accept** — real project, wrong integration path as submitted; now shipping as [YantrikDB Memory (via MCP)](../usecases/yantrikdb-memory-mcp.md) |
| 6 | `zouroboros-swarm-bridge` | **Accept** — real repo, explicit Hermes bridge; now shipping as [Zouroboros Swarm Bridge](../usecases/zouroboros-swarm-bridge.md) |

**Net: 2 accepted (both rewritten), 4 rejected.**

## Per-entry rationale

### 1. `raspberry-pi-edge-deployment` — Reject

Source is "Community Build," which fails the evidence rule. Content-wise, the write-up is framework-agnostic — "the agent framework," "compile ARM-compatible versions," "quantized model files" — nothing Hermes-specific. Could describe any agent stack running on a Pi.

The real Hermes edge story is also already documented: the official repo supports **Android/Termux** on ARM (with a curated `.[termux]` extra that handles Android-incompatible voice deps). That's the Nous-sanctioned path for edge/mobile. A Raspberry Pi write-up grounded in actual Hermes setup — Termux, the `hermes-agent.nousresearch.com/docs/` Termux guide, a specific model and its Hermes config — could earn a spot. As submitted, it's too generic to keep.

### 2. `second-brain-does-things` — Reject

"Community Reports" fails the evidence rule. More importantly, the write-up never mentions Hermes's actual memory primitives:

- `MEMORY.md` and `USER.md` (the always-loaded layer)
- FTS5 cross-session recall
- `skill_manage` and `~/.hermes/skills/` for procedural memory
- Honcho dialectic user modeling

Instead it describes generic RAG ("vector database accumulates a continuous log"). If someone wrote this grounded in Hermes's four-layer memory system with a real daily-use report, that's a potential entry. As written, it's generic LLM-product marketing.

### 3. `sim-visual-workflow` — Reject

The HN link is a real source, but it's about Sim itself, not about Sim as a Hermes integration. The write-up describes Sim's own features (DAG builder, MCP export) without documenting how Sim connects to Hermes. The implied path — Sim exports as MCP, Hermes consumes MCP — is technically possible but not documented anywhere in the submission, and "technically possible" isn't a use case.

If the Sim project publishes an explicit Hermes integration walkthrough, or if someone writes up having used Sim to orchestrate Hermes workflows, that could be an entry. The submission as written is a Sim pitch, not a Hermes use case.

### 4. `telegram-universal-interface` — Reject

Redundant. The existing [Team Telegram Assistant](../usecases/team-telegram-assistant.md) entry already documents the Telegram pattern with a first-party docs source. The submission adds "three X handles as supporting signal," which per the evidence rule doesn't upgrade anything.

Also updated the existing entry's description in the README to note that the same gateway supports Discord, Signal, Slack, WhatsApp, Matrix, etc. — one line in the existing entry absorbs this submission's content without adding a second Telegram page.

### 5. `yantrikdb-memory-engine` — Rewrite and accept

YantrikDB is real. Confirmed primary sources:

- `github.com/yantrikos/yantrikdb` — cognitive memory engine (AGPL)
- `github.com/yantrikos/yantrikdb-mcp` — MCP server (MIT)
- `yantrikdb.com` — project site with maturity notes

The submission's claim of a `yantrikdb-hermes-plugin` is not verified — no such plugin appears in the YantrikDB repo or elsewhere. But the correct integration path is **MCP**: YantrikDB ships an MCP server, and Hermes has first-class MCP client support.

Rewrote the submission to reflect the actual integration shape (MCP, not a plugin), added appropriate caveats about when to reach for it vs. Hermes's native memory, and noted the AGPL licensing. Shipping as [`yantrikdb-memory-mcp.md`](../usecases/yantrikdb-memory-mcp.md).

### 6. `zouroboros-swarm-bridge` — Accept (with corrections)

Verified primary sources:

- `github.com/marlandoj/zouroboros` — active monorepo, explicitly names Hermes as one of four executors
- `github.com/marlandoj/zouroboros-swarm-executors` — archived but contains the bridge architecture
- The repo ships a literal `hermes-bridge.sh` alongside Claude Code, Gemini, and Codex bridges

One correction: the standalone executors repo is archived and has been migrated into the monorepo under `packages/swarm/src/executor/`. The published use case page reflects that.

Conceptually overlaps with the [Paperclip adapter](../usecases/paperclip-managed-employee.md) — both pose Hermes as an executor inside a larger system. Differences documented in the page (official/TypeScript-adapter vs. third-party/bash-bridge, and Zouroboros also bridges non-Hermes executors). Kept both entries because the orchestrator patterns differ enough to matter to a reader choosing between them.

## Patterns from this batch

Reinforces last batch's observations plus two new ones:

1. **"MCP" is the honest integration path for most third-party tools.** Submitters keep describing dedicated plugins (`yantrikdb-hermes-plugin`, the earlier `yantrikdb-hermes-plugin` fiction) when the real answer is MCP, which is what Hermes was built to consume. Future submissions that claim a "Hermes plugin" for a third-party service should be checked: does the service actually ship a plugin, or does it ship an MCP server?
2. **Framework-agnostic submissions can often be rewritten into good Hermes use cases.** The `sim-visual-workflow` and `second-brain-does-things` cases both describe real projects (Sim, generic RAG) that *could* have been Hermes integrations with different grounding. The path forward isn't to accept them as-is; it's to wait for a contributor who's actually used the thing with Hermes and can document the real integration.
