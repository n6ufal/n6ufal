import os
import re
import sys
from typing import Optional
import argparse


def read_file(path: str) -> Optional[str]:
    try:
        with open(path, 'r', encoding='utf-8') as f:
            return f.read()
    except FileNotFoundError:
        print(f"File not found: {path}", file=sys.stderr)
        return None
    except IOError as e:
        print(f"Error reading {path}: {e}", file=sys.stderr)
        return None


def write_file(path: str, content: str) -> bool:
    try:
        with open(path, 'w', encoding='utf-8') as f:
            f.write(content)
        return True
    except IOError as e:
        print(f"Error writing {path}: {e}", file=sys.stderr)
        return False


def build_blog_section() -> str:
    blog_lines = []
    for i in range(1, 4):
        title = os.getenv(f'BLOG_TITLE_{i}')
        link = os.getenv(f'BLOG_LINK_{i}', '#')
        date = os.getenv(f'BLOG_DATE_{i}', '')
        if title and title != "No posts yet":
            line = f"- [{title}]({link})" + (f" — {date}" if date else "")
            blog_lines.append(line)
    return "\n".join(blog_lines) if blog_lines else "No posts yet"


def replace_section(content: str, marker: str, replacement: str) -> str:
    pattern = rf'(<!-- {marker}-start -->).*?(<!-- {marker}-end -->)'
    return re.sub(
        pattern,
        lambda m: f"{m.group(1)}\n{replacement}\n{m.group(2)}",
        content,
        flags=re.DOTALL
    )


def main() -> None:
    parser = argparse.ArgumentParser(description="Update README.md with fetched data")
    parser.add_argument("--readme", default="README.md", help="Path to README.md")
    args = parser.parse_args()

    content = read_file(args.readme)
    if content is None:
        sys.exit(1)

    if not os.getenv('BLOG_TITLE_1'):
        print("Warning: BLOG_TITLE_1 not set", file=sys.stderr)

    blog_block = build_blog_section()
    content = replace_section(content, "blog", blog_block)

    langs = os.getenv('TOP_LANGS', '')
    if not langs:
        print("Warning: TOP_LANGS not set", file=sys.stderr)
        langs = 'Fetching...'
    content = replace_section(content, "langs", langs)

    if not write_file(args.readme, content):
        sys.exit(1)


if __name__ == '__main__':
    main()
