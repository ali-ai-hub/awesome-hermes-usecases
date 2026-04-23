# Open WebUI Frontend

**Class:** Official integration · **Confidence:** High · **Demo status:** [Runnable](../demos/openwebui/)

## Pain Point

The Hermes CLI is powerful but not shareable — you can't hand it to a non-terminal teammate, and it's awkward to use from a tablet or phone browser. You want a proper chat UI for Hermes that supports streaming, file uploads, conversation history, and works in any browser.

## What It Does

Hermes exposes an OpenAI-compatible API server. Open WebUI is a mature self-hosted chat frontend that talks to any OpenAI-compatible endpoint. Point Open WebUI at Hermes and you get a polished browser UI on top of your full agent — sessions, tools, skills, memory — with streaming replies and file upload.

Both projects document this integration on their respective sides.

## Setup

1. Enable the API server in Hermes:
   ```bash
   hermes config set api_server.enabled true
   hermes config set api_server.key "$(openssl rand -hex 32)"   # save this
   hermes gateway install
   ```
   The API server listens on port 8642 by default.

2. Run Open WebUI via Docker, pointed at Hermes:
   ```yaml
   # docker-compose.yml
   services:
     open-webui:
       image: ghcr.io/open-webui/open-webui:main
       ports: ["3000:8080"]
       environment:
         OPENAI_API_BASE_URL: http://host.docker.internal:8642/v1
         OPENAI_API_KEY: YOUR_API_SERVER_KEY
       extra_hosts:
         - "host.docker.internal:host-gateway"
   ```
   ```bash
   docker compose up -d
   ```

3. Open `http://localhost:3000`, finish the first-run admin setup, and start chatting. Conversations persist because Hermes keeps session state — closing the browser doesn't reset context.

## Prompts

Once connected, every Hermes capability is available through the chat box — terminal, file, web, delegation, cron. Nothing special about the prompts.

## Skills Needed

- Hermes API server enabled (`API_SERVER_ENABLED=true`, `API_SERVER_KEY=...`)
- Open WebUI (self-hosted via Docker)

## Notes

- Use a long random `API_SERVER_KEY`. If you expose the port beyond localhost, put TLS in front.
- For multi-user access, Open WebUI handles user accounts on its side; Hermes still sees one API client. Per-user sessions on the Hermes side require a different setup (messaging gateways do this better).

## Sources

- Hermes docs: <https://hermes-agent.nousresearch.com/docs/user-guide/messaging/open-webui/>
- Open WebUI docs: <https://docs.openwebui.com/getting-started/quick-start/connect-an-agent/hermes-agent/>
