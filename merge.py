import feedparser
import os
from feedgen.feed import FeedGenerator
from datetime import timezone
import time

with open("feeds.txt") as f:
    urls = [line.strip() for line in f if line.strip()]

fg = FeedGenerator()
fg.id("https://reading-rss-feed.github.io/merged.xml")
fg.title("Manga Watch - Merged Feed")
fg.link(href="https://reading-rss-feed.github.io")
fg.language("en")

entries = []
for url in urls:
    feed = feedparser.parse(url)
    for e in feed.entries:
        entries.append(e)

entries.sort(key=lambda e: e.get("published_parsed") or time.gmtime(0), reverse=True)

for e in entries[:100]:
    fe = fg.add_entry()
    fe.id(e.get("link", e.get("id", "")))
    fe.title(e.get("title", "No title"))
    fe.link(href=e.get("link", ""))
    if e.get("published_parsed"):
        from datetime import datetime
        dt = datetime(*e.published_parsed[:6], tzinfo=timezone.utc)
        fe.published(dt)
        fe.updated(dt)

os.makedirs("public", exist_ok=True)
fg.atom_str(pretty=True)
with open("public/merged.xml", "wb") as f:
    f.write(fg.atom_str(pretty=True))

print(f"Merged {len(entries)} entries from {len(urls)} feeds.")
