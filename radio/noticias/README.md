# Modulo de Noticias — Radio AM Villarrica

Sistema automatico de recoleccion de noticias, generacion de boletines en PDF y distribucion por email y WhatsApp.

## Fuentes configuradas

| Medio | URL | Metodo |
|-------|-----|--------|
| ABC Color | www.abc.com.py | RSS |
| Ultima Hora | www.ultimahora.com | RSS |
| La Nacion | www.lanacion.com.py | RSS |
| Radio Guaira | www.radioguaira.com | RSS |

## Flujo del sistema

```
Fuentes RSS/Web --> Scraper --> Generador PDF --> Email + WhatsApp
     (cada 1 hora)
```

## Estructura

```
noticias/
├── main.py                  # Orquestador principal (scheduler)
├── config.py                # Configuracion de fuentes y credenciales
├── requirements.txt
├── .env.example             # Variables de entorno (copiar a .env)
├── scrapers/
│   ├── rss_scraper.py       # Scraping via RSS feeds
│   └── web_scraper.py       # Scraping HTML como fallback
├── generators/
│   └── pdf_generator.py     # Genera boletin en PDF
└── distributors/
    ├── email_sender.py      # Envio por email (SMTP)
    └── whatsapp_sender.py   # Envio por WhatsApp (Twilio)
```

## Instalacion

```bash
# 1. Crear entorno virtual
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows

# 2. Instalar dependencias
pip install -r requirements.txt

# 3. Configurar variables de entorno
cp .env.example .env
# Editar .env con tus credenciales

# 4. Ejecutar
python main.py
```

## Configuracion de credenciales

### Email (Gmail)
1. Activar verificacion en dos pasos en tu cuenta Gmail
2. Generar una **App Password**: Google Account > Seguridad > Contrasenas de aplicacion
3. Usar esa contrasena en `EMAIL_PASSWORD`

### WhatsApp (Twilio)
1. Crear cuenta en https://www.twilio.com (tiene plan gratuito)
2. Activar el Sandbox de WhatsApp en la consola de Twilio
3. Cargar `TWILIO_ACCOUNT_SID` y `TWILIO_AUTH_TOKEN` en el `.env`
4. Los destinatarios deben enviar el codigo de activacion al sandbox primero

### Proximos pasos
- [ ] Agregar fuentes de Facebook (Meta Graph API)
- [ ] Agregar fuentes de X/Twitter (X API v2)
- [ ] Agregar resumen automatico con Claude AI
