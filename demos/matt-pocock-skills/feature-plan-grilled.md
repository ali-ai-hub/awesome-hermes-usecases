# Feature: Automated Usecase Verification Pipeline (GRILLED)

## Problem Statement
Every new usecase in the awesome-hermes-usecases repo requires manual verification of primary sources (GitHub star counts, Reddit post engagement, X/Twitter mentions). This creates a bottleneck, introduces human error, and risks fabricated usecases entering the catalog.

## Solution
A pipeline that automatically validates incoming usecase PRs by checking source URLs, fetching live metrics, and generating a verification report with red/yellow/green flags.

## Design Decisions (Post-Grill)

### Decision 1: Single script, not GitHub Action-only
- **Rationale**: Users run verification before PR. CI catches what they miss.
- **Trade-off**: Duplicates logic across local and CI. Mitigated by `verify-usecase.py` being the single source of truth.

### Decision 2: Read GitHub stars via public API, not scraping
- **Rationale**: Scraping breaks. API has rate limits but is contractually stable.
- **Trade-off**: Unauthenticated API hits 60 req/hr limit. Mitigated by caching.

### Decision 3: Report as Markdown, not JSON
- **Rationale**: Humans read reports, machines can parse Markdown.
- **Trade-off**: Less structured for downstream automation. Mitigated by front-matter YAML block.

### Decision 4: Git-only for Reddit verification
- **Rationale**: Reddit has aggressive anti-bot. Git commits mentioning the usecase are checkable.
- **Trade-off**: Misses organic mentions. Accepted as a known limitation.

## User Stories

1. As a contributor, I want my usecase PR auto-verified so that I don't wait for manual review.
2. As a maintainer, I want red-flag usecases blocked from merge so that fabrication risk stays ≤1%.
3. As a reader, I want star counts refreshed on page load so that I trust the numbers.
4. As a reviewer, I want a one-page verification summary so that I decide in under 30 seconds.

## Surfaces Touched

| Surface | Action |
|---------|--------|
| `scripts/verify-usecase.py` | New. Core validation engine. |
| `.github/workflows/verify.yml` | New. CI runner calling the script. |
| `docs/verification-criteria.md` | New. Human-readable rules for what counts as verified. |
| `README.md` | Modify. Badge auto-update logic (stretch). |

## Interface (Deep Module)

```python
# scripts/verify-usecase.py
class UsecaseValidator:
    def validate(self, usecase_path: Path) -> VerificationReport:
        '''Single entry point. Orchestrates all checks.'''
        
    def check_github_stars(self, repo_url: str) -> tuple[int, bool]:
        '''Returns (star_count, is_above_threshold).'''
        
    def check_source_alive(self, url: str) -> tuple[int, bool]:
        '''Returns (status_code, is_200).'''
        
    def check_reddit_mentions(self, query: str) -> MentionSummary:
        '''Returns engagement metrics.'''
        
    def generate_report(self) -> MarkdownReport:
        '''Synthesizes all checks into a red/yellow/green doc.'''
```

## Risk Register

| Risk | Likelihood | Impact | Mitigation |
|------|-----------|--------|------------|
| GitHub API rate limit | High | Medium | Cache results, allow manual override |
| False negative on valid source | Medium | High | Yellow flag + human review, not auto-reject |
| Platform API changes | Low | Medium | Pin API versions, test monthly |
| Maintainer doesn't trust report | Medium | High | Report includes all raw data + decision log |
