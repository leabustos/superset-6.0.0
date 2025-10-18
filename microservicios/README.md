# Arquitectura de Microservicios - Superset

Documentación completa de la arquitectura modular de Superset con servicios independientes y escalables.

## 📋 Tabla de Contenidos

- [Estructura](#estructura)
- [Despliegue Completo](#despliegue-completo)
- [Escalado de Workers](#escalado-de-workers)
- [Arquitectura y Comunicación](#arquitectura-y-comunicación)
- [Ventajas](#ventajas)
- [Troubleshooting](#troubleshooting)

## 📁 Estructura

```
microservicios/
├── docker-compose.db.yml           # PostgreSQL independiente
├── docker-compose.redis.yml        # Redis independiente
├── docker-compose.superset.yml     # Superset App + Init
├── docker-compose.worker.yml       # Workers de Celery (escalable) ⭐
├── docker-compose.worker-beat.yml  # Celery Beat Scheduler (1 instancia)
├── docker-compose.nginx-ssl.yml    # Nginx con SSL real
└── docker-compose.nginx-dev.yml    # Nginx con certificados autofirmados
```

## 🚀 Despliegue Completo

### 1. Infraestructura Base (DB + Redis)

```bash
# Crear la red compartida
docker network create superset_net

# Levantar PostgreSQL
docker compose -f microservicios/docker-compose.db.yml up -d

# Levantar Redis
docker compose -f microservicios/docker-compose.redis.yml up -d
```

### 2. Aplicación Superset

```bash
# Levantar Superset (incluye init y app)
docker compose -f microservicios/docker-compose.superset.yml up -d
```

### 3. Workers (Escalable)

```bash
# Levantar 2 workers por defecto
docker compose -f microservicios/docker-compose.worker.yml up -d

# O escalar a N workers
docker compose -f microservicios/docker-compose.worker.yml up -d --scale superset-worker=5

# Agregar más workers sin interrumpir los existentes
docker compose -f microservicios/docker-compose.worker.yml up -d --scale superset-worker=10 --no-recreate
```

### 4. Celery Beat Scheduler

```bash
# ⚠️ Solo UNA instancia de beat debe correr
docker compose -f microservicios/docker-compose.worker-beat.yml up -d
```

### 5. Nginx (Elegir uno)

**Para desarrollo (certificados autofirmados):**
```bash
docker compose -f microservicios/docker-compose.nginx-dev.yml up -d
```

**Para producción (certificados reales):**
```bash
# Asegúrate de tener los certificados en ../nginx/certs/
docker compose -f microservicios/docker-compose.nginx-ssl.yml up -d
```

## 📊 Escalado de Workers

### Ver Workers Activos

```bash
# Ver estado de workers
docker compose -f microservicios/docker-compose.worker.yml ps

# Ver workers registrados en Celery
docker exec superset_app celery -A superset.tasks.celery_app:app inspect registered

# Ver tareas activas
docker exec superset_app celery -A superset.tasks.celery_app:app inspect active

# Ver estadísticas
docker exec superset_app celery -A superset.tasks.celery_app:app inspect stats
```

### Escalar Workers

```bash
# Aumentar a 5 workers
docker compose -f microservicios/docker-compose.worker.yml up -d --scale superset-worker=5

# Reducir a 2 workers
docker compose -f microservicios/docker-compose.worker.yml up -d --scale superset-worker=2

# Escalar sin interrumpir servicios existentes
docker compose -f microservicios/docker-compose.worker.yml up -d --scale superset-worker=10 --no-recreate
```

### Recomendaciones de Escalado

| Escenario | Usuarios | Workers | CPU | RAM |
|-----------|----------|---------|-----|-----|
| Desarrollo | 1-5 | 1-2 | 2 cores | 2GB |
| Pequeña empresa | 10-50 | 2-3 | 4 cores | 4GB |
| Mediana empresa | 50-200 | 5-10 | 8 cores | 8GB |
| Gran empresa | 200+ | 10-20+ | 16+ cores | 16GB+ |

## 🏗️ Arquitectura y Comunicación

### Diagrama de Arquitectura

```
┌─────────────────────────────────────────────────────────────┐
│                         Internet                             │
└──────────────────────────┬──────────────────────────────────┘
                           │
                    ┌──────▼──────┐
                    │    Nginx    │ :80/:443 (SSL)
                    │  (Reverse   │
                    │   Proxy)    │
                    └──────┬──────┘
                           │
                    ┌──────▼──────┐
                    │  Superset   │ :8088
                    │     App     │
                    └──────┬──────┘
                           │
        ┌──────────────────┼──────────────────┐
        │                  │                  │
   ┌────▼────┐      ┌──────▼──────┐    ┌─────▼─────┐
   │PostgreSQL│      │    Redis    │    │  Workers  │
   │  :5432   │      │    :6379    │    │ (Celery)  │
   │          │      │             │    │  N inst.  │
   └──────────┘      └─────────────┘    └─────┬─────┘
                                              │
                                        ┌─────▼─────┐
                                        │   Beat    │
                                        │ Scheduler │
                                        │ (1 inst.) │
                                        └───────────┘
```

### Flujo de Comunicación

1. **Usuario → Nginx**
   - Puerto 80 (HTTP) redirige a 443 (HTTPS)
   - Puerto 443 (HTTPS) con SSL/TLS

2. **Nginx → Superset App**
   - Proxy reverso a `http://superset_app:8088`
   - WebSocket support para actualizaciones en tiempo real

3. **Superset App → PostgreSQL**
   - Conexión: `postgresql://superset:password@db:5432/superset`
   - Pool de conexiones configurado

4. **Superset App → Redis**
   - Conexión: `redis://redis:6379/0`
   - Usado para caché y sesiones

5. **Workers → Redis**
   - Celery usa Redis como broker de mensajes
   - Múltiples workers pueden conectarse simultáneamente

6. **Beat → Redis**
   - Programa tareas periódicas
   - Solo UNA instancia debe correr

### Servicios y Puertos

| Servicio | Puerto Interno | Puerto Externo | Escalable |
|----------|---------------|----------------|-----------|
| PostgreSQL | 5432 | - | No |
| Redis | 6379 | - | No* |
| Superset App | 8088 | - | Sí** |
| Workers | - | - | ✅ Sí |
| Beat | - | - | ❌ No (solo 1) |
| Nginx | 80, 443 | 80, 443 | No |

*Redis puede escalarse con Redis Cluster (no implementado)  
**Superset App puede escalarse con load balancer (no implementado)

## ✅ Ventajas de esta Arquitectura

### 1. Escalabilidad Horizontal
- Workers pueden escalarse independientemente
- Sin afectar otros servicios
- Agregar/quitar capacidad dinámicamente

### 2. Modularidad
- Cada servicio tiene su propio compose
- Fácil de entender y mantener
- Actualizaciones independientes

### 3. Flexibilidad
- Servicios pueden correr en diferentes hosts
- Fácil migración entre ambientes
- Configuraciones separadas dev/prod

### 4. Alta Disponibilidad
- Múltiples workers distribuyen carga
- Fácil recuperación ante fallos
- Sin downtime al escalar

### 5. Desarrollo/Producción
- Configuraciones claras y separadas
- Fácil cambio entre ambientes
- Testing aislado

## 🔄 Orden de Despliegue Recomendado

```bash
# 1. Red
docker network create superset_net

# 2. Base de datos
docker compose -f microservicios/docker-compose.db.yml up -d

# 3. Caché
docker compose -f microservicios/docker-compose.redis.yml up -d

# 4. Esperar que DB esté lista
sleep 10

# 5. Aplicación Superset
docker compose -f microservicios/docker-compose.superset.yml up -d

# 6. Esperar que Superset esté listo
sleep 15

# 7. Workers
docker compose -f microservicios/docker-compose.worker.yml up -d --scale superset-worker=5

# 8. Beat Scheduler
docker compose -f microservicios/docker-compose.worker-beat.yml up -d

# 9. Nginx (elegir uno)
docker compose -f microservicios/docker-compose.nginx-dev.yml up -d
# O
docker compose -f microservicios/docker-compose.nginx-ssl.yml up -d
```

## 🐛 Troubleshooting

### Workers no se conectan

```bash
# Verificar que Redis esté corriendo
docker compose -f microservicios/docker-compose.redis.yml ps

# Ver logs de workers
docker compose -f microservicios/docker-compose.worker.yml logs -f

# Verificar conexión a Redis desde worker
docker exec -it $(docker ps -q -f name=superset_worker) redis-cli -h redis ping
```

### Superset no inicia

```bash
# Verificar que DB esté saludable
docker compose -f microservicios/docker-compose.db.yml ps

# Ver logs de init
docker logs superset_init

# Verificar conexión a DB
docker exec superset_db pg_isready -U superset
```

### Nginx no puede conectar

```bash
# Verificar que Superset esté corriendo
docker compose -f microservicios/docker-compose.superset.yml ps

# Probar conexión directa
curl http://localhost:8088/health

# Ver logs de Nginx
docker compose -f microservicios/docker-compose.nginx-dev.yml logs -f
```

### Workers no procesan tareas

```bash
# Ver tareas pendientes
docker exec superset_app celery -A superset.tasks.celery_app:app inspect reserved

# Ver workers activos
docker exec superset_app celery -A superset.tasks.celery_app:app inspect active_queues

# Reiniciar workers
docker compose -f microservicios/docker-compose.worker.yml restart
```

## 🧹 Limpieza

### Detener Servicios

```bash
# Detener todos los servicios
docker compose -f microservicios/docker-compose.db.yml down
docker compose -f microservicios/docker-compose.redis.yml down
docker compose -f microservicios/docker-compose.superset.yml down
docker compose -f microservicios/docker-compose.worker.yml down
docker compose -f microservicios/docker-compose.worker-beat.yml down
docker compose -f microservicios/docker-compose.nginx-dev.yml down

# O usar el compose principal
cd .. && docker compose down
```

### Eliminar Volúmenes (¡CUIDADO! Borra datos)

```bash
docker compose -f microservicios/docker-compose.db.yml down -v
docker compose -f microservicios/docker-compose.redis.yml down -v
docker compose -f microservicios/docker-compose.superset.yml down -v
```

## 📝 Notas Importantes

- **Celery Beat**: Solo debe haber UNA instancia corriendo. No escalar.
- **Workers**: Pueden escalarse horizontalmente sin límite práctico.
- **Red**: Todos los servicios deben estar en la red `superset_net`.
- **Volúmenes**: Los volúmenes son compartidos entre servicios cuando es necesario.
- **Certificados SSL**: Para producción, coloca tus certificados en `../nginx/certs/`.
- **Orden de inicio**: Respetar el orden de despliegue para evitar errores.

## 🔗 Enlaces Útiles

- [README Principal](../README.md)
- [Documentación de Superset](https://superset.apache.org/docs/intro)
- [Documentación de Celery](https://docs.celeryproject.org/)
- [Documentación de Docker Compose](https://docs.docker.com/compose/)

## 💡 Tips y Mejores Prácticas

1. **Monitoreo**: Implementa monitoreo de workers con Flower o similar
2. **Logs**: Usa un sistema de log aggregation (ELK, Loki)
3. **Backups**: Automatiza backups de PostgreSQL
4. **Alertas**: Configura alertas para workers caídos
5. **Recursos**: Monitorea uso de CPU/RAM de workers
6. **Escalado**: Escala workers según carga, no preventivamente
7. **Testing**: Prueba escalado en staging antes de producción
