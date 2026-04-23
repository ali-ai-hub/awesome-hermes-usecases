# Enterprise Messaging (Feishu / WeCom)

**Class:** Independent deployment · **Confidence:** High · **Demo status:** Case study

## Pain Point

Most Hermes messaging tutorials target Telegram, Discord, or Slack — fine for Western teams, but the enterprise messaging surface in China runs on Feishu (Lark) and WeCom (WeChat Work). Teams in those environments need a Hermes gateway that speaks the right protocols, handles media analysis natively, and can run as a supervised service without babysitting.

## What It Does

Hermes's gateway supports Feishu, WeCom, DingTalk, and Weixin as first-class platforms (per the official docs). Multiple first-person GitHub issues document production-style deployments:

- **Feishu on macOS, supervised by `launchd`.** User `runwithcc` ([issue #10541](https://github.com/NousResearch/hermes-agent/issues/10541)) runs Hermes as a live Feishu transport backbone with dedicated service user, webhook ports, and `launchd`-managed restarts. The issue is a bug report about Hermes modifying its own runtime config during a live conversation, which happens to reveal exactly how the deployment is wired.
- **WeCom media extraction and vision analysis.** User `mc436572` ([PR for WeCom media fixes](https://github.com/NousResearch/hermes-agent/pulls?q=is%3Apr+author%3Amc436572)) documents WeCom usage where image-analysis flows depend on media extraction from the WeCom transport layer — a concrete enterprise media workflow, not just text chat.

Both cases show Hermes functioning as an enterprise-grade chat bot rather than a personal assistant.

## Setup

The gateway docs cover platform-specific credential setup. The common pattern:

1. Register an internal app on Feishu or WeCom's developer console. Both platforms require an admin with rights to install apps into the organization.
2. Collect the app's credentials (App ID, App Secret, verification token for webhooks).
3. Configure the corresponding platform in `config.yaml` or via `hermes config set`. Each platform has its own config section under `platforms:`.
4. Expose the webhook endpoint with TLS (both platforms reject unsigned HTTP). A reverse proxy in front of the Hermes gateway is the usual path.
5. Supervise the gateway. Production deployments typically wrap it in `systemd` on Linux or `launchd` on macOS — the Feishu issue above shows the latter.

## Running as a Supervised Service

On Linux, `hermes gateway install --system` sets up a boot-time systemd unit. On macOS, a `launchd` plist is more common; the gateway issue thread referenced above includes a working pattern for a dedicated service user and restart policy.

Gotcha from that issue: **don't ask the agent to edit its own live gateway config mid-conversation.** That path can spawn duplicate gateways and port conflicts. Config changes should go through a restart, not a live self-edit.

## Skills Needed

- Feishu or WeCom platform configured in `config.yaml`
- Organization admin rights to register the app
- A public HTTPS endpoint for webhooks
- Process supervisor (`systemd`, `launchd`, or equivalent)
- For WeCom media workflows: the vision toolset enabled

## Notes

- Both platforms have their own rate limits and media-size caps — test attachments before promising image-analysis features to users.
- Enterprise admins often require audit trails. Hermes's JSONL transcripts and SQLite session store give you a raw record; you'll likely need to add a retention policy on top.
- The WeCom PR fixed a specific breakage where media extraction failures cascaded into the vision pipeline. If you deploy on WeCom, pin to a post-fix Hermes version.

## Sources

- Feishu deployment issue (`runwithcc`): <https://github.com/NousResearch/hermes-agent/issues/10541>
- Official messaging docs (platforms list): <https://hermes-agent.nousresearch.com/docs/user-guide/messaging/>
- WeCom-related fixes: tracked in the Hermes repo's PR history
