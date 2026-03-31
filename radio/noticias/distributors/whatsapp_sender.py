from datetime import datetime


def send_whatsapp(
    pdf_path: str,
    recipients: list,
    account_sid: str,
    auth_token: str,
    from_number: str,
    radio_name: str = "Radio AM",
) -> bool:
    """Envia notificacion por WhatsApp via Twilio."""
    if not account_sid or not auth_token or not recipients:
        print("  [WARN] WhatsApp no configurado. Omitiendo envio.")
        return False

    try:
        from twilio.rest import Client

        client = Client(account_sid, auth_token)
        now_str = datetime.now().strftime("%d/%m/%Y %H:%M")

        body = (
            f"*{radio_name}*\n"
            f"Boletin de Noticias - {now_str} hs\n\n"
            f"El boletin ya esta disponible. Revisa tu email para el PDF completo."
        )

        for recipient in recipients:
            to = (
                f"whatsapp:{recipient}"
                if not recipient.startswith("whatsapp:")
                else recipient
            )
            client.messages.create(body=body, from_=from_number, to=to)
            print(f"  [OK] WhatsApp enviado a: {recipient}")

        return True

    except Exception as e:
        print(f"  [ERROR] WhatsApp: {e}")
        return False
