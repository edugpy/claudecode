import os
import sys
from datetime import datetime

from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
from pydantic import BaseModel
import uvicorn

# Reutiliza el generador de PDF existente
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from generators.pdf_generator import generate_pdf

app = FastAPI(title="Radio PDF Service", version="1.0")


class NewsItem(BaseModel):
    source: str
    title: str
    summary: str = ""
    url: str = ""
    published: str = ""


class BulletinRequest(BaseModel):
    radio_name: str = "Radio AM Villarrica"
    news: list[NewsItem]


@app.get("/health")
def health():
    return {"status": "ok", "timestamp": datetime.now().isoformat()}


@app.post("/generate-pdf")
def generate_bulletin(request: BulletinRequest):
    if not request.news:
        raise HTTPException(status_code=400, detail="La lista de noticias esta vacia.")

    news_list = [
        {
            "source": item.source,
            "title": item.title,
            "summary": item.summary,
            "url": item.url,
            "published": datetime.now(),
        }
        for item in request.news
    ]

    pdf_path = generate_pdf(news_list, "output", request.radio_name)
    filename = os.path.basename(pdf_path)
    return FileResponse(pdf_path, media_type="application/pdf", filename=filename)


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
