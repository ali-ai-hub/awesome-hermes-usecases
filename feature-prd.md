---
title: Automated Usecase Verification Pipeline
status: draft
author: @aliaihub
labels: [needs-triage, tooling]
---

# Automated Usecase Verification Pipeline

## Problem Statement
Manual verification of every new usecase PR (star counts, primary source URLs, fabrication checks) creates a maintainer bottleneck and risks fake usecases entering the catalog.

## Solution
A single verification script (`scripts/verify-usecase.py`) callable locally and from CI, which validates usecase files against live sources and produces a red/yellow/green Markdown report.

## User Stories

1. As a contributor, I want my usecase PR auto-verified so that I don't wait for manual review.
2. As a maintainer, I want fabrication-risk usecases blocked from merge so that catalog trust stays high.
3. As a reader, I want star counts refreshed on page load so that I trust the numbers.
4. As a reviewer, I want a one-page verification summary so that I decide in under 30 seconds.

## Implementation

### Module: `scripts/verify-usecase.py`

**Interface (deep module):**

```python
class UsecaseValidator:
    def validate(self, usecase_path: Path) -> VerificationReport:
        '''Orchestrates all checks. Single entry point.'''
        
    def check_github_stars(self, repo_url: str) -> tuple[int, bool]:
        '''Returns (star_count, is_above_threshold). Uses API with $GITHUB_TOKEN if available.'''
        
    def check_source_alive(self, url: str) -> tuple[int, bool]:
        '''HEAD request. Returns (status_code, is_200).'''
        
    def check_reddit_mentions(self, query: str, subreddit: str) -> MentionSummary:
        '''Searches old.reddit.com via HTTP. Returns engagement count.'''
        
    def generate_report(self, checks: list[Check]) -> MarkdownReport:
        '''Synthesizes front-matter YAML + human-readable Markdown.'''
```

### CI Surface: `.github/workflows/verify.yml`

Runs on every PR affecting `usecases/*.md`. Calls `scripts/verify-usecase.py --ci` and fails the PR on any red flag.

### Decision Log

| Decision | Alternatives | Chosen | Rationale |
|----------|-------------|--------|-----------|
| Single python script | Separate JS action | Python | Maintainer skillset |
| Markdown report | JSON only | Markdown | Humans read it; machines parse YAML frontmatter |
| Yellow flag vs red block | Auto-reject all failures | Yellow flag | False negatives are worse than false positives |
| Public GitHub API | Scraping or GraphQL | Public API | Contractual stability over rate limits |

## Acceptance Criteria

- [ ] `scripts/verify-usecase.py --usecase usecases/matt-pocock-skills-subagents.md` returns report
- [ ] Report shows 45.6k stars ✓ for mattpocock/skills
- [ ] Report shows valid 200 ✓ for all primary source URLs
- [ ] CI fails PRs with any red flag
- [ ] Yellow flags generate comment, don't block merge
- [ ] Stretch: README badge auto-updates via cron

## Out of Scope

- Auto-PR creation for star count bumps (would flood git history)
- Chrome extension for reader-side verification (future)
- Integration with Hermes memory for cross-session source tracking
