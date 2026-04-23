# YantrikDB Cognitive Memory (via MCP)

**Class:** Ecosystem integration · **Confidence:** Medium-High · **Demo status:** MCP server + install guide

## Pain Point

Hermes's native memory is excellent at what it does — four-layer design with `MEMORY.md`, `USER.md`, session history, and skills. But some workflows need more than that: automatic contradiction detection, temporal decay (memories that fade if they're not reinforced), and cognitive consolidation across thousands of entries. File-based memory also has a token-cost ceiling — at 500+ entries it starts to crowd the context window; at 5,000+ it won't fit even in 200K-context models.

## What It Does

[YantrikDB](https://yantrikdb.com/) is a cognitive memory engine designed specifically for this: vector + knowledge-graph + temporal + decay, all in one embedded database. It ships as an MCP server (`yantrikdb-mcp`), which Hermes can consume via its built-in MCP client support. The integration path isn't a dedicated Hermes plugin — it's standard MCP, which is what makes it work at all.

Once connected, the agent gets four tool-call-shaped memory operations:

- `record()` — store a fact with importance, domain, and optional temporal half-life
- `recall()` — semantic retrieval ranked by relevance, recency, importance, and graph proximity
- `relate()` — build knowledge-graph edges between entities
- `think()` — trigger consolidation, contradiction detection, and pattern mining

Memory lives in a local SQLite file (default `~/.yantrikdb/memory.db`); nothing leaves your machine in stdio mode.

## Setup

### Stdio mode (single machine, simplest)

```bash
pip install yantrikdb-mcp
```

Add to Hermes's MCP server config (typically `config.yaml` under `mcp_servers:`):

```yaml
mcp_servers:
  yantrikdb:
    command: yantrikdb-mcp
    # Optional: override default DB location
    env:
      YANTRIKDB_DB_PATH: /home/you/.hermes/yantrikdb.db
```

Restart Hermes. The YantrikDB tools now appear under `hermes tools`.

### SSE mode (shared across machines)

For a multi-machine setup — e.g., Hermes on a VPS talking to YantrikDB on a homelab box:

```bash
export YANTRIKDB_API_KEY=$(python -c "import secrets; print(secrets.token_urlsafe(32))")
yantrikdb-mcp --transport sse --port 8420
```

Then in Hermes's MCP config:

```yaml
mcp_servers:
  yantrikdb:
    type: sse
    url: http://your-homelab:8420/sse
    headers:
      Authorization: Bearer YOUR_API_KEY
```

## When to Use YantrikDB vs. Native Memory

Use Hermes's native memory (`MEMORY.md`, `USER.md`, skills) as the default. It's the right tool for identity, user preferences, and procedural knowledge that the agent actively curates.

Reach for YantrikDB when:

- You're storing **thousands of facts**, not hundreds, and context-window cost matters.
- You want **automatic contradiction detection** — "Alice moved to Berlin" vs. an older "Alice lives in London."
- **Temporal decay** matters — stale memories should fade unless explicitly reinforced.
- Multiple agents, devices, or sessions need to **share a common memory** (SSE mode).

For a single-user laptop setup, native memory is simpler and sufficient.

## Reported Scale

Per the YantrikDB project:

- File-based memory exceeds 32K context at ~500 memories and won't fit in 200K at ~5,000.
- YantrikDB queries use **~70 tokens per query** regardless of database size — precision improves as data grows.
- The embeddable engine is reported in production use by the YantrikOS ecosystem; the network server runs on a multi-tenant Proxmox cluster per the project's maturity notes.

## Skills Needed

- MCP server support in Hermes (built in)
- Python runtime for `yantrikdb-mcp`
- Optional: a homelab or VPS for SSE mode

## Licensing

YantrikDB engine is **AGPL-3.0**. The MCP server wrapper is MIT. Using the engine as-is via the MCP server does not trigger AGPL obligations on your code — but modifying the engine and redistributing it does. If you're building a commercial product, read the license before forking.

## Notes

- **Not an official Nous integration.** YantrikDB is a third-party project that happens to work with Hermes because both speak MCP. If the Hermes MCP client or the YantrikDB server changes shape, the bridge needs to hold on both sides.
- **Treat it as an add-on, not a replacement.** Hermes's native memory handles identity and style; YantrikDB is best as a searchable long-term fact store the agent can query on demand.
- For a lighter alternative, Hermes's built-in `skill_manage` and session search (FTS5-backed) cover most "remember this across sessions" needs without adding a service.

## Sources

- YantrikDB engine: <https://github.com/yantrikos/yantrikdb>
- YantrikDB MCP server: <https://github.com/yantrikos/yantrikdb-mcp>
- Project site: <https://yantrikdb.com/>
- Hermes MCP support: <https://hermes-agent.nousresearch.com/docs/>
