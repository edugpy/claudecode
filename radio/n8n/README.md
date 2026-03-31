# n8n — Configuracion de Workflows

## Workflow: Boletin de Noticias

Archivo: `workflow_noticias.json`

### Como importar el workflow

1. Abre tu n8n en `https://n8n.panambidigital.com`
2. Menu lateral > **Workflows** > boton **Import**
3. Selecciona el archivo `workflow_noticias.json`

---

## Configuracion previa (hacer antes de activar)

### 1. Variables de entorno en n8n

En n8n: **Settings > Variables** — crear estas variables:

| Variable | Valor | Descripcion |
|----------|-------|-------------|
| `CLAUDE_API_KEY` | `sk-ant-...` | API key de console.anthropic.com |
| `EMAIL_SENDER` | `tucorreo@gmail.com` | Email remitente |
| `EMAIL_RECIPIENTS` | `dest@email.com` | Destinatarios separados por coma |
| `TWILIO_ACCOUNT_SID` | `ACxxxxxxx` | De la consola de Twilio |
| `TWILIO_AUTH_TOKEN` | `xxxxxxx` | De la consola de Twilio |
| `WHATSAPP_RECIPIENTS` | `whatsapp:+595981000000` | Numero destinatario |

### 2. Credencial SMTP (para el nodo Email)

1. En n8n: **Credentials > New > SMTP**
2. Completar:
   - Host: `smtp.gmail.com`
   - Port: `587`
   - User: tu email Gmail
   - Password: App Password de Gmail
3. Guardar y asignar al nodo **Enviar Email** del workflow

### 3. PDF Service en la VPS

El nodo **Generar PDF** llama a `http://localhost:8000/generate-pdf`.
El servicio debe estar corriendo en la VPS antes de activar el workflow.

Ver instrucciones de instalacion en: `../noticias/pdf_service/setup_vps.sh`

```bash
# En la VPS, ejecutar:
sudo bash setup_vps.sh

# Verificar que el servicio esta activo:
curl http://localhost:8000/health
```

---

## Flujo del workflow

```
Cron (cada 1h)
    |
    +--> RSS ABC Color  --+
    +--> RSS Ultima Hora  |
    +--> RSS La Nacion    +--> Merge --> Normalizar
    +--> RSS Radio Guaira +                 |
                                    Claude AI (resumir)
                                            |
                                    Generar PDF (localhost:8000)
                                            |
                              +-------------+-------------+
                              |                           |
                         Enviar Email            Enviar WhatsApp
```
