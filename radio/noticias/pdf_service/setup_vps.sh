#!/bin/bash
# Script de instalacion del PDF Service en la VPS
# Ejecutar como root o con sudo

set -e

PROJECT_DIR="/opt/radio"

echo "=== Instalando PDF Service para Radio AM ==="

# 1. Crear directorio del proyecto
mkdir -p $PROJECT_DIR
cd $PROJECT_DIR

# 2. Clonar o actualizar el repositorio
if [ -d "claudecode" ]; then
    echo "Actualizando repositorio..."
    cd claudecode && git pull && cd ..
else
    echo "Clonando repositorio..."
    git clone https://github.com/edugpy/claudecode.git
fi

# 3. Crear entorno virtual
if [ ! -d "venv" ]; then
    python3 -m venv venv
fi

# 4. Instalar dependencias
source venv/bin/activate
pip install --upgrade pip
pip install -r claudecode/radio/noticias/requirements.txt
pip install -r claudecode/radio/noticias/pdf_service/requirements.txt

# 5. Crear directorio de salida
mkdir -p $PROJECT_DIR/claudecode/radio/noticias/pdf_service/output

# 6. Instalar servicio systemd
cp claudecode/radio/noticias/pdf_service/boletin-pdf.service /etc/systemd/system/
sed -i "s|/opt/radio|$PROJECT_DIR|g" /etc/systemd/system/boletin-pdf.service

systemctl daemon-reload
systemctl enable boletin-pdf
systemctl start boletin-pdf

echo ""
echo "=== Instalacion completada ==="
echo "Estado del servicio:"
systemctl status boletin-pdf --no-pager
echo ""
echo "Probar con: curl http://localhost:8000/health"
