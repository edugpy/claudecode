import os
from dotenv import load_dotenv

load_dotenv()

# --- Fuentes de noticias ---
SOURCES = [
    {
        "name": "ABC Color",
        "url": "https://www.abc.com.py",
        "rss": "https://www.abc.com.py/arc/outboundfeeds/rss/?outputType=xml",
        "type": "rss",
    },
    {
        "name": "Ultima Hora",
        "url": "https://www.ultimahora.com",
        "rss": "https://www.ultimahora.com/rss.xml",
        "type": "rss",
    },
    {
        "name": "La Nacion",
        "url": "https://www.lanacion.com.py",
        "rss": "https://www.lanacion.com.py/feed/",
        "type": "rss",
    },
    {
        "name": "Radio Guaira",
        "url": "https://www.radioguaira.com",
        "rss": "https://www.radioguaira.com/feed/",
        "type": "rss",
    },
]

# --- Configuracion general ---
MAX_NEWS_PER_SOURCE = 5
FETCH_INTERVAL_HOURS = 1
RADIO_NAME = os.getenv("RADIO_NAME", "Radio AM Villarrica")
OUTPUT_DIR = os.getenv("OUTPUT_DIR", "output")

# --- Email ---
EMAIL_SENDER = os.getenv("EMAIL_SENDER")
EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD")
EMAIL_SMTP_SERVER = os.getenv("EMAIL_SMTP_SERVER", "smtp.gmail.com")
EMAIL_SMTP_PORT = int(os.getenv("EMAIL_SMTP_PORT", "587"))
EMAIL_RECIPIENTS = [r.strip() for r in os.getenv("EMAIL_RECIPIENTS", "").split(",") if r.strip()]

# --- WhatsApp (Twilio) ---
TWILIO_ACCOUNT_SID = os.getenv("TWILIO_ACCOUNT_SID")
TWILIO_AUTH_TOKEN = os.getenv("TWILIO_AUTH_TOKEN")
TWILIO_WHATSAPP_FROM = os.getenv("TWILIO_WHATSAPP_FROM", "whatsapp:+14155238886")
WHATSAPP_RECIPIENTS = [r.strip() for r in os.getenv("WHATSAPP_RECIPIENTS", "").split(",") if r.strip()]
