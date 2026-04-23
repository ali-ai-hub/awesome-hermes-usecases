# Open WebUI Demo

A runnable version of the [Open WebUI Frontend](../../usecases/open-webui-frontend.md) use case. Stands up Open WebUI in Docker, pointed at the Hermes API server.

## What you'll end up with

Open WebUI running at `http://localhost:3000`, talking to your local Hermes instance over the OpenAI-compatible API. Full agent capability (terminal, file, web, delegation) available through a browser chat UI with streaming and file upload.

## Prerequisites

- Hermes Agent installed and a model configured.
- Docker and Docker Compose installed.

## Setup

1. Copy `.env.example` to `.env` and set an API key:
   ```bash
   cp .env.example .env
   # edit .env — set HERMES_API_KEY to something long and random
   # e.g.: openssl rand -hex 32
   ```

2. Enable the Hermes API server with the same key:
   ```bash
   source .env
   hermes config set api_server.enabled true
   hermes config set api_server.key "$HERMES_API_KEY"
   hermes gateway install    # starts the API server on port 8642
   ```

3. Start Open WebUI:
   ```bash
   docker compose up -d
   ```

4. Open `http://localhost:3000`, finish the first-run admin setup (local account, stays on your machine), and send a message. It routes through Hermes.

## Verifying

Quick sanity check the Hermes API server is up before pointing Open WebUI at it:

```bash
curl -s http://localhost:8642/v1/models \
  -H "Authorization: Bearer $HERMES_API_KEY" | head
```

Expect a JSON response listing models. If you get a connection error, the gateway isn't running. If you get 401, the key in `.env` and the key set via `hermes config` don't match.

## Shutting down

```bash
docker compose down
```

The Hermes API server stays up — that's a separate process. Stop it with `hermes gateway stop` if you want to.

## Sources

- Hermes docs: <https://hermes-agent.nousresearch.com/docs/user-guide/messaging/open-webui/>
- Open WebUI docs: <https://docs.openwebui.com/getting-started/quick-start/connect-an-agent/hermes-agent/>
