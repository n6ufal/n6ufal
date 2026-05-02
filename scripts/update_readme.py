import os, re

with open('README.md', 'r') as f:
    content = f.read()

blog_title = os.getenv('BLOG_TITLE', 'No posts')
blog_link = os.getenv('BLOG_LINK', '#')
blog_date = os.getenv('BLOG_DATE', '')
blog_line = f"[{blog_title}]({blog_link})" + (f" — {blog_date}" if blog_date else "")

content = re.sub(
    r'(<!-- blog-start -->).*?(<!-- blog-end -->)',
    lambda m: f"{m.group(1)}\n{blog_line}\n{m.group(2)}",
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