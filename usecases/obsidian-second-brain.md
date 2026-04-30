# Memory: Obsidian Vault as a Second Brain

**Class:** Community pattern · **Confidence:** Medium-High · **Demo status:** Verified integrations

## Pain Point

AI agents are great at answering questions, but most forget everything when the session ends. Building persistent knowledge — research notes, project history, personal journal — requires a structured store that the agent can read from and write to, not just a chat log.

## What It Does

Multiple community members have wired Hermes into Obsidian vaults as a persistent knowledge base. The agent can:
- Read existing notes to answer questions with your own prior research
- Create new notes, daily dashboards, and task lists
- Cross-reference tags and links across the vault
- Maintain a "daily review" or "morning briefing" note generated automatically

One documented setup uses Zotero → Obsidian (PC) → Syncthing → Obsidian (RPi5) → Hermes, where the agent only reads from the synced vault on the Pi, keeping the knowledge loop air-gapped from the source.

## Setup

1. Point Hermes at your Obsidian vault directory using the `obsidian` skill or direct file tools.
2. Ensure the vault is reachable from Hermes's environment (local file system, synced folder, or mounted path).
3. Grant read and write permissions as appropriate.

**Typical config:**
```yaml
# In Hermes config or .env
OBSIDIAN_VAULT_PATH=/path/to/your/vault
```

**Common cron patterns:**
```
/cron add "0 7 * * *" "Read yesterday's journal, today's calendar, and open tasks, then write a morning briefing to vault/00-Daily/Today.md"
```

## Prompts

**Daily review:**
```
Read my vault, identify what I worked on yesterday, what meetings I have today, and write a morning briefing in vault/00-Daily/Today.md.
```

**Research capture:**
```
I just finished reading this paper: [paste abstract]. Save a summary to vault/10-Research/ with key findings, open questions, and tags matching my existing taxonomy.
```

**Knowledge retrieval:**
```
What do my notes say about MLX quantization? Cite the specific notes.
```

## Skills Needed

- obsidian skill (read/search/create notes in vault)
- File tools
- Optional: Zotero or reference manager for literature intake
- Optional: cron for daily automation

## Notes

- The quality of this setup depends entirely on vault structure. A flat pile of notes is no better than chat history. Invest time in a consistent folder and tag structure.
- Syncing via Syncthing, Dropbox, or iCloud keeps the vault accessible across devices but introduces file-lock edge cases if Hermes and Obsidian desktop write simultaneously.
- The OMI + Obsidian + Hermes combo (voice capture → transcription → note creation) is an emerging pattern for frictionless knowledge capture.

## Sources

- GitHub: https://github.com/omankz/Hermes-Agent---Claude-Cowork---Notion---Obsidian
- YouTube: "Hermes Agent + Obsidian: The Self-Improving Second Brain" — https://www.youtube.com/watch?v=L0hs3-xBjJE
- Podcast: "Hermes Agent clearly explained" (Apple) covers Obsidian integration
- Blog: pandaitech.my — "Setting Up an Automated Daily Dashboard with Hermes Agent and Obsidian"
