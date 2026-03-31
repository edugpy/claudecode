import schedule
import time
from datetime import datetime

from config import (
    SOURCES, MAX_NEWS_PER_SOURCE, FETCH_INTERVAL_HOURS,
    EMAIL_SENDER, EMAIL_PASSWORD, EMAIL_SMTP_SERVER, EMAIL_SMTP_PORT, EMAIL_RECIPIENTS,
    TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN, TWILIO_WHATSAPP_FROM, WHATSAPP_RECIPIENTS,
    OUTPUT_DIR, RADIO_NAME,
)
from scrapers import fetch_news
from generators import generate_pdf
from distributors import send_email, send_whatsapp


def run_boletin():
    print(f"\n{'=' * 55}")
    print(f"  Generando boletin — {datetime.now().strftime('%d/%m/%Y %H:%M')}")
    print(f"{'=' * 55}")

    # 1. Recolectar noticias
    all_news = []
    for source in SOURCES:
        print(f"  Scrapeando: {source['name']}...")
        news = fetch_news(source, MAX_NEWS_PER_SOURCE)
        all_news.extend(news)
        print(f"    -> {len(news)} noticias encontradas")

    if not all_news:
        print("[WARN] No se encontraron noticias. Omitiendo generacion.")
        return

    print(f"\n  Total: {len(all_news)} noticias de {len(SOURCES)} fuentes.")

    # 2. Generar PDF
    pdf_path = generate_pdf(all_news, OUTPUT_DIR, RADIO_NAME)

    # 3. Enviar por email
    send_email(
        pdf_path=pdf_path,
        recipients=EMAIL_RECIPIENTS,
        sender=EMAIL_SENDER,
        password=EMAIL_PASSWORD,
        smtp_server=EMAIL_SMTP_SERVER,
        smtp_port=EMAIL_SMTP_PORT,
        radio_name=RADIO_NAME,
    )

    # 4. Enviar por WhatsApp
    send_whatsapp(
        pdf_path=pdf_path,
        recipients=WHATSAPP_RECIPIENTS,
        account_sid=TWILIO_ACCOUNT_SID,
        auth_token=TWILIO_AUTH_TOKEN,
        from_number=TWILIO_WHATSAPP_FROM,
        radio_name=RADIO_NAME,
    )

    print(f"\n  Boletin completado. Proxima ejecucion en {FETCH_INTERVAL_HOURS}h.")


if __name__ == "__main__":
    print(f"Sistema de Noticias — {RADIO_NAME}")
    print(f"Intervalo: cada {FETCH_INTERVAL_HOURS} hora(s).")

    # Ejecutar inmediatamente al iniciar
    run_boletin()

    # Programar ejecucion horaria
    schedule.every(FETCH_INTERVAL_HOURS).hours.do(run_boletin)

    while True:
        schedule.run_pending()
        time.sleep(60)
