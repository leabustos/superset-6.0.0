#!/bin/bash
# Script para generar certificados autofirmados para desarrollo
# Se ejecuta ANTES de levantar docker-compose.dev.yml

CERT_DIR="nginx/certs-dev"

echo "🔐 Generando certificados autofirmados para desarrollo..."

# Crear directorio si no existe
mkdir -p "$CERT_DIR"

# Verificar si ya existen
if [ -f "$CERT_DIR/selfsigned.crt" ] && [ -f "$CERT_DIR/selfsigned.key" ]; then
    echo "⚠️  Los certificados ya existen en $CERT_DIR"
    read -p "¿Deseas regenerarlos? (s/N): " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Ss]$ ]]; then
        echo "✅ Usando certificados existentes"
        exit 0
    fi
fi

# Generar certificado autofirmado
openssl req -x509 -nodes -days 365 -newkey rsa:2048 \
  -keyout "$CERT_DIR/selfsigned.key" \
  -out "$CERT_DIR/selfsigned.crt" \
  -subj "/C=ES/ST=Madrid/L=Madrid/O=Development/CN=localhost" \
  -addext "subjectAltName=DNS:localhost,DNS:*.localhost,IP:127.0.0.1"

if [ $? -eq 0 ]; then
    echo "✅ Certificados generados exitosamente en: $CERT_DIR"
    echo "   - Certificado: $CERT_DIR/selfsigned.crt"
    echo "   - Clave: $CERT_DIR/selfsigned.key"
    echo ""
    echo "🚀 Ahora puedes ejecutar:"
    echo "   docker compose -f docker-compose.dev.yml up -d"
else
    echo "❌ Error al generar certificados"
    exit 1
fi
