import xml.etree.ElementTree as ET
from datetime import datetime
from typing import List, Dict
import argparse
import sys


def parse_feed(feed_path: str, limit: int = 3) -> List[Dict[str, str]]:
    try:
        tree = ET.parse(feed_path)
        root = tree.getroot()
    except FileNotFoundError:
        print(f"Feed not found: {feed_path}", file=sys.stderr)
        return []
    except ET.ParseError as e:
        print(f"Feed malformed: {e}", file=sys.stderr)
        return []

    items = root.findall('.//item')
    if not items:
        print(f"No items in feed: {feed_path}", file=sys.stderr)
        return []

    posts: List[Dict[str, str]] = []
    for item in items[:limit]:
        title_el = item.find('title')
        link_el = item.find('link')
        pub_date_el = item.find('pubDate')

        title = title_el.text if title_el is not None else "Untitled"
        link = link_el.text if link_el is not None else "#"

        formatted_date = ""
        if pub_date_el is not None and pub_date_el.text:
            try:
                date_obj = datetime.strptime(pub_date_el.text, '%a, %d %b %Y %H:%M:%S %z')
                formatted_date = date_obj.strftime('%b %d, %Y')
            except ValueError:
                print(f"Warning: unparseable date '{pub_date_el.text}'", file=sys.stderr)

        posts.append({"title": title, "link": link, "date": formatted_date})

    return posts


def main() -> None:
    parser = argparse.ArgumentParser(description="Parse RSS feed for blog posts")
    parser.add_argument("--feed", default="feed.xml", help="RSS feed XML path")
    parser.add_argument("--limit", type=int, default=3, help="Number of posts")
    args = parser.parse_args()

    posts = parse_feed(args.feed, args.limit)

    if not posts:
        print("BLOG_TITLE_1=No posts yet")
        print("BLOG_LINK_1=#")
        print("BLOG_DATE_1=")
        sys.exit(1)

    for i, post in enumerate(posts, start=1):
        print(f"BLOG_TITLE_{i}={post['title']}")
        print(f"BLOG_LINK_{i}={post['link']}")
        print(f"BLOG_DATE_{i}={post['date']}")


if __name__ == '__main__':
    main()
