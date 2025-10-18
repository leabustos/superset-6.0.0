#!/bin/bash
# Script de despliegue de Superset
# Uso: ./deploy.sh [dev|prod|modular] [workers]

set -e

MODE=${1:-dev}
WORKERS=${2:-2}

echo "🚀 Desplegando Superset en modo: $MODE"

case $MODE in
  dev)
    echo "📦 Modo desarrollo con certificados autofirmados"
    
    # Generar certificados si no existen
    if [ ! -f "nginx/certs-dev/selfsigned.crt" ]; then
      echo "🔐 Generando certificados autofirmados..."
      ./scripts/setup-dev-certs.sh
    fi
    
    docker compose -f docker-compose.dev.yml up -d
    echo "✅ Superset disponible en https://localhost"
    echo "⚠️  Acepta el certificado autofirmado en tu navegador"
    ;;
    
  prod)
    echo "🏭 Modo producción con certificados SSL"
    if [ ! -f "nginx/certs/cert.crt" ] || [ ! -f "nginx/certs/cert.key" ]; then
      echo "❌ Error: Certificados SSL no encontrados en nginx/certs/"
      echo "   Coloca tus certificados como:"
      echo "   - nginx/certs/cert.crt"
      echo "   - nginx/certs/cert.key"
      exit 1
    fi
    docker compose up -d
    docker compose up -d --scale superset-worker=$WORKERS
    echo "✅ Superset desplegado con $WORKERS workers"
    ;;
    
  modular)
    echo "🔧 Modo modular - desplegando servicios independientes"
    
    # Crear red si no existe
    docker network create superset_net 2>/dev/null || true
    
    # Desplegar en orden
    echo "1️⃣  Desplegando PostgreSQL..."
    docker compose -f microservicios/docker-compose.db.yml up -d
    
    echo "2️⃣  Desplegando Redis..."
    docker compose -f microservicios/docker-compose.redis.yml up -d
    
    echo "⏳ Esperando que la base de datos esté lista..."
    sleep 10
    
    echo "3️⃣  Desplegando Superset..."
    docker compose -f microservicios/docker-compose.superset.yml up -d
    
    echo "⏳ Esperando que Superset esté listo..."
    sleep 15
    
    echo "4️⃣  Desplegando $WORKERS workers..."
    docker compose -f microservicios/docker-compose.worker.yml up -d --scale superset-worker=$WORKERS
    
    echo "5️⃣  Desplegando Celery Beat..."
    docker compose -f microservicios/docker-compose.worker-beat.yml up -d
    
    echo "6️⃣  Desplegando Nginx (dev)..."
    docker compose -f microservicios/docker-compose.nginx-dev.yml up -d
    
    echo "✅ Despliegue modular completado"
    echo "📊 Servicios:"
    echo "   - PostgreSQL: localhost:5432"
    echo "   - Redis: localhost:6379"
    echo "   - Superset: localhost:8088"
    echo "   - Nginx: https://localhost"
    echo "   - Workers: $WORKERS instancias"
    ;;
    
  stop)
    echo "🛑 Deteniendo todos los servicios..."
    docker compose -f docker-compose.dev.yml down 2>/dev/null || true
    docker compose down 2>/dev/null || true
    docker compose -f microservicios/docker-compose.db.yml down 2>/dev/null || true
    docker compose -f microservicios/docker-compose.redis.yml down 2>/dev/null || true
    docker compose -f microservicios/docker-compose.superset.yml down 2>/dev/null || true
    docker compose -f microservicios/docker-compose.worker.yml down 2>/dev/null || true
    docker compose -f microservicios/docker-compose.worker-beat.yml down 2>/dev/null || true
    docker compose -f microservicios/docker-compose.nginx-dev.yml down 2>/dev/null || true
    docker compose -f microservicios/docker-compose.nginx-ssl.yml down 2>/dev/null || true
    echo "✅ Todos los servicios detenidos"
    ;;
    
  *)
    echo "❌ Modo desconocido: $MODE"
    echo ""
    echo "Uso: $0 [modo] [workers]"
    echo ""
    echo "Modos disponibles:"
    echo "  dev      - Desarrollo con certificados autofirmados"
    echo "  prod     - Producción con certificados SSL reales"
    echo "  modular  - Despliegue modular de servicios independientes"
    echo "  stop     - Detener todos los servicios"
    echo ""
    echo "Ejemplos:"
    echo "  $0 dev"
    echo "  $0 prod 5"
    echo "  $0 modular 10"
    echo "  $0 stop"
    exit 1
    ;;
esac

echo ""
echo "📝 Ver logs:"
echo "   docker compose logs -f"
echo ""
echo "🔍 Ver estado:"
echo "   docker compose ps"
