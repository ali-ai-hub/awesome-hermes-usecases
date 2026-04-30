# Infrastructure: TUI Operator Console

**Class:** Community project · **Confidence:** High · **Demo status:** Verified project

## Pain Point

Managing a Hermes agent through CLI commands and config files is functional but opaque. You can't see what's running, what's scheduled, what skills are loaded, or what the agent is doing right now without bouncing between terminal windows, log files, and text editors.

## What It Does

The Hermes TUI HUD is a keyboard-first terminal operator console built with Textual. It gives a single-pane view of everything happening across your agent:

- **Live sessions** with export capability
- **Skills toggle** — enable/disable per session
- **Config YAML editing** inline
- **Cron, logs, analytics, environment variables**
- **Multiple cyber themes** (Neon, Matrix, Vaporwave)

The official Hermes TUI is part of the core distribution — start it with `hermes tui` or just `hermes`. A community extension by @ShaneRobinett extends this into a full-screen HUD.

## Setup

**Official TUI (built-in):**
```bash
hermes tui          # start the terminal UI
# or
hermes              # default entry point on some installs
```

**Community HUD (optional):**
- Project: "Hermes TUI HUD" by @ShaneRobinett
- Stays 100% native to Hermes APIs — no extra data layer
- Full-screen Textual interface with tabs

**Configuration via TUI:**
- Press `c` or navigate to Config to edit YAML
- Navigate to Skills to toggle the active set
- Navigate to Cron to view and edit scheduled tasks

## Prompts

From within the TUI, you interact normally — type commands at the chat input, use slash commands, or delegate tasks. The HUD is a view layer; the agent underneath is the same.

**Common commands inside TUI:**
```
/help           # list available slash commands
/status         # show current agent state
/cron list      # show scheduled jobs
```

**From outside TUI (systemd-managed agent):**
```
hermes gateway status    # check if gateway is running
hermes logs              # tail the agent log
```

## Skills Needed

- Hermes TUI (ships with core)
- Optional: Textual for custom theme development

## Notes

- The TUI is mouse-friendly but designed for keyboard-first operation. Arrow keys, tab, and Enter navigate all views.
- The React Ink-based docs description on DeepWiki refers to an earlier or alternate TUI implementation; the current core TUI uses Textual.
- For remote management, the TUI runs over SSH without issues — the display is terminal-native.
- @ShaneRobinett's HUD adds visual chrome but depends on the same API surface; it's a skin, not a fork.

## Sources

- Official docs — TUI: https://hermes-agent.nousresearch.com/docs/user-guide/tui/
- GitHub README (terminal modes): https://github.com/NousResearch/hermes-agent
- DeepWiki TUI docs: https://deepwiki.com/nousresearch/hermes-agent/3.3-tui-(terminal-user-interface)
- @ShaneRobinett on X: https://x.com/ShaneRobinett/status/2047895502159479188
