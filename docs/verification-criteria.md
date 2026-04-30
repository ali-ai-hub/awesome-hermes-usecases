# Verification Criteria for Usecase Contributors

This document defines what "verified" means in `awesome-hermes-usecases` and how the automated pipeline evaluates it.

---

## Primary Source Requirements

A primary source is **live evidence that the usecase actually happened** — not a tweet about it, not a blog post summarizing it, but the artifact itself.

| Tier | Source Type | Example |
|------|-------------|---------|
| Gold | GitHub repo with live star count, commit history, open issues | `github.com/mattpocock/skills` |
| Silver | Official docs page under project domain | `hermes-agent.nousresearch.com/docs/...` |
| Bronze | Reddit post by the person who built it, not a third-party summary | `/r/LocalLLaMA/comments/...` |

**Not accepted as primary sources:**
- Twitter/X threads (too easy to fabricate)
- Blog posts summarizing someone else's work
- Any URL that 404s, 403s permanently, or redirects to a domain parking page
- "Trust me bro" (no link at all)

---

## Automated Verification Pipeline

When you open a PR that touches `usecases/*.md`, the CI pipeline runs:

1. **GitHub star check** — every `github.com/owner/repo` URL is resolved via the GitHub API. Minimum threshold: 10 stars. (Exception: brand-new Hermes plugins, labeled `nascent` in PR title, get a 0-star pass.)
2. **Source-alive check** — every non-GitHub URL gets a HEAD request. 403/429 → yellow (not red), because anti-bot protection ≠ dead link.
3. **Reddit mention detection** (optional) — if the usecase claims Reddit origin, a `--reddit-query` search attempts to corroborate. 403 from Reddit is documented, not a failure.
4. **Confidence score** — weighted composite of the above. Thresholds:
   - < 50 → **red**: likely fabrication, missing corroboration, or stale links
   - 50–80 → **yellow**: plausible but thin — needs more sources or time
   - > 80 → **green**: well-corroborated, live sources, high confidence

---

## Confidence Scoring Breakdown

| Component | Weight | What triggers full points |
|-----------|--------|---------------------------|
| Source alive | 50% | ≥ 50% of non-GitHub URLs return 200 |
| Engagement | 30% | At least one GitHub repo ≥ 10 stars |
| Corroboration | 20% | Multiple repos, or repo + source, or repo + Reddit |

**No source URLs at all?** You can still hit 80 (yellow) with two verified GitHub repos. To get green, add a non-GitHub source or a Reddit query.

---

## For Contributors

### Before Submitting

- [ ] At least one `github.com/...` link with **live star count** (visible on the repo page)
- [ ] If citing docs, the URL resolves with 200 (not 404 or redirect)
- [ ] The usecase name matches the filename: `usecases/my-topic.md`
- [ ] No AI-generated hallucinations: if you didn't personally verify the star count, run the script

### Running the Script Locally

```bash
python scripts/verify-usecase.py --usecase usecases/my-topic.md --check all
```

This generates `usecases/my-topic.verification.md` — include it in your PR if you want reviewers to trust the numbers immediately.

### Labels

- `nascent` → bypasses star threshold (for repos < 48 hours old)
- `community-only` → no GitHub repo exists yet; relies on docs + Reddit corroboration

---

## Examples

### Verified Usecase

```markdown
---
usecase: "matt-pocock-skills-subagents.md"
verified: true
repos_checked: 2
---

# Verification Report

- **mattpocock/skills**: 45790 stars (✅ above threshold)
- **mattpocock/sandcastle**: 1592 stars (✅ above threshold)

## Confidence Score

- **Score**: 80/100
- **Flag**: yellow
- **Badge**: ![matt--pocock--skills--subagents](https://img.shields.io/badge/matt--pocock--skills--subagents-80%2F100-yellow)
```

**Why yellow?** Two repos = strong corroboration (40 pts), stars above threshold (30 pts), but zero non-GitHub sources (0/50). To get green, add a docs link or Reddit post that still resolves.

### Rejected Usecase

```markdown
---
usecase: "totally-real-ai-agent.md"
verified: true
repos_checked: 1
sources_checked: 1
sources_alive: 0
sources_red: 1
---

# Verification Report

- **totallyreal/ai-agent**: 0 stars (❌ below threshold)
- **https://totallyreal.com/**: client-error (404)

## Confidence Score

- **Score**: 0/100
- **Flag**: red
- **Badge**: ![totally--real--ai--agent](https://img.shields.io/badge/totally--real--ai--agent-0%2F100-red)
```

**Why rejected:** Repo has 0 stars (below 10 threshold), claimed primary source 404s. This is classic fabrication pattern.

---

## FAQ

**Q: My usecase has no GitHub repo yet. Can I still submit?**
A: Yes — label it `community-only`. Score will be capped at yellow until a repo exists, but docs + Reddit corroboration is acceptable.

**Q: The script says my source URL is "blocked" (403). Is my usecase dead?**
A: Not necessarily. Some platforms (Reddit, X/Twitter, some docs sites) return 403 to bots. This is a **yellow** flag, not red. Include a screenshot or manual verification in your PR description.

**Q: Why are X/Twitter threads disallowed as primary sources?**
A: Fabrication risk is too high. A single screenshot can be faked in 30 seconds. GitHub repos cannot — they have commit history, issue tracker, and star counts that are public and verifiable.

**Q: How often does the CI re-verify existing usecases?**
A: Currently only on PR touching `usecases/*.md`. A nightly cron is planned (Issue #7).
