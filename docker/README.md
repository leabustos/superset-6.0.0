# Docker Compose Modulares

Esta carpeta contiene archivos Docker Compose modulares que permiten desplegar servicios por separado en diferentes servidores.

## 📋 Archivos Disponibles

- `docker-compose-db.yml` - PostgreSQL
- `docker-compose-redis.yml` - Redis
- `docker-compose-superset.yml` - Superset (app + workers)
- `docker-compose-nginx.yml` - Nginx

## 🚀 Uso

### Opción 1: Todos los Servicios Juntos

Usa el `docker-compose.yml` principal en la raíz del proyecto:

```bash
cd ..
docker-compose --profile http up -d
```

### Opción 2: Servicios Separados

Despliega cada servicio en un servidor diferente:

#### Servidor 1: Base de Datos

```bash
docker-compose -f docker/docker-compose-db.yml up -d
```

#### Servidor 2: Redis

```bash
docker-compose -f docker/docker-compose-redis.yml up -d
```

#### Servidor 3: Superset

**Importante:** Antes de iniciar, edita `../.env` y configura:
- `POSTGRES_HOST` - IP del servidor de PostgreSQL
- `REDIS_HOST` - IP del servidor de Redis

```bash
docker-compose -f docker/docker-compose-superset.yml up -d
```

#### Servidor 4: Nginx (Opcional)

```bash
docker-compose -f docker/docker-compose-nginx.yml up -d
```

## 🔧 Configuración para Despliegue Distribuido

### 1. Configurar Red

Si los servicios están en diferentes servidores, necesitas configurar la red:

**Opción A: Usar IPs directas**

Edita `../.env`:
```bash
POSTGRES_HOST=192.168.1.10  # IP del servidor PostgreSQL
REDIS_HOST=192.168.1.11     # IP del servidor Redis
```

**Opción B: Usar Docker Swarm o Kubernetes**

Para despliegues más complejos, considera usar:
- Docker Swarm para orquestación simple
- Kubernetes para orquestación avanzada

### 2. Configurar Firewall

Asegúrate de abrir los puertos necesarios:

**PostgreSQL (Servidor 1):**
```bash
sudo ufw allow 5432/tcp
```

**Redis (Servidor 2):**
```bash
sudo ufw allow 6379/tcp
```

**Superset (Servidor 3):**
```bash
sudo ufw allow 8088/tcp
```

**Nginx (Servidor 4):**
```bash
sudo ufw allow 80/tcp
sudo ufw allow 443/tcp
```

### 3. Verificar Conectividad

Desde el servidor de Superset, verifica conectividad:

```bash
# Probar PostgreSQL
telnet <POSTGRES_HOST> 5432

# Probar Redis
telnet <REDIS_HOST> 6379
```

## 📊 Ejemplo de Arquitectura Distribuida

```
┌─────────────────┐
│   Servidor 1    │
│   PostgreSQL    │
│   Puerto 5432   │
└────────┬────────┘
         │
         │
┌────────┴────────┐
│   Servidor 2    │
│     Redis       │
│   Puerto 6379   │
└────────┬────────┘
         │
         │
┌────────┴────────┐
│   Servidor 3    │
│   Superset      │
│   Puerto 8088   │
└────────┬────────┘
         │
         │
┌────────┴────────┐
│   Servidor 4    │
│     Nginx       │
│   Puerto 80     │
└─────────────────┘
```

## 🔒 Seguridad

**IMPORTANTE para despliegue distribuido:**

1. **Usar SSL/TLS** para todas las conexiones
2. **Configurar firewall** para permitir solo IPs específicas
3. **Usar VPN** o red privada entre servidores
4. **Cambiar contraseñas** por defecto
5. **Habilitar autenticación** en Redis

### Ejemplo: Configurar PostgreSQL para acceso remoto

Edita `postgresql.conf`:
```
listen_addresses = '*'
```

Edita `pg_hba.conf`:
```
host    all    all    192.168.1.0/24    md5
```

### Ejemplo: Configurar Redis para acceso remoto

Edita `redis.conf`:
```
bind 0.0.0.0
requirepass tu_password_seguro
```

Actualiza `../.env`:
```
REDIS_PASSWORD=tu_password_seguro
```

## 📝 Notas

- Los archivos modulares comparten la misma red `superset_net` por defecto
- Para despliegue distribuido, necesitas configurar red externa o usar IPs
- Todos los archivos usan `../.env` para variables de entorno
- Los volúmenes son independientes en cada archivo

## 🆘 Troubleshooting

### Error: Cannot connect to database

Verifica:
1. PostgreSQL está corriendo: `docker ps`
2. Puerto está abierto: `telnet <host> 5432`
3. Variables en `.env` son correctas
4. Firewall permite conexión

### Error: Cannot connect to Redis

Verifica:
1. Redis está corriendo: `docker ps`
2. Puerto está abierto: `telnet <host> 6379`
3. Variables en `.env` son correctas
4. Firewall permite conexión

### Error: Network not found

Si usas archivos modulares por separado, la red `superset_net` debe existir:

```bash
docker network create superset_net
```

O usa red externa en cada archivo:

```yaml
networks:
  superset_net:
    external: true
```
