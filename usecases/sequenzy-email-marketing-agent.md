# Sequenzy Email Marketing Agent

**Class:** Ecosystem integration
**Confidence:** Medium-High
**Demo status:** Docs + runbook

## Pain Point

Founders and small SaaS teams need lifecycle email workflows, but setting up subscribers, segments, campaigns, sequences, and reporting is repetitive and easy to neglect.

## What It Does

Hermes Agent uses an installable Sequenzy skill plus the Sequenzy CLI/API to inspect account state, draft lifecycle email copy, create templates/campaigns/sequences, send tests, and report delivery stats back to the operator.

## Setup

```bash
hermes skills tap add polnikale/sequenzy-agent-skills
hermes skills install github:polnikale/sequenzy-agent-skills/skills/sequenzy-email-marketing
npm install -g @sequenzy/cli@latest
sequenzy login
sequenzy whoami
```

For scheduled reporting, create a Hermes cron that checks Sequenzy stats and delivers to Telegram, Discord, or another gateway target.

## Prompts

```text
Use Sequenzy to create a 4-email trial onboarding sequence for our SaaS. Draft the copy first, create the templates, then send a test to me before anything goes live.
```

```text
Every weekday morning, check Sequenzy campaign and sequence stats for the last 24 hours. Send me only anomalies, large changes, or anything needing action.
```

## Skills Needed

- Hermes Agent skills support
- Hermes cron or messaging gateway for scheduled reports
- Sequenzy CLI/API authentication
- `sequenzy-email-marketing` skill

## Notes

Live sends should stay operator-approved. The useful pattern is agent-assisted setup and QA first, then explicit approval before enabling or sending to real subscribers.

## Sources

- Hermes Agent skills documentation: https://hermes-agent.nousresearch.com/docs/
- Sequenzy agent skills repo: https://github.com/polnikale/sequenzy-agent-skills
- Sequenzy website: https://sequenzy.com
