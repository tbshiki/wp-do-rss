import feedparser
from feedgen.feed import FeedGenerator
from datetime import datetime
import pytz

# 日本時間のタイムゾーンを設定
JST = pytz.timezone("Asia/Tokyo")


def generate_rss_feed():

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
    # 'published_parsed'がない場合は現在時刻を使用する
    all_entries.sort(
        key=lambda entry: entry.get(
            "published_parsed", datetime.now(tz=JST).timetuple()
        ),
        reverse=True,
    )

    # 新しいRSSフィードを初期化
    fg = FeedGenerator()
    fg.title("WP do")
    fg.link(href="https://tbshiki.github.io/wp-do-rss/", rel="alternate")
    fg.description("WP do RSS feed")
    fg.lastBuildDate(datetime.now(JST))

    # 新しいRSSフィードの項目を追加
    for entry in all_entries:
        fe = fg.add_entry()
        fe.title(entry.title)
        fe.link(href=entry.link)
        fe.description(entry.description)
        if hasattr(entry, "published"):
            fe.published(entry.published)

    # RSSフィードをファイルに書き出す
    fg.rss_file("feed/index.xml", pretty=True, encoding="utf-8")


if __name__ == "__main__":
    generate_rss_feed()
