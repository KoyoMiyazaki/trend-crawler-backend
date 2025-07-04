import os
import requests
from dotenv import load_dotenv

load_dotenv()


def fetch_qiita_articles():
    """
    QiitaのAPIから記事を取得する関数
    5ページ分のデータを取得し、いいね数でソートして上位20件を返す
    """

    headers = {"Authorization": f"Bearer {os.getenv('QIITA_ACCESS_TOKEN')}"}
    articles = []
    for i in range(1, 6):
        url = f"https://qiita.com/api/v2/items?page={i}&per_page=100"
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            data = response.json()
            for item in data:
                articles.append(
                    {
                        "url": item["url"],
                        "title": item["title"],
                        "description": item["body"][:500],
                        "source": "qiita",
                        "published_at": item["created_at"],
                        "likes_count": item["likes_count"],
                    }
                )

    top_articles = sorted(articles, key=lambda x: x["likes_count"], reverse=True)[:20]
    # likes_countを除外して返す
    result = [
        {k: v for k, v in article.items() if k != "likes_count"}
        for article in top_articles
    ]
    return result
