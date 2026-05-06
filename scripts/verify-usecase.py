#!/usr/bin/env python3
"""
verify-usecase.py

Check GitHub stars for repositories linked in a usecase markdown file.
Generates a markdown report with YAML front-matter.

Usage:
    python scripts/verify-usecase.py --usecase path/to/readme.md
"""

import argparse
import json
import re
import sys
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Optional
from urllib.parse import quote_plus
from urllib.request import Request, urlopen
from urllib.error import HTTPError

# GitHub REST API endpoint for public repo metadata (no auth required for public repos)
GITHUB_API = "https://api.github.com/repos/{owner}/{repo}"

# Regex to capture github.com URLs: https://github.com/<owner>/<repo>[optional trailing /...]
GITHUB_URL_RE = re.compile(r'https://github\.com/([^/\s\)\]\>]+)/([^/\s\)\]\>]+)')

# Not used — parse_source_urls_from_markdown is regex-free

# Default star threshold for Hermes ecosystem repos
DEFAULT_THRESHOLD = 10


def fetch_json(url: str) -> dict:
    """Fetch JSON from a URL with a standard GitHub Accept header."""
    req = Request(url, headers={"Accept": "application/vnd.github.v3+json"})
    with urlopen(req, timeout=30) as resp:
        return json.load(resp)


def check_source_alive(url: str) -> dict:
    """
    Perform an HTTP HEAD check on any URL. Returns status mapping.

    403/429 are flagged as "yellow" (anti-bot protection, not necessarily dead).
    Everything else follows standard HTTP semantics.
    """
    try:
        req = Request(url, method="HEAD", headers={
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                          "AppleWebKit/537.36 (KHTML, like Gecko) "
                          "Chrome/120.0.0.0 Safari/537.36",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
            "Accept-Language": "en-US,en;q=0.5",
            "Accept-Encoding": "identity",
        })
        with urlopen(req, timeout=10) as resp:
            code = resp.getcode()
            if 200 <= code < 400:
                return {"url": url, "status": "alive", "code": code, "flag": "green"}
            else:
                return {"url": url, "status": f"unexpected-{code}", "code": code, "flag": "red"}
    except HTTPError as e:
        code = e.code
        if code in (403, 429):
            return {"url": url, "status": "blocked", "code": code, "flag": "yellow"}
        elif 400 <= code < 500:
            return {"url": url, "status": "client-error", "code": code, "flag": "red"}
        else:
            return {"url": url, "status": f"server-error-{code}", "code": code, "flag": "red"}
    except Exception as e:
        return {"url": url, "status": f"error-{type(e).__name__}", "code": None, "flag": "red"}


def check_reddit_mentions(query: str, cache_dir: str = "scripts/.cache") -> dict:
    """
    Search old.reddit.com for mentions of a topic. Cached per query to avoid
    repeated scraping. Returns result count and top post engagement.

    This is a best-effort signal, not primary-source verification.
    Reddit blocks programmatic access; old.reddit.com with a Firefox
    UA gives the highest success rate from an unauthenticated script.
    """
    cache_path = Path(cache_dir) / "reddit_cache.json"
    try:
        cache = json.loads(cache_path.read_text(encoding="utf-8")) if cache_path.exists() else {}
    except Exception:
        cache = {}

    cache_key = re.sub(r"\W+", "_", query.lower().strip())[:64]
    if cache_key in cache:
        return {"topic": query, **cache[cache_key], "cached": True}

    search_url = f"https://old.reddit.com/search/?q={quote_plus(query)}&sort=new"
    try:
        req = Request(search_url, headers={
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:120.0) "
                          "Gecko/20100101 Firefox/120.0",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
            "Accept-Language": "en-US,en;q=0.5",
        })
        with urlopen(req, timeout=15) as resp:
            html = resp.read().decode("utf-8", "replace")
    except HTTPError as e:
        if e.code == 403:
            return {"topic": query, "status": "blocked", "flag": "yellow", "cached": False, "note": "Reddit anti-bot"}
        return {"topic": query, "status": f"http-{e.code}", "flag": "red", "cached": False}
    except Exception as e:
        return {"topic": query, "status": f"error-{type(e).__name__}", "flag": "red", "cached": False}

    # Very basic parsing: count result blocks, grab top title/score
    # old.reddit search page structure: each result is a <div class="search-result ...">
    result_blocks = html.split('class="search-result ')
    count = max(0, len(result_blocks) - 1)

    top_post = None
    # Try to extract first result title + score
    m = re.search(r'class="search-title"[^>]*>\s*<a[^>]*>([^<]+)</a>', html)
    if m:
        top_post = m.group(1).strip()

    result = {
        "topic": query,
        "status": "checked",
        "count": count,
        "top_post": top_post,
        "flag": "green" if count > 0 else "yellow",
        "cached": False,
    }
    cache[cache_key] = {k: v for k, v in result.items() if k != "cached"}
    cache_path.parent.mkdir(parents=True, exist_ok=True)
    cache_path.write_text(json.dumps(cache, indent=2), encoding="utf-8")
    return result


def calculate_confidence_score(repos_results: list, source_results: list, reddit_result: dict = None) -> tuple:
    """
    Calculate confidence score based on three weighted signals.

    - Source alive (50%): if source URLs exist, most must be green
    - Engagement detected (30%): GitHub repos above star threshold
    - Multiple corroborations (20%): 2+ repos, or repo + source, or repo + reddit

    A usecase with zero source URLs can still score up to 80 (yellow).
    Perfect score requires stars + source + reddit.
    """
    score = 0

    # Source alive (50%)
    if source_results:
        total = len(source_results)
        green = sum(1 for r in source_results if r.get("flag") == "green")
        if total > 0 and green / total >= 0.5:
            score += 50
        elif green > 0:
            score += 25

    # Engagement detected (30%)
    if repos_results:
        any_engaged = any(
            stars is not None and ok
            for _, _, stars, ok, _ in repos_results
        )
        if any_engaged:
            score += 30

    # Multiple corroborations (20%)
    types_present = 0
    repo_count = len([r for r in repos_results if r[2] is not None and r[3]])
    if repo_count >= 2:
        types_present = 2  # Multiple repos = strong corroboration
    elif repos_results:
        types_present = 1

    if source_results and any(r.get("flag") in ("green", "yellow") for r in source_results):
        types_present += 1
    if reddit_result and reddit_result.get("flag") == "green":
        types_present += 1

    if types_present >= 2:
        score += 20
    elif types_present >= 1:
        score += 10

    if score > 80:
        flag = "green"
    elif score >= 50:
        flag = "yellow"
    else:
        flag = "red"

    return score, flag


def generate_badge(usecase_name: str, score: int, flag: str) -> str:
    """Generate a shields.io badge markdown string."""
    color_map = {"green": "brightgreen", "yellow": "yellow", "red": "red"}
    color = color_map.get(flag, "lightgrey")
    label = usecase_name.replace("-", "--")
    return f"![{label}](https://img.shields.io/badge/{label}-{score}%2F100-{color})"


def is_recent_repo(created_at: Optional[str], max_age_hours: int = 48) -> bool:
    """Return true when a repository was created within the nascent window."""
    if not created_at:
        return False
    try:
        created = datetime.fromisoformat(created_at.replace("Z", "+00:00"))
    except ValueError:
        return False
    return datetime.now(timezone.utc) - created <= timedelta(hours=max_age_hours)


def check_github_stars(
    owner: str,
    repo: str,
    threshold: int = DEFAULT_THRESHOLD,
    allow_nascent: bool = False,
):
    """
    Fetch star count for a GitHub repository and compare against a threshold.

    Args:
        owner: Repository owner (user or organization).
        repo: Repository name.
        threshold: Minimum star count to pass (default 10).

    Returns:
        Tuple of (star_count: int, is_above_threshold: bool, reason: str).
    """
    url = GITHUB_API.format(owner=owner, repo=repo)
    data = fetch_json(url)
    star_count = data.get("stargazers_count", 0)
    if star_count >= threshold:
        return star_count, True, "threshold"
    if allow_nascent and is_recent_repo(data.get("created_at")):
        return star_count, True, "nascent"
    return star_count, False, "below-threshold"


def parse_github_repos_from_markdown(path: str):
    """
    Parse a markdown file and extract unique GitHub owner/repo pairs.

    Args:
        path: Path to the markdown file.

    Returns:
        List of (owner, repo) tuples in order of first appearance.
    """
    text = Path(path).read_text(encoding="utf-8")
    matches = GITHUB_URL_RE.findall(text)
    seen = set()
    repos = []
    for owner, repo in matches:
        repo = repo.rstrip('.,;:!?')
        if repo.endswith(".git"):
            repo = repo[:-4]
        key = (owner, repo)
        if key not in seen:
            seen.add(key)
            repos.append(key)
    return repos


def parse_source_urls_from_markdown(path: str):
    """
    Parse a markdown file and extract unique non-GitHub source URLs.

    Uses a two-pass approach: find all http(s) URLs, then filter
    GitHub repos and trailing punctuation.
    """
    text = Path(path).read_text(encoding="utf-8")
    # find all http(s) URLs regardless of wrapping chars
    raw = re.findall(r'https?://[^\s\)\>\]]+', text, re.IGNORECASE)
    seen = set()
    urls = []
    image_exts = ('.png', '.jpg', '.jpeg', '.gif', '.svg', '.ico', '.webp', '.mp4')
    for url in raw:
        # strip trailing punctuation commonly found in markdown
        url = url.rstrip('.,;:!?')
        if url.endswith(')'):
            # heuristic: if the ')' is not matched by a preceding '(', drop it
            if url.count('(') < url.count(')'):
                url = url[:-1]
        if url not in seen and not url.startswith('https://github.com/') and not url.endswith(image_exts):
            seen.add(url)
            urls.append(url)
    return urls


def generate_report(usecase_path: str, results: list, source_results: list = None) -> str:
    """
    Build a markdown report with YAML front-matter.

    Args:
        usecase_path: Path to the original usecase markdown.
        results: List of tuples (owner, repo, star_count, is_above_threshold).
        source_results: Optional list of dicts from check_source_alive().

    Returns:
        Markdown string.
    """
    lines = []
    lines.append("---")
    lines.append(f'usecase: "{Path(usecase_path).name}"')
    lines.append("verified: true")
    lines.append(f"repos_checked: {len(results)}")
    if source_results:
        lines.append(f"sources_checked: {len(source_results)}")
        alive_count = sum(1 for r in source_results if r["flag"] == "green")
        yellow_count = sum(1 for r in source_results if r["flag"] == "yellow")
        red_count = sum(1 for r in source_results if r["flag"] == "red")
        lines.append(f"sources_alive: {alive_count}")
        lines.append(f"sources_yellow: {yellow_count}")
        lines.append(f"sources_red: {red_count}")
    lines.append("---")
    lines.append("")
    lines.append("# Verification Report")
    lines.append("")
    for owner, repo, stars, ok, reason in results:
        if reason == "nascent":
            status = "✅ nascent exception"
        else:
            status = "✅ above threshold" if ok else "❌ below threshold"
        lines.append(f"- **{owner}/{repo}**: {stars} stars ({status})")
    lines.append("")
    lines.append("## Summary")
    lines.append(f"- Total repos checked: {len(results)}")
    passed = sum(1 for _, _, _, ok, _ in results if ok)
    lines.append(f"- Passed threshold (≥{DEFAULT_THRESHOLD} stars): {passed}")
    lines.append(f"- Failed threshold (<{DEFAULT_THRESHOLD} stars): {len(results) - passed}")
    lines.append("")
    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(
        description="Verify GitHub stars for repos listed in a usecase markdown file."
    )
    parser.add_argument(
        "--usecase",
        required=True,
        help="Path to the usecase markdown file",
    )
    parser.add_argument(
        "--check",
        choices=["github-stars", "sources-alive", "all"],
        default="all",
        help="Verification scope (default: all)",
    )
    parser.add_argument(
        "--reddit-query",
        default=None,
        help="Search old.reddit.com for mentions of a topic",
    )
    parser.add_argument(
        "--ci",
        action="store_true",
        help="Exit non-zero if any red flag is found",
    )
    parser.add_argument(
        "--allow-nascent",
        action="store_true",
        help="Allow GitHub repos created in the last 48 hours to pass below the star threshold",
    )
    args = parser.parse_args()

    repos = parse_github_repos_from_markdown(args.usecase)
    source_results = []

    if args.check in ("sources-alive", "all"):
        urls = parse_source_urls_from_markdown(args.usecase)
        print(f"Found {len(urls)} non-GitHub source URL(s).")
        for url in urls[:10]:  # cap at 10 to avoid abuse
            result = check_source_alive(url)
            flag_emoji = {"green": "✅", "yellow": "⚠️", "red": "❌"}.get(result["flag"], "❓")
            print(f"  {flag_emoji} {url}: {result['status']} ({result['code']})")
            source_results.append(result)

    results = []
    if args.check in ("github-stars", "all"):
        if not repos:
            print("No GitHub repositories found in the markdown file.", file=sys.stderr)
            if args.check == "github-stars":
                sys.exit(1)
        for owner, repo in repos:
            try:
                stars, ok, reason = check_github_stars(
                    owner,
                    repo,
                    allow_nascent=args.allow_nascent,
                )
                results.append((owner, repo, stars, ok, reason))
                if reason == "nascent":
                    status = "nascent exception"
                else:
                    status = f"threshold {'met' if ok else 'not met'}"
                print(f"{owner}/{repo}: {stars} stars ({status})")
            except HTTPError as e:
                print(f"Error fetching {owner}/{repo}: {e.code} {e.reason}", file=sys.stderr)
                results.append((owner, repo, None, False, "fetch-error"))

    report = generate_report(args.usecase, results, source_results)

    if args.reddit_query:
        print(f"\nSearching Reddit for: {args.reddit_query}")
        reddit_result = check_reddit_mentions(args.reddit_query)
        flag_emoji = {"green": "✅", "yellow": "⚠️", "red": "❌"}.get(reddit_result.get("flag"), "❓")
        print(f"  {flag_emoji} {reddit_result['topic']}: {reddit_result.get('status', 'unknown')} "
              f"(count={reddit_result.get('count', 'n/a')}, top='{reddit_result.get('top_post', 'n/a')}')")
        if reddit_result.get("cached"):
            print("  (from cache)")
    else:
        reddit_result = None

    score, flag = calculate_confidence_score(results, source_results, reddit_result)
    badge = generate_badge(Path(args.usecase).stem, score, flag)
    print(f"\nConfidence Score: {score}/100 ({flag.upper()}) {badge}")

    report += f"\n## Confidence Score\n\n- **Score**: {score}/100\n- **Flag**: {flag}\n- **Badge**: {badge}\n\n"

    if args.reddit_query:
        report += "## Reddit Mentions\n\n"
        report += f"- **Query**: {reddit_result['topic']}\n"
        report += f"- **Status**: {reddit_result.get('status', 'unknown')} ({flag_emoji})\n"
        report += f"- **Result count**: {reddit_result.get('count', 'N/A')}\n"
        if reddit_result.get("top_post"):
            report += f"- **Top post**: {reddit_result['top_post']}\n"
        if reddit_result.get("note"):
            report += f"- **Note**: {reddit_result['note']}\n"
        report += "\n"

    print("\n--- Generated Markdown Report ---\n")
    print(report)

    # Optionally write report beside the usecase file
    report_path = Path(args.usecase).with_suffix(".verification.md")
    report_path.write_text(report, encoding="utf-8")
    print(f"\nReport written to: {report_path}")

    if args.ci:
        any_red = any(r.get("flag") == "red" for r in source_results)
        any_dead_repo = any(stars is not None and not ok for _, _, stars, ok, _ in results)
        if any_red or any_dead_repo:
            print("\n❌ CI mode: red flag(s) detected — failing.", file=sys.stderr)
            sys.exit(1)
        print("\n✅ CI mode: all checks passed.")


if __name__ == "__main__":
    main()
