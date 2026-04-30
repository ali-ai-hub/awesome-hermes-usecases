---
# Issues for Feature: Automated Usecase Verification Pipeline
---

## Issue 1: GitHub star verification (backend path)
**Vertical slice:** End-to-end star count fetching + reporting for GitHub-sourced usecases

- [ ] Implement `check_github_stars()` in `scripts/verify-usecase.py`
- [ ] Use public GitHub API with $GITHUB_TOKEN fallback for higher rate limit
- [ ] Test against 3 real usecases: mattpocock/skills (45.6k), ComfyUI (69k), skills repo
- [ ] Generate markdown report with YAML front-matter
- [ ] Add `--check=github-stars` CLI flag
- **HITL gate:** Verify star counts match live GitHub numbers

## Issue 2: Primary source URL alive check (frontend entry)
**Vertical slice:** HTTP HEAD check + report for any usecase type

- [ ] Implement `check_source_alive()` with HEAD request
- [ ] Test against Reddit-sourced usecase (HERMES.md billing post)
- [ ] Handle 403/429 anti-bot responses gracefully (yellow flag, not red)
- [ ] Wire into report generation
- **HITL gate:** Test with 2 real usecases, confirm false-negative rate

## Issue 3: Reddit mention detection (separate platform)
**Vertical slice:** old.reddit.com search for Reddit-sourced usecases

- [ ] Implement `check_reddit_mentions()`
- [ ] Parse result count + top post engagement
- [ ] Cache results to avoid repeated scraping
- [ ] Document limitations in report
- **HITL gate:** Verify output matches manual search for existing usecase

## Issue 4: CI integration (GitHub Actions wrapper)
**Vertical slice:** PR automation + comment posting

- [ ] Create `.github/workflows/verify.yml`
- [ ] Trigger on PR affecting `usecases/*.md`
- [ ] Run `verify-usecase.py --ci`
- [ ] Post PR comment with report summary
- [ ] FAIL PR on any red flag; warn on yellow
- **HITL gate:** Admin token permission review

## Issue 5: Confidence scoring + badges
**Vertical slice:** Scoring matrix + visual indicators

- [ ] Define scoring: Source alive (50%), Engagement detected (30%), Multiple corroborations (20%)
- [ ] Implement `calculate_confidence_score()`
- [ ] Map to red/yellow/green: <50 red, 50-80 yellow, >80 green
- [ ] Generate shield badge markdown for README
- **HITL gate:** Manual threshold calibration

## Issue 6: Contributor documentation
**Parallel, no dependencies**

- [ ] Write `docs/verification-criteria.md`
- [ ] Define "primary source" requirements
- [ ] Add "For Contributors" section to README
- [ ] Include examples: verified vs rejected usecase
