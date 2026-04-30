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

# Default star threshold for Hermes ecosystem repos
DEFAULT_THRESHOLD = 10


def fetch_json(url: str) -> dict:
    """Fetch JSON from a URL with a standard GitHub Accept header."""
    req = Request(url, headers={"Accept": "application/vnd.github.v3+json"})
    with urlopen(req, timeout=30) as resp:
        return json.load(resp)


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


def generate_report(usecase_path: str, results: list) -> str:
    """
    Build a markdown report with YAML front-matter.

    Args:
        usecase_path: Path to the original usecase markdown.
        results: List of tuples (owner, repo, star_count, is_above_threshold).

    Returns:
        Markdown string.
    """
    lines = []
    lines.append("---")
    lines.append(f'usecase: "{Path(usecase_path).name}"')
    lines.append("verified: true")
    lines.append(f"repos_checked: {len(results)}")
    lines.append("---")
    lines.append("")
    lines.append("# GitHub Star Verification Report")
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
    args = parser.parse_args()

    repos = parse_github_repos_from_markdown(args.usecase)
    if not repos:
        print("No GitHub repositories found in the markdown file.", file=sys.stderr)
        sys.exit(1)

    results = []
    for owner, repo in repos:
        try:
            stars, ok = check_github_stars(owner, repo)
            results.append((owner, repo, stars, ok))
            print(f"{owner}/{repo}: {stars} stars (threshold {'met' if ok else 'not met'})")
        except HTTPError as e:
            print(f"Error fetching {owner}/{repo}: {e.code} {e.reason}", file=sys.stderr)
            results.append((owner, repo, None, False))

    report = generate_report(args.usecase, results)
    print("\n--- Generated Markdown Report ---\n")
    print(report)

    # Optionally write report beside the usecase file
    report_path = Path(args.usecase).with_suffix(".verification.md")
    report_path.write_text(report, encoding="utf-8")
    print(f"\nReport written to: {report_path}")


if __name__ == "__main__":
    main()
