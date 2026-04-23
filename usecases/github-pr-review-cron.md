# GitHub PR Review (cron)

**Class:** First-party demo · **Confidence:** High · **Demo status:** Docs + runbook

## Pain Point

You want automated PR review on a repo, but you don't want to open a public webhook endpoint, install a bot app, or manage yet another SaaS. You just want something that checks your repo on a schedule and leaves real review comments.

## What It Does

A cron job runs every N minutes (or nightly). The agent uses the authenticated `gh` CLI to list open PRs, pulls diffs for anything new, applies a review skill that understands your repo's style and constraints, and posts review comments back on the PR. Delivery can also go to Telegram or Discord as a digest.

No webhook, no public endpoint, no inbound network exposure at all.

## Setup

1. Authenticate `gh` on the Hermes host:
   ```bash
   gh auth login                    # needs repo scope
   gh auth status                   # verify
   ```
2. Create a review skill that encodes your standards. Drop it in `~/.hermes/skills/pr-review/`:
   ```
   ~/.hermes/skills/pr-review/
     SKILL.md          # review criteria, style rules, what to flag
   ```
3. Start the gateway so cron runs unattended:
   ```bash
   hermes gateway install
   ```
4. Create the cron job:
   ```bash
   hermes cron create "*/30 * * * *" \
     "Review open PRs on YOUR_ORG/YOUR_REPO opened or updated in the last
      30 minutes. For each one: gh pr diff <num>, evaluate against the
      pr-review skill, then post a review comment with gh pr review.
      If nothing new, respond [SILENT]." \
     --skills pr-review \
     --name "PR review (cron)" \
     --deliver local
   ```

Swap `--deliver local` for `--deliver telegram` or `--deliver discord` to also get a digest.

## Prompts

A lighter daily variant that only summarizes instead of auto-commenting:

```
hermes cron create "0 9 * * *" \
  "Daily PR digest for YOUR_ORG/YOUR_REPO. List PRs opened yesterday,
   their titles, authors, and a one-line assessment (ready to merge /
   needs changes / wip). Post to home channel." \
  --name "Daily PR digest" \
  --deliver telegram
```

## Skills Needed

- Terminal tool (for `gh`)
- Custom review skill (quality depends on this)
- Messaging gateway (for digest delivery)
- Cron

## Notes

- Frequency trade-off: every 30 minutes means faster feedback but more repeated diff-reads. Nightly is cheapest.
- Cron sessions are fresh — the agent has no memory of previous reviews. If you want continuity (e.g., "I already commented on this line"), encode that in the review skill as a rule to check existing comments first.

## Sources

- Official tutorial: <https://hermes-agent.nousresearch.com/docs/guides/github-pr-review-agent>
- Cron reference: <https://hermes-agent.nousresearch.com/docs/guides/automate-with-cron>
- Automation templates: <https://hermes-agent.nousresearch.com/docs/guides/automation-templates>
