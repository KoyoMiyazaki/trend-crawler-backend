from app.parsers.zenn import fetch_zenn_articles
from app.fetch import save_articles_to_db


def main():
    zenn_articles = fetch_zenn_articles()
    save_articles_to_db(zenn_articles)


if __name__ == "__main__":
    main()
