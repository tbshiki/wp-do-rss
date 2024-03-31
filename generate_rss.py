import feedparser
import PyRSS2Gen
import datetime

# 読み込みたいRSSフィードのURL
feed_urls = [
    "https://wptavern.com/feed",
    "https://kinsta.com/blog/feed/",
    "https://www.wpbeginner.com/feed/",
    "https://gutenbergtimes.com/feed/",
]

# 全てのフィードエントリを保持するリスト
all_entries = []

# 各フィードを読み込み、エントリをリストに追加
for url in feed_urls:
    feed = feedparser.parse(url)
    all_entries.extend(feed.entries)

# エントリを公開日でソート
all_entries.sort(key=lambda entry: entry.published_parsed, reverse=True)

# 新しいRSSフィードの項目を生成
rss_items = []
for entry in all_entries:
    rss_items.append(
        PyRSS2Gen.RSSItem(
            title=entry.title,
            link=entry.link,
            description=entry.description,
            pubDate=datetime.datetime(*entry.published_parsed[:6]),
        )
    )

# 新しいRSSフィードを生成
rss = PyRSS2Gen.RSS2(
    title="WP do",
    link="https://tbshiki.github.io/wp-do-rss/",
    description="WP do RSS feed",
    lastBuildDate=datetime.datetime.now(),
    items=rss_items,
)

# ファイルに書き出す前にRSSフィードをUTF-8のXML文字列として生成
rss_xml = rss.to_xml(encoding="utf-8")

# RSSフィードをファイルに書き出す
with open("feed/index.xml", "w", encoding="utf-8") as f:
    f.write(rss_xml)
