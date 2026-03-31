import os
import smtplib
from datetime import datetime
from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


def send_email(
    pdf_path: str,
    recipients: list,
    sender: str,
    password: str,
    smtp_server: str = "smtp.gmail.com",
    smtp_port: int = 587,
    radio_name: str = "Radio AM",
) -> bool:
    """Envia el boletin PDF por email via SMTP."""
    if not recipients or not sender or not password:
        print("  [WARN] Email no configurado. Omitiendo envio.")
        return False

    try:
        now_str = datetime.now().strftime("%d/%m/%Y %H:%M")
        subject = f"Boletin de Noticias — {radio_name} — {now_str}"

        msg = MIMEMultipart()
        msg["From"] = sender
        msg["To"] = ", ".join(recipients)
        msg["Subject"] = subject

        body = (
            f"Adjunto el boletin de noticias de las {datetime.now().strftime('%H:%M')} hs.\n\n"
            f"— {radio_name}"
        )
        msg.attach(MIMEText(body, "plain"))

        with open(pdf_path, "rb") as f:
            part = MIMEBase("application", "octet-stream")
            part.set_payload(f.read())
        encoders.encode_base64(part)
        part.add_header(
            "Content-Disposition",
            f"attachment; filename={os.path.basename(pdf_path)}",
        )
        msg.attach(part)

        with smtplib.SMTP(smtp_server, smtp_port) as server:
            server.starttls()
            server.login(sender, password)
            server.sendmail(sender, recipients, msg.as_string())

        print(f"  [OK] Email enviado a: {', '.join(recipients)}")
        return True

    except Exception as e:
        print(f"  [ERROR] Email: {e}")
        return False
