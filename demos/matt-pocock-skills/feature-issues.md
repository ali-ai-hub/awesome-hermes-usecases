---
# Issues for Feature: Automated Usecase Verification Pipeline
---

## Issue 1: Core validation engine
**Vertical slice:** Script skeleton + single-usecase verification

- [ ] Create `scripts/verify-usecase.py` with `UsecaseValidator` class
- [ ] Implement `check_source_alive()` — HEAD request any URL, return (status, is_200)
- [ ] Implement `check_github_stars()` — public API fetch with $GITHUB_TOKEN fallback
- [ ] Implement `generate_report()` — markdown output with YAML front-matter
- [ ] Add `--usecase` CLI flag for single-file mode
- [ ] Add `--ci` flag for exit-code behavior (0 = all green/yellow, 1 = any red)
- **HITL gate:** Report format review by maintainer

## Issue 2: GitHub Actions CI integration
**Vertical slice:** Auto-run on PR, fail on red flags

- [ ] Create `.github/workflows/verify.yml`
- [ ] Trigger on PR affecting `usecases/*.md`
- [ ] Set up Python 3.11 + dependencies
- [ ] Run `verify-usecase.py --ci` on all modified usecases
- [ ] Post PR comment with report summary
- [ ] FAIL PR if any red flag; WARN if any yellow
- **HITL gate:** Token permissions for PR comments

## Issue 3: Reddit verification capability
**Vertical slice:** Mention detection for Reddit-sourced usecases

- [ ] Implement `check_reddit_mentions()` using old.reddit.com HTTP search
- [ ] Parse result count + top post engagement
- [ ] Cache results to avoid repeated scraping
- [ ] Add Reddit-specific confidence scoring (not just binary found/missing)
- [ ] Document Reddit anti-bot limitations in `docs/verification-criteria.md`
- **HITL gate:** Manual audit of 5 Reddit-sourced usecases

## Issue 4: Multi-source confidence score
**Vertical slice:** Weighted scoring, not just pass/fail

- [ ] Define scoring matrix: GitHub stars (40%), URL alive (30%), Reddit/X mention (30%)
- [ ] Implement `calculate_confidence_score()` returning 0-100
- [ ] Map score to red/yellow/green: <50 = red, 50-80 = yellow, >80 = green
- [ ] Add confidence score to report front-matter
- [ ] Generate per-usecase badge for README (stretch)
- **HITL gate:** Manual review of scoring thresholds

## Issue 5: Verification criteria documentation
**Vertical slice:** Human-readable rules for contributors

- [ ] Write `docs/verification-criteria.md`
- [ ] Define "primary source" requirements (GitHub repo, official docs, or authenticated social post)
- [ ] Document Reddit scraping limitations and workarounds
- [ ] Provide examples: verified usecase vs rejected usecase
- [ ] Add to README as "For Contributors" section
- **HITL gate:** External contributor reads doc and understands rules
