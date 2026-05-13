import os, re

with open('README.md', 'r') as f:
    content = f.read()

blog_lines = []
for i in range(1, 4):
    title = os.getenv(f'BLOG_TITLE_{i}')
    link = os.getenv(f'BLOG_LINK_{i}', '#')
    date = os.getenv(f'BLOG_DATE_{i}', '')
    if title:
        line = f"- [{title}]({link})" + (f" — {date}" if date else "")
        blog_lines.append(line)

blog_block = "\n".join(blog_lines) if blog_lines else "No posts yet"

content = re.sub(
    r'(<!-- blog-start -->).*?(<!-- blog-end -->)',
    lambda m: f"{m.group(1)}\n{blog_block}\n{m.group(2)}",
    content,
    flags=re.DOTALL
)

langs = os.getenv('TOP_LANGS', 'Fetching...')
content = re.sub(
    r'(<!-- langs-start -->).*?(<!-- langs-end -->)',
    lambda m: f"{m.group(1)}\n{langs}\n{m.group(2)}",
    content,
    flags=re.DOTALL
)

with open('README.md', 'w') as f:
    f.write(content)