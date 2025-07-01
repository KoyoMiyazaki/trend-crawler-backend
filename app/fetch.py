from datetime import date
from app.database import SessionLocal, Base, engine
from app.models import Article
import hashlib

Base.metadata.create_all(bind=engine)


def generate_unique_id(article_url: str, source: str, fetched_at: date) -> str:
    base = f"{source}:{article_url}:{fetched_at.isoformat()}"
    return hashlib.sha1(base.encode()).hexdigest()


def save_articles_to_db(articles: list[dict]):
    session = SessionLocal()
    fetched_at = date.today()

    for article in articles:
        article_id = generate_unique_id(article["url"], article["source"], fetched_at)

        if session.query(Article).filter_by(id=article_id).first():
            continue  # Skip if article already exists

        new_article = Article(
            id=article_id,
            url=article["url"],
            title=article["title"],
            description=article.get("description", ""),
            source=article["source"],
            published_at=article["published_at"],
            fetched_at=fetched_at,
        )
        session.add(new_article)

    session.commit()
    session.close()


def lambda_handler(event=None, context=None):
    from app.parsers.zenn import fetch_zenn_articles

    articles = fetch_zenn_articles()
    save_articles_to_db(articles)
    return {
        "statusCode": 200,
        "count": len(articles),
        "body": "Articles fetched and saved successfully.",
    }
