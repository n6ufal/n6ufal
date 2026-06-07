import json
import sys
from datetime import datetime, timedelta, timezone
from typing import Any, Dict, List, Set
from urllib.request import Request, urlopen
from urllib.error import URLError
import argparse


def fetch_user_events(username: str, token: str = "") -> List[Dict[str, Any]]:
    url = f"https://api.github.com/users/{username}/events?per_page=100"
    headers = {
        "Accept": "application/vnd.github.v3+json",
        "User-Agent": "n6ufal-readme/1.0",
    }
    if token:
        headers["Authorization"] = f"Bearer {token}"

    req = Request(url, headers=headers)
    try:
        with urlopen(req, timeout=15) as resp:
            return json.loads(resp.read().decode())
    except URLError as e:
        print(f"Failed to fetch events: {e}", file=sys.stderr)
        return []


def compute_streak(events: List[Dict[str, Any]]) -> int:
    commit_dates: Set[datetime.date] = set()

    for event in events:
        if event.get("type") != "PushEvent":
            continue
        created = event.get("created_at", "")
        if not created:
            continue
        try:
            d = datetime.fromisoformat(created.replace("Z", "+00:00")).date()
            commit_dates.add(d)
        except ValueError:
            continue

    if not commit_dates:
        return 0

    today = datetime.now(timezone.utc).date()
    streak = 0
    current = today
    while current in commit_dates:
        streak += 1
        current -= timedelta(days=1)

    return streak


def main() -> None:
    parser = argparse.ArgumentParser(description="Fetch GitHub commit streak")
    parser.add_argument("--user", default="n6ufal", help="GitHub username")
    parser.add_argument("--token", default="", help="GitHub token (optional)")
    args = parser.parse_args()

    events = fetch_user_events(args.user, args.token)
    streak = compute_streak(events)

    if streak > 0:
        label = f"{streak} day{'s' if streak != 1 else ''}"
    else:
        label = "No recent commits"

    print(f"STREAK={label}")
    print(f"STREAK_NUM={streak}")


if __name__ == '__main__':
    main()
