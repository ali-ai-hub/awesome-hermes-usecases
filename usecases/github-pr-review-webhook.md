# GitHub PR Review (webhook)

**Class:** First-party demo · **Confidence:** High · **Demo status:** Docs + runbook

## Pain Point

Cron-based review is fine for nightly digests, but you want review comments on a PR within seconds of it being opened — not 30 minutes later. You also want the agent to respond to re-requests (new commits on an existing PR) without re-reviewing unchanged files.

## What It Does

GitHub fires a webhook on `pull_request` events. Hermes's gateway exposes a signed route that validates the payload, routes it to the agent, and triggers a review workflow. The agent pulls the diff with `gh pr diff`, reviews against your skill, and posts comments back on the PR. Turnaround is seconds-to-tens-of-seconds depending on diff size and model.

## Setup

1. Add a webhook route in Hermes's `config.yaml` under `platforms.webhook.extra.routes`:
   ```yaml
   platforms:
     webhook:
       extra:
         routes:
           github-pr-review:
             secret: ${GITHUB_WEBHOOK_SECRET}
             prompt: |
               A PR event fired. Validate the payload, extract the PR
               number and repo, run gh pr diff, review against the
               pr-review skill, and post a review comment. If the
               event is a synchronize, only re-review the newly
               changed files.
             skills: [pr-review]
   ```
2. Expose the gateway publicly. Options:
   - A reverse proxy on your VPS (Caddy or nginx) with TLS in front of the gateway port.
   - A tunnel service for testing (Tailscale Funnel, Cloudflare Tunnel).
3. In your GitHub repo settings → Webhooks:
   - Payload URL: `https://your-host/webhook/github-pr-review`
   - Content type: `application/json`
   - Secret: the value you put in `GITHUB_WEBHOOK_SECRET`
   - Events: select `Pull requests` (and `Pull request reviews` if you want reply-to-reply).

## Prompts

Test the route with a signed `curl` before connecting GitHub:

```bash
BODY='{"action":"opened","pull_request":{"number":1},"repository":{"full_name":"YOUR_ORG/YOUR_REPO"}}'
SIG=$(echo -n "$BODY" | openssl dgst -sha256 -hmac "$GITHUB_WEBHOOK_SECRET" | awk '{print "sha256="$2}')

curl -X POST https://your-host/webhook/github-pr-review \
  -H "Content-Type: application/json" \
  -H "X-Hub-Signature-256: $SIG" \
  -d "$BODY"
```

## Skills Needed

- Terminal tool (for `gh`)
- Custom review skill
- Webhook route in `config.yaml`
- Public endpoint with TLS

## Security Notes

- **Always verify the signature.** The `secret` field in the route config must match GitHub's webhook secret, and the gateway validates `X-Hub-Signature-256` before dispatching.
- Limit the route to the specific repo events you care about — an unsigned or wrong-repo payload should be rejected early.
- The agent still runs with full skill permissions. Don't wire a webhook route to a skill that can push code or close issues unless that's exactly what you want.

## Sources

- Official tutorial: <https://hermes-agent.nousresearch.com/docs/guides/webhook-github-pr-review>
- Gateway / webhook docs: <https://hermes-agent.nousresearch.com/docs/user-guide/messaging/>
