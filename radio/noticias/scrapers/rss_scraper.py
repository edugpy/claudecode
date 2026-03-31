import feedparser
from bs4 import BeautifulSoup
from datetime import datetime


def fetch_rss(source: dict, max_items: int = 5) -> list:
    """Obtiene noticias desde un feed RSS."""
    try:
        feed = feedparser.parse(source["rss"])
        if feed.bozo and not feed.entries:
            return []

        news = []
        for entry in feed.entries[:max_items]:
            # Limpiar resumen HTML
            summary = entry.get("summary", "")
            if summary:
                soup = BeautifulSoup(summary, "html.parser")
                summary = soup.get_text(separator=" ").strip()

            # Parsear fecha
            try:
                pub_date = datetime(*entry.published_parsed[:6])
            except (AttributeError, TypeError):
                pub_date = datetime.now()

            title = entry.get("title", "").strip()
            if not title:
                continue

            news.append({
                "source": source["name"],
                "title": title,
                "summary": summary[:400] + "..." if len(summary) > 400 else summary,
                "url": entry.get("link", source["url"]),
                "published": pub_date,
            })

        return news

    except Exception as e:
        print(f"    [ERROR] RSS {source['name']}: {e}")
        return []
