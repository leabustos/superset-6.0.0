#!/bin/bash
# Script para configurar certificados SSL de producción
# Uso: ./scripts/setup-production-certs.sh <ruta-cert> <ruta-key>

set -e

if [ $# -ne 2 ]; then
    echo "❌ Error: Se requieren 2 argumentos"
    echo ""
    echo "Uso: $0 <ruta-certificado> <ruta-clave>"
    echo ""
    echo "Ejemplo:"
    echo "  $0 /ruta/a/mi-cert.crt /ruta/a/mi-key.key"
    echo "  $0 /etc/letsencrypt/live/midominio.com/fullchain.pem /etc/letsencrypt/live/midominio.com/privkey.pem"
    exit 1
fi

CERT_FILE=$1
KEY_FILE=$2
DEST_DIR="nginx/certs"

echo "🔐 Configurando certificados SSL de producción"

# Verificar que los archivos existen
if [ ! -f "$CERT_FILE" ]; then
    echo "❌ Error: Certificado no encontrado: $CERT_FILE"
    exit 1
fi

if [ ! -f "$KEY_FILE" ]; then
    echo "❌ Error: Clave privada no encontrada: $KEY_FILE"
    exit 1
fi

# Crear directorio de destino
mkdir -p "$DEST_DIR"

# Copiar certificados
echo "📋 Copiando certificados a $DEST_DIR..."
cp "$CERT_FILE" "$DEST_DIR/cert.crt"
cp "$KEY_FILE" "$DEST_DIR/cert.key"

# Establecer permisos seguros
chmod 644 "$DEST_DIR/cert.crt"
chmod 600 "$DEST_DIR/cert.key"

echo "✅ Certificados configurados correctamente"
echo ""
echo "📁 Archivos:"
echo "   - Certificado: $DEST_DIR/cert.crt"
echo "   - Clave: $DEST_DIR/cert.key"
echo ""
echo "🚀 Ahora puedes desplegar en producción:"
echo "   ./deploy.sh prod"
