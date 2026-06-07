import json
from typing import Dict, List, Tuple
import argparse
import sys


def count_languages(repos_path: str) -> List[Tuple[str, int]]:
    try:
        with open(repos_path, 'r') as f:
            repos = json.load(f)
    except FileNotFoundError:
        print(f"File not found: {repos_path}", file=sys.stderr)
        return []
    except json.JSONDecodeError as e:
        print(f"Invalid JSON in {repos_path}: {e}", file=sys.stderr)
        return []

    if not isinstance(repos, list):
        print(f"{repos_path} is not a list", file=sys.stderr)
        return []

    counts: Dict[str, int] = {}
    for repo in repos:
        if not isinstance(repo, dict):
            continue
        lang = repo.get('language')
        if isinstance(lang, str) and lang:
            counts[lang] = counts.get(lang, 0) + 1

    return sorted(counts.items(), key=lambda x: (-x[1], x[0]))


def main() -> None:
    parser = argparse.ArgumentParser(description="Aggregate top languages from repos.json")
    parser.add_argument("--repos", default="repos.json", help="Path to repos JSON")
    parser.add_argument("--limit", type=int, default=5, help="Number of top languages")
    args = parser.parse_args()

    top = count_languages(args.repos)[:args.limit]

    if top:
        langs_str = ', '.join(lang for lang, _ in top)
    else:
        langs_str = "No language data yet"

    print(f"TOP_LANGS={langs_str}")


if __name__ == '__main__':
    main()
