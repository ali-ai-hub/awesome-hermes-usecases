# Zouroboros Swarm Executor Bridge

**Class:** Ecosystem integration · **Confidence:** Medium-High · **Demo status:** Bridge repo (archived — migrated to monorepo)

## Pain Point

You want a multi-agent orchestrator — one that routes different kinds of work to different coding agents (Claude Code for one task, Codex for another, Hermes for a third) — without tying yourself to any single CLI's ergonomics or pricing. The orchestrator decides; the executors do the work. The tricky part is the wire between them: how does the orchestrator actually *call* Hermes in a way it can call Claude Code and Codex the same way?

## What It Does

[Zouroboros](https://github.com/marlandoj/zouroboros) is a self-enhancing AI platform built on Zo Computer with a swarm-orchestration layer that routes tasks across four executor types: **Claude Code, Gemini CLI, Codex, and Hermes**. Each executor gets a bridge script — `hermes-bridge.sh` in Hermes's case — with a shared I/O contract:

```
Input:   bash hermes-bridge.sh "prompt" [workdir]
Output:  plain text on stdout
Errors:  stderr + non-zero exit code
```

The orchestrator picks an executor based on an 8-signal composite (capability, health, complexity, history, procedure, temporal, budget, role) and calls its bridge. The bridge runs Hermes on the local machine, collects the output, and returns it. All executors share the same `SOUL.md`, identity files, and memory system, so context moves with the task even when the executor changes.

It's a **headless adapter pattern** — Hermes becomes one of several interchangeable tool-execution backends rather than the primary interface. Similar in spirit to the [Paperclip adapter](paperclip-managed-employee.md), but lighter and language-agnostic.

## Setup

> ⚠️ **Note on repo state.** The original standalone `marlandoj/zouroboros-swarm-executors` repo is archived. The code has been migrated to the Zouroboros monorepo under `packages/swarm/src/executor/`. Use the monorepo for new installs.

1. Install Zouroboros:
   ```bash
   git clone https://github.com/marlandoj/zouroboros.git
   cd zouroboros
   pnpm install
   pnpm run build
   zouroboros init
   zouroboros doctor    # checks executor availability
   ```

2. Ensure Hermes is installed and on your `PATH`. The bridge shells out to `hermes` directly; no extra config on the Hermes side is required for basic use.

3. Test the Hermes bridge in isolation:
   ```bash
   bash packages/swarm/src/executor/bridges/hermes-bridge.sh \
     "write a hello world in python" \
     /tmp/hermes-test
   ```

4. Register Hermes with the orchestrator via its executor registry. The orchestrator reads `registry/executor-registry.json` (or the monorepo equivalent) to know which executors are available and their capabilities.

## Key Integration Details

- **Model routing.** When called via the orchestrator, the bridge receives a `SWARM_RESOLVED_MODEL` env var that tells Hermes which model to use. The orchestrator picks this based on the task's complexity tier — cheap models for trivial tasks, powerful ones for hard ones. Lets you keep your Hermes config in one place while the orchestrator handles cost routing.
- **Standalone fallback.** Call the bridge directly (outside the orchestrator) and it falls back to Hermes's normal model selection. Useful for debugging and one-off tasks.
- **Shared memory.** All executors read the same `SOUL.md` and identity files — Hermes picks up the same context whether invoked directly or via Zouroboros.

## When to Use This

This isn't a use case for someone who's happy with Hermes as their primary agent. It's for people who want:

- A **higher-level orchestrator** making routing decisions across multiple coding CLIs.
- **Cost-sensitive routing** — trivial work on cheap local models, hard work on Claude Opus or equivalent.
- **Cascade failover** — executor A fails, the swarm reroutes to B automatically.

If you're running a single-agent workflow, use Hermes directly and skip this layer.

## Skills Needed

- Hermes installed and working (prerequisite)
- Node.js / pnpm for Zouroboros
- Bun (for the optional skill-mode install path)
- Basic comfort with bash scripts and env-var conventions

## Notes

- **Third-party ecosystem project.** Not Nous Research, not Fly, not Anthropic. Evaluate the orchestrator code before running it against real workloads.
- **Overlaps conceptually with Paperclip.** Both pose Hermes as an employee/executor inside a larger system. The differences: Paperclip is Nous-built and TypeScript-adapter-based; Zouroboros is third-party, bash-bridge-based, and spans non-Hermes executors too. Pick based on which orchestrator matches your workflow, not which is "better."
- **Executor bridges repo is archived.** Don't start from the archived standalone repo — the active code path is in the Zouroboros monorepo.

## Sources

- Zouroboros monorepo: <https://github.com/marlandoj/zouroboros>
- Swarm executors repo (archived, reference only): <https://github.com/marlandoj/zouroboros-swarm-executors>
