# RADIO — Automatizacion de Noticias y Grillas Horarias

Proyecto de automatizacion para las dos radioemisoras de Villarrica, Paraguay.

## Emisoras

| Emisora | Formato | Enfoque |
|---------|---------|---------|
| Radio AM | Noticias / Informacion | Actualidad, politica, economia |
| Radio FM | Musica | Pop y Rock |

## Modulos del Proyecto

### 1. `noticias/`
Automatizacion de recoleccion, resumen y publicacion de noticias para la AM.
- Scraping de fuentes locales y nacionales
- Resumen automatico con IA
- Generacion de boletines horarios

### 2. `grillas/`
Gestion y generacion de grillas horarias para ambas emisoras.
- Plantillas de programacion semanal
- Exportacion de grillas en formatos utiles (CSV, PDF, etc.)
- Alertas y recordatorios de programas

### 3. `scripts/`
Scripts utilitarios de soporte para ambas emisoras.

## Tecnologias Previstas
- Python 3.x
- APIs de noticias (NewsAPI, RSS feeds locales)
- Claude API para resumen y redaccion automatica
- Pandas para manejo de grillas

## Estado
- [x] Estructura inicial del proyecto
- [ ] Modulo de scraping de noticias
- [ ] Generador de boletines
- [ ] Gestor de grillas horarias
