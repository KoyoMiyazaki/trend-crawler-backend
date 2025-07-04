from app.parsers.qiita import fetch_qiita_articles
from app.parsers.zenn import fetch_zenn_articles
from app.fetch import save_articles_to_db


def main():
    articles = []
    articles.extend(fetch_qiita_articles())
    articles.extend(fetch_zenn_articles())
    save_articles_to_db(articles)


if __name__ == "__main__":
    main()
