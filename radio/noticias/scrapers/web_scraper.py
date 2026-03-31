import requests
from bs4 import BeautifulSoup
from datetime import datetime


HEADERS = {"User-Agent": "Mozilla/5.0 (compatible; RadioNewsBot/1.0)"}


def fetch_web(source: dict, max_items: int = 5) -> list:
    """Scraping HTML como fallback cuando no hay RSS disponible."""
    try:
        response = requests.get(source["url"], headers=HEADERS, timeout=10)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, "html.parser")

        news = []
        # Busca contenedores comunes de articulos de noticias
        articles = soup.find_all(
            ["article", "div"],
            class_=lambda c: c and any(
                kw in c.lower() for kw in ["noticia", "article", "news", "item", "post", "nota"]
            ),
        )[:max_items]

        for article in articles:
            title_tag = article.find(["h1", "h2", "h3", "h4"])
            if not title_tag:
                continue

            title = title_tag.get_text(strip=True)
            if not title:
                continue

            link_tag = article.find("a", href=True)
            url = link_tag["href"] if link_tag else source["url"]
            if url.startswith("/"):
                url = source["url"].rstrip("/") + url

            summary_tag = article.find("p")
            summary = summary_tag.get_text(strip=True) if summary_tag else ""

            news.append({
                "source": source["name"],
                "title": title,
                "summary": summary[:400] + "..." if len(summary) > 400 else summary,
                "url": url,
                "published": datetime.now(),
            })

        return news

    except Exception as e:
        print(f"    [ERROR] Web {source['name']}: {e}")
        return []
