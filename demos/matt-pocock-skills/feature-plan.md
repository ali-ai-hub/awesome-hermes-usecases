# Feature: Automated Usecase Verification Pipeline

## Problem
Every new usecase PR needs manual source verification (star counts, primary links, fabrication checks). This creates a bottleneck and risks fake usecases slipping through.

## Scope
- Automated star count fetching for GitHub repos
- Primary source URL validation (200 check)
- Cross-platform mention verification (Reddit, X, Discord)
- Report generation with red/yellow/green flags
- Skill-based reviewer assignment

## Surfaces
- README.md (badge auto-update)
- .github/workflows/verify.yml (CI)
- scripts/verify-usecase.py (new script)
- docs/verification-criteria.md (new doc)

## Risks
- GitHub API rate limits
- False negatives on legitimate sources
- Breaking changes in external platform APIs
