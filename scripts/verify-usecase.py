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
from pathlib import Path
from urllib.request import Request, urlopen
from urllib.error import HTTPError

# GitHub REST API endpoint for public repo metadata (no auth required for public repos)
GITHUB_API = "https://api.github.com/repos/{owner}/{repo}"

# Regex to capture github.com URLs: https://github.com/<owner>/<repo>[optional trailing /...]
GITHUB_URL_RE = re.compile(r'https://github\.com/([^/\s)]+)/([^/\s)]+)')

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


def check_github_stars(owner: str, repo: str, threshold: int = DEFAULT_THRESHOLD):
    """
    Fetch star count for a GitHub repository and compare against a threshold.

    Args:
        owner: Repository owner (user or organization).
        repo: Repository name.
        threshold: Minimum star count to pass (default 10).

    Returns:
        Tuple of (star_count: int, is_above_threshold: bool).
    """
    url = GITHUB_API.format(owner=owner, repo=repo)
    data = fetch_json(url)
    star_count = data.get("stargazers_count", 0)
    return star_count, star_count >= threshold


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
    for owner, repo, stars, ok in results:
        status = "✅ above threshold" if ok else "❌ below threshold"
        lines.append(f"- **{owner}/{repo}**: {stars} stars ({status})")
    lines.append("")
    lines.append("## Summary")
    lines.append(f"- Total repos checked: {len(results)}")
    passed = sum(1 for _, _, _, ok in results if ok)
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
                stars, ok = check_github_stars(owner, repo)
                results.append((owner, repo, stars, ok))
                print(f"{owner}/{repo}: {stars} stars (threshold {'met' if ok else 'not met'})")
            except HTTPError as e:
                print(f"Error fetching {owner}/{repo}: {e.code} {e.reason}", file=sys.stderr)
                results.append((owner, repo, None, False))

    report = generate_report(args.usecase, results, source_results)
    print("\n--- Generated Markdown Report ---\n")
    print(report)

    # Optionally write report beside the usecase file
    report_path = Path(args.usecase).with_suffix(".verification.md")
    report_path.write_text(report, encoding="utf-8")
    print(f"\nReport written to: {report_path}")


if __name__ == "__main__":
    main()
