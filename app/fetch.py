import os
import hashlib
from datetime import date
from dotenv import load_dotenv
import requests

load_dotenv()

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_API_KEY = os.getenv("SUPABASE_API_KEY")


def generate_unique_id(article_url: str, source: str, fetched_at: date) -> str:
    base = f"{source}:{article_url}:{fetched_at.isoformat()}"
    return hashlib.sha1(base.encode()).hexdigest()


def save_articles_to_db(articles: list[dict]):
    fetched_at = date.today()

    # ref: https://docs.postgrest.org/en/v12/references/api/tables_views.html#upsert
    url = f"{SUPABASE_URL}/rest/v1/articles"
    headers = {
        "apikey": SUPABASE_API_KEY,
        "Authorization": f"Bearer {SUPABASE_API_KEY}",
        "Content-Type": "application/json",
        "Prefer": "resolution=merge-duplicates",
    }

    for article in articles:
        article_id = generate_unique_id(article["url"], article["source"], fetched_at)

        payload = {
            "id": article_id,
            "url": article["url"],
            "title": article["title"],
            "description": article.get("description", ""),
            "source": article["source"],
            "published_at": (
                article["published_at"].isoformat()
                if hasattr(article["published_at"], "isoformat")
                else article["published_at"]
            ),
            "fetched_at": fetched_at.isoformat(),
        }

        response = requests.post(url, headers=headers, json=payload)
        if not response.ok:
            print(f"Failed to save article {article['url']}: {response.text}")


def lambda_handler(event=None, context=None):
    from app.parsers.qiita import fetch_qiita_articles
    from app.parsers.zenn import fetch_zenn_articles

    articles = []
    articles.extend(fetch_zenn_articles())
    articles.extend(fetch_qiita_articles())
    save_articles_to_db(articles)
    return {
        "statusCode": 200,
        "count": len(articles),
        "body": "Articles fetched and saved successfully.",
    }
