#!/bin/bash
# Script para generar certificados SSL autofirmados
# Uso: ./scripts/generate-self-signed-certs.sh [dominio]

DOMAIN=${1:-localhost}
CERT_DIR="../nginx/certs-dev"

echo "🔐 Generando certificados autofirmados para: $DOMAIN"

# Crear directorio si no existe
mkdir -p "$CERT_DIR"

# Generar certificado autofirmado
openssl req -x509 -nodes -days 365 -newkey rsa:2048 \
  -keyout "$CERT_DIR/selfsigned.key" \
  -out "$CERT_DIR/selfsigned.crt" \
  -subj "/C=ES/ST=Madrid/L=Madrid/O=Development/CN=$DOMAIN" \
  -addext "subjectAltName=DNS:$DOMAIN,DNS:*.${DOMAIN},DNS:localhost,IP:127.0.0.1"

echo "✅ Certificados generados en: $CERT_DIR"
echo "   - Certificado: $CERT_DIR/selfsigned.crt"
echo "   - Clave: $CERT_DIR/selfsigned.key"
echo ""
echo "⚠️  Estos certificados son solo para desarrollo"
echo "   Tu navegador mostrará una advertencia de seguridad"
