# Contributing

Thanks for thinking about contributing. This repo has one rule that keeps it useful: **every use case is backed by a primary public source.** If that rule holds, the rest is easy.

## Adding a Use Case

1. Create a markdown file in `/usecases` named after your use case (e.g. `slack-standup-bot.md`).
2. Fill in the sections below (template at the bottom of this file). The essentials:
   - **Pain Point** — what problem this actually solves
   - **What It Does** — brief description of the workflow
   - **Setup** — commands and config someone else can follow
   - **Prompts** — the actual prompts or cron expressions
   - **Skills Needed** — tools, gateways, plugins required
   - **Sources** — at least one primary source link
3. Add a row in the right category table in [README.md](README.md). Suggest a new category in your PR if nothing fits.
4. Open a PR.

## Evidence Rule (the important one)

A use case qualifies as "verified" only if it has **at least one primary source** — one of:

- Official Hermes docs, repo, or release notes.
- An official Nous Research companion repo or blog post.
- A GitHub issue or PR with concrete deployment details (not just a feature request).
- A first-person third-party blog post or repo that explicitly shows Hermes in the architecture.

The following don't count as primary evidence on their own:

- X / Twitter posts (useful as leads, not as proof).
- "Community Build" or marketing pages on non-Hermes product sites.
- Your own private setup with no public write-up.

If your use case only has social or private evidence, it still has a home — [`research/unverified.md`](research/unverified.md). We promote entries from there to the main catalog once stronger sources emerge.

## Guidelines

- **One use case per markdown file.** Don't stuff several into one page.
- **Confidence and class, honestly stated.** If it's an official demo, say so. If it's a community extension, say so. Inflation hurts the catalog.
- **Keep setup reproducible.** Real commands, real config. If part of it is private (API keys, internal stacks), say what's private and what a reader can substitute.
- **Prompts should be the ones you actually used.** Cleaned up for clarity is fine; invented is not.
- **No duplicates of the same approach.** Variations are welcome if they meaningfully differ.
- **Don't use AI to invent new use cases.** Submit things you've run, or that you can trace to a real primary source.
- **No crypto use cases.** These will not be accepted.
- **No social engineering or stalker workflows.** Not accepted.

## Per-Use-Case Template

```markdown
# <Title>

**Class:** First-party demo | Official integration | Official production | Official companion | Independent deployment | Ecosystem integration
**Confidence:** High | Medium-High | Medium | Low
**Demo status:** Runnable | Docs + runbook | Case study

## Pain Point

What problem is this solving, in plain language.

## What It Does

Short description of the workflow — ingress → core → tools → delivery.

## Setup

Real commands. Copy-pasteable.

## Prompts

The actual prompts / cron expressions / config snippets you used.

## Skills Needed

- Tool / gateway / plugin
- Etc.

## Notes

Anything non-obvious — gotchas, trade-offs, security.

## Sources

- Primary source link(s) — official docs, companion repo, GitHub issue, or first-person blog.
```

## Getting Help

Open an issue tagged `question` if you're unsure whether something qualifies. Easier to ask first than to have a PR sit.
