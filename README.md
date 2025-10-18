# Apache Superset 6.0.0 - Despliegue con Docker

Configuración completa y lista para producción de Apache Superset 6.0.0 con arquitectura modular escalable.

## 🚀 Inicio Rápido

### Desarrollo (5 minutos)

```bash
# 1. Configurar variables de entorno
cp .env.example .env
nano .env  # Editar ADMIN_USERNAME, ADMIN_PASSWORD, SECRET_KEY

# 2. Desplegar
./deploy.sh dev

# 3. Acceder
# https://localhost (acepta el certificado autofirmado)
```

### Producción

```bash
# 1. Configurar certificados SSL
./scripts/setup-production-certs.sh /ruta/a/cert.crt /ruta/a/cert.key

# 2. Desplegar con 5 workers
./deploy.sh prod 5
```

## 📁 Estructura del Proyecto

```
.
├── docker-compose.yml              # Producción con SSL
├── docker-compose.dev.yml          # Desarrollo con certificados autofirmados
├── deploy.sh                       # Script de despliegue automatizado
├── .env                            # Variables de entorno
│
├── superset-config/                # Configuración de Superset
│   ├── Dockerfile                  # Imagen personalizada
│   ├── Dockerfile-oficial-superset # Referencia oficial
│   ├── superset_config.py          # Configuración personalizada
│   └── config.py                   # Configuración base (referencia)
│
├── microservicios/                 # Servicios modulares independientes
│   ├── docker-compose.db.yml
│   ├── docker-compose.redis.yml
│   ├── docker-compose.superset.yml
│   ├── docker-compose.worker.yml
│   ├── docker-compose.worker-beat.yml
│   ├── docker-compose.nginx-ssl.yml
│   ├── docker-compose.nginx-dev.yml
│   └── README.md                   # Documentación de microservicios
│
├── nginx/                          # Configuración de Nginx
│   ├── nginx.conf
│   ├── conf.d/
│   │   ├── superset_ssl.conf      # Producción
│   │   └── superset_dev.conf      # Desarrollo
│   ├── certs/                      # Certificados SSL (producción)
│   └── certs-dev/                  # Certificados autofirmados (desarrollo)
│
└── scripts/                        # Scripts de utilidad
    ├── setup-dev-certs.sh          # Generar certificados autofirmados
    └── setup-production-certs.sh   # Configurar certificados SSL
```

## ⚙️ Configuración

### Variables de Entorno (.env)

```bash
# Admin de Superset
ADMIN_USERNAME=admin
ADMIN_PASSWORD=tu_password_seguro
ADMIN_EMAIL=admin@tudominio.com

# Base de datos PostgreSQL
POSTGRES_DB=superset
POSTGRES_USER=superset
POSTGRES_PASSWORD=tu_password_seguro

# Redis
REDIS_HOST=redis
REDIS_PORT=6379

# Superset
SECRET_KEY=$(openssl rand -base64 42)
SUPERSET_ENV=production

# Dominio (para producción)
DOMAIN_NAME=tu-dominio.com
```

## 🎯 Modos de Despliegue

| Modo | Comando | Uso | Certificados |
|------|---------|-----|--------------|
| **Desarrollo** | `./deploy.sh dev` | Pruebas locales | Autofirmados |
| **Producción** | `./deploy.sh prod 5` | Despliegue real | SSL reales |
| **Modular** | `./deploy.sh modular 10` | Máxima flexibilidad | Ambos |

## 📊 Escalado de Workers

### Recomendaciones

| Escenario | Usuarios | Workers Recomendados |
|-----------|----------|---------------------|
| Desarrollo | 1-5 | 1-2 |
| Pequeña empresa | 10-50 | 2-3 |
| Mediana empresa | 50-200 | 5-10 |
| Gran empresa | 200+ | 10-20+ |

### Comandos

```bash
# Escalar a 10 workers
docker compose up -d --scale superset-worker=10

# Agregar más sin interrumpir
docker compose up -d --scale superset-worker=15 --no-recreate

# Ver workers activos
docker exec superset_app celery -A superset.tasks.celery_app:app inspect active
```

## 🔐 Certificados SSL

### Desarrollo (Autofirmados)

Los certificados se generan automáticamente con `./deploy.sh dev` o manualmente:

```bash
./scripts/setup-dev-certs.sh
```

### Producción (SSL Reales)

```bash
# Opción 1: Script de ayuda
./scripts/setup-production-certs.sh /ruta/a/cert.crt /ruta/a/cert.key

# Opción 2: Let's Encrypt
sudo certbot certonly --standalone -d tu-dominio.com
./scripts/setup-production-certs.sh \
  /etc/letsencrypt/live/tu-dominio.com/fullchain.pem \
  /etc/letsencrypt/live/tu-dominio.com/privkey.pem
```

## 🔍 Monitoreo y Verificación

```bash
# Ver estado de servicios
docker compose ps

# Ver logs en tiempo real
docker compose logs -f

# Healthchecks
curl http://localhost:8088/health                    # Superset
docker exec superset_db pg_isready -U superset       # PostgreSQL
docker exec superset_cache redis-cli ping            # Redis
```

## 🐛 Troubleshooting

### Superset no inicia

```bash
docker logs superset_init
docker compose down -v && docker compose up -d
```

### Workers no procesan tareas

```bash
docker compose logs -f superset-worker
docker compose restart superset-worker
```

### Problemas con certificados

```bash
# Verificar certificados
ls -la nginx/certs-dev/  # Desarrollo
ls -la nginx/certs/      # Producción

# Regenerar certificados de desarrollo
rm -rf nginx/certs-dev/*
./scripts/setup-dev-certs.sh
docker compose -f docker-compose.dev.yml restart nginx-dev
```

## 🛠️ Comandos Útiles

```bash
# Detener servicios
./deploy.sh stop

# Reconstruir imágenes
docker compose build --no-cache

# Ver uso de recursos
docker stats

# Backup de base de datos
docker exec superset_db pg_dump -U superset superset > backup_$(date +%Y%m%d).sql

# Restaurar base de datos
docker exec -i superset_db psql -U superset superset < backup.sql

# Limpiar todo (¡CUIDADO! Borra datos)
docker compose down -v
```

## 📚 Documentación Adicional

- [microservicios/README.md](microservicios/README.md) - Arquitectura modular y escalado
- [INICIO_RAPIDO.md](INICIO_RAPIDO.md) - Guía de inicio rápido con troubleshooting
- [SOLUCION_CERTIFICADOS.md](SOLUCION_CERTIFICADOS.md) - Detalles sobre certificados SSL
- [Documentación oficial de Superset](https://superset.apache.org/docs/intro)

## 🏗️ Arquitectura

```
Internet
    ↓
Nginx (SSL) :80/:443
    ↓
Superset App :8088
    ↓
┌────────┬─────────┬──────────┬────────┐
│        │         │          │        │
PostgreSQL Redis  Worker1  Worker2  WorkerN
:5432    :6379   (Celery) (Celery) (Celery)
                     ↓
                 Beat Scheduler
                 (1 instancia)
```

## 🔧 Personalización

### Modificar Configuración de Superset

Edita `superset-config/superset_config.py` para personalizar:
- Configuración de caché
- Límites de queries
- Feature flags
- Autenticación (LDAP, OAuth, etc.)
- Y más...

### Modificar Dockerfile

El Dockerfile en `superset-config/Dockerfile` incluye:
- PostgreSQL driver (psycopg2-binary)
- Oracle driver (oracledb)
- Locale español
- Paquetes adicionales (Authlib, openpyxl, Pillow)

## 📝 Notas Importantes

- **Celery Beat**: Solo debe haber UNA instancia corriendo
- **Workers**: Pueden escalarse horizontalmente sin límite
- **Certificados**: Los autofirmados son solo para desarrollo
- **Backups**: Configura backups automáticos de PostgreSQL en producción
- **Seguridad**: Cambia todas las contraseñas por defecto en `.env`

## 🤝 Contribuir

1. Fork el proyecto
2. Crea una rama (`git checkout -b feature/AmazingFeature`)
3. Commit tus cambios (`git commit -m 'Add AmazingFeature'`)
4. Push a la rama (`git push origin feature/AmazingFeature`)
5. Abre un Pull Request

## 📄 Licencia

Apache License 2.0

## 🙏 Agradecimientos

- [Apache Superset](https://superset.apache.org/)
- [Docker](https://www.docker.com/)
- [Nginx](https://nginx.org/)
- [PostgreSQL](https://www.postgresql.org/)
- [Redis](https://redis.io/)
