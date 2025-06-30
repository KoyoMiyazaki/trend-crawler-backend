import feedparser
from datetime import datetime


def fetch_zenn_articles():
    """
    ZennのRSSフィードから記事を取得する関数
    """
    # ZennのRSSフィードURL
    rss_url = "https://zenn.dev/feed"
    feed = feedparser.parse(rss_url)
    articles = []

    for entry in feed.entries:
        # published_at は time.struct_time（年, 月, 日, 時, 分, 秒, ...）の形式
        # datetime() は年〜秒までの6つの引数を取るので [:6] でスライスして渡す
        published_at = datetime(*entry.published_parsed[:6])
        articles.append(
            {
                "url": entry.link,
                "title": entry.title,
                "description": entry.summary,
                "source": "zenn",
                "published_at": published_at,
            }
        )

    return articles
