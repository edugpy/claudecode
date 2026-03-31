from .rss_scraper import fetch_rss
from .web_scraper import fetch_web


def fetch_news(source: dict, max_items: int = 5) -> list:
    """Obtiene noticias de una fuente. Usa RSS si esta disponible, web scraping como fallback."""
    if source.get("type") == "rss" and source.get("rss"):
        news = fetch_rss(source, max_items)
        if news:
            return news
    return fetch_web(source, max_items)
