# Paperclip Managed Employee

**Class:** Official companion · **Confidence:** High · **Demo status:** Companion repo

## Pain Point

A raw agent in a chat box is fine for interactive work, but it doesn't fit how you'd use agents at company scale — as a fleet of workers assigned tasks by a coordinator, with task histories, heartbeats, and swappable tool configurations. You want Hermes acting like an employee inside a task-orchestration system, not a chatbot.

## What It Does

Paperclip is Nous Research's task-orchestration system — think of it as the manager layer that dispatches work to AI workers. The `hermes-paperclip-adapter` lets Hermes *be* a worker inside Paperclip. Tasks come in as Paperclip assignments with heartbeats; the adapter invokes Hermes to execute them with the configured toolset; sessions persist across checkpoints so long-running jobs can resume; results flow back to Paperclip.

You can mix providers (Nous Portal, OpenRouter, OpenAI, local) and toolsets per agent, so the same Paperclip instance can have a coding-specialist Hermes and a research-specialist Hermes operating side by side.

## Setup

1. Install the adapter:
   ```bash
   npm install -g hermes-paperclip-adapter
   ```
2. Create a Hermes agent config for Paperclip to spawn. Example `hermes_local.json`:
   ```json
   {
     "name": "hermes_local",
     "provider": "openrouter",
     "model": "anthropic/claude-3.7-sonnet",
     "persistSession": true,
     "tools": ["terminal", "file", "web_search", "delegate"]
   }
   ```
3. Register the agent in your Paperclip instance (Paperclip's own docs cover the registration step).
4. Assign a Paperclip task — the adapter starts a Hermes session, runs the task with checkpointing, and returns results on completion.

## Prompts

Prompts are task content from Paperclip, not interactive chat. A typical task assignment might be:

```
Audit this directory for unused dependencies. Produce a report listing
each unused package, where it was expected, and a suggested removal
command. Commit nothing.
```

The adapter passes that into Hermes with the configured toolset and streams progress back to Paperclip.

## Skills Needed

- `hermes-paperclip-adapter` (npm)
- A running Paperclip instance
- A model provider (Nous Portal, OpenRouter, OpenAI, or local)
- Persistent session enabled (`persistSession: true`) for multi-step tasks

## Notes

- The adapter supports multiple providers and swappable skills per agent — use this to specialize workers instead of giving one Hermes every tool.
- Checkpointing means a crashed worker can resume; for long-running jobs this is the difference between wasted hours and a simple restart.

## Sources

- Companion repo: <https://github.com/NousResearch/hermes-paperclip-adapter>
