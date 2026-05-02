import xml.etree.ElementTree as ET
from datetime import datetime

tree = ET.parse('feed.xml')
root = tree.getroot()
items = root.findall('.//item')

if items:
    item = items[0]
    title = item.find('title').text
    link = item.find('link').text
    pubDate = item.find('pubDate').text
    date_obj = datetime.strptime(pubDate, '%a, %d %b %Y %H:%M:%S %z')
    formatted_date = date_obj.strftime('%b %d, %Y')
    print(f"BLOG_TITLE={title}")
    print(f"BLOG_LINK={link}")
    print(f"BLOG_DATE={formatted_date}")
else:
    print("BLOG_TITLE=No posts yet")
    print("BLOG_LINK=#")
    print("BLOG_DATE=")