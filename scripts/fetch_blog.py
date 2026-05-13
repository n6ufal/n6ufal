import xml.etree.ElementTree as ET
from datetime import datetime

tree = ET.parse('feed.xml')
root = tree.getroot()
items = root.findall('.//item')

if items:
    for i, item in enumerate(items[:3], start=1):
        title = item.find('title').text
        link = item.find('link').text
        pubDate = item.find('pubDate').text
        date_obj = datetime.strptime(pubDate, '%a, %d %b %Y %H:%M:%S %z')
        formatted_date = date_obj.strftime('%b %d, %Y')
        print(f"BLOG_TITLE_{i}={title}")
        print(f"BLOG_LINK_{i}={link}")
        print(f"BLOG_DATE_{i}={formatted_date}")
else:
    print("BLOG_TITLE_1=No posts yet")
    print("BLOG_LINK_1=#")
    print("BLOG_DATE_1=")