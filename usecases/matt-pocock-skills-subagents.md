# Matt Pocock Skills + Hermes Sub-Agents for Feature Work

| **Aspect** | **Detail** |
|---|---|
| **Category** | Software Development |
| **Complexity** | Advanced |
| **Hermes Features Used** | `skills`, `delegate_task`, `hermes config set`, file-writer skill |
| **Primary Sources** | Reddit post by Hermes user (setup/guide), linked repos, star counts verified live |

---

## Overview

Matt Pocock's public skill repo handles planning and issue breakdown. Hermes's builtin sub-agents handle implementation. Together they give you a planning layer that prevents "AI slop" and an execution layer that parallelizes across vertical slices.

Pocock's repo had **45.6k GitHub stars** at verification time (up from 42.5k when the Reddit post was written).

- **Skills repo:** [github.com/mattpocock/skills](https://github.com/mattpocock/skills)
- **Claude Code runner (not used here):** [github.com/mattpocock/sandcastle](https://github.com/mattpocock/sandcastle)

Since Hermes already has built-in sub-agents, the Hermes user skips Sandcastle and runs implementation natively.

**Use case:** an existing project, one big feature or refactor, multiple surfaces. Backend, frontend, docs, landing page, tests, etc. Not a whole project from scratch.

---

## Who's Doing This

A Hermes user running a mature codebase who wants to land a cross-cutting feature without giving a single agent a vague giant task. They know Matt Pocock's skills from the TypeScript community and want the same rigor for AI-assisted development.

---

## How It Works

### Step 1: Ask Hermes for a Local Markdown Plan

Scope, risks, surfaces touched, rough outline. No code yet.

```
Hermes, write a plan for ~/projectA/big-feature-x.md covering scope,
riskiest assumptions, surfaces touched, and a rough task outline.
Save as local markdown, do NOT create a GitHub issue.
```

### Step 2: Run Matt's `grill-me` or `grill-with-docs` Skill on the Plan

Answer the hard questions. If the agent drifts into implementation, tell it to refocus on the feature plan. Let it update the markdown.

```
/grill-with-docs on ~/projectA/big-feature-x.md
```

This skill also updates `CONTEXT.md` and ADRs inline, building a shared domain language that makes later sub-agent instructions shorter and more precise.

### Step 3: Run Matt's `to-prd` Skill

```
/to-prd on ~/projectA/big-feature-x.md, create local md PRD not in github
```

### Step 4: Run Matt's `to-issues` Skill

```
/to-issues on ~/projectA/big-feature-x-prd.md, create local md issues not in github
```

### Step 5: Check the Issue Split Before Running Agents

It should be **vertical**, not horizontal.

**Bad split (horizontal):**
- backend
- frontend
- docs
- tests

**Better split (vertical):**
- small backend path + one frontend entry point
- user-facing flow + error state
- docs/landing update for the behavior
- verification/tests/cleanup

Ask Hermes to apply more verticalization; it will know what you mean.

### Step 6: One Sub-Agent Per Issue, Halt on HITL

```
Implement the feature split slices in ~/projectA/big-feature-x-issues.md,
use sub-agents for every issue, and parallelize when possible but carefully.
Halt on tasks that are HITL or otherwise require human input.
```

Still needs human judgment. The user reads the plan, rejects bad issue splits, and stops AI slop before it turns into code.

---

## Configuration Tweaks (Required)

Out-of-the-box Hermes can hit iteration exhaustion on deep sub-agent chains. Bump before starting:

```bash
hermes config set delegation.max_iterations 100
hermes config set delegation.child_timeout_seconds 1200
```

Then restart the Hermes session.

---

## Real-World Constraints

- **Not for greenfield projects.** The workflow assumes an existing codebase with tests, types, and documented patterns.
- **Requires domain context.** `grill-with-docs` builds `CONTEXT.md` over time. First run is slower; subsequent runs in the same repo are faster.
- **Human gatekeeper.** The user explicitly intervenes at the plan-to-code boundary. This is not fully autonomous.
- **Skill compatibility.** Pocock's skills use Claude Code slash-command conventions. Hermes parses them as skill invocations. The user is effectively running Pocock's prompts inside Hermes's tool-calling system.

---

## Primary Sources

- **[mattpocock/skills](https://github.com/mattpocock/skills)** — 45.6k stars, MIT license. Skills used: `grill-me`, `grill-with-docs`, `to-prd`, `to-issues`
- **[mattpocock/sandcastle](https://github.com/mattpocock/sandcastle)** — Pocock's Claude Code runner. Not used here; Hermes sub-agents replace it
- **Reddit post by Hermes user** (setup/guide category) describing the combo workflow, April 2026, including delegation-limit tweaks and the HITL stop gate

---

## Related Use Cases

- [Self-Evolution](self-evolution.md) — Hermes optimizing its own skills, also uses PRD + iteration pattern
- [Zouroboros Swarm Bridge](zouroboros-swarm-bridge.md) — Multi-agent execution with external orchestrators
- [Paperclip Managed Employee](paperclip-managed-employee.md) — Hermes inside a task-orchestration system with persistent sessions

---

## Why It Works

Pocock's skills solve planning and scoping — the most common failure mode of coding agents. Hermes sub-agents solve execution — the most common failure mode of Pocock's Sandcastle (which is Claude-specific).

Combining the two means you get Matt's rigor on the front end and Hermes's flexible tool-calling on the back end, with a human gate at the plan-to-code boundary.
