# 🔐 Solución: Certificados Autofirmados para Desarrollo

## Problema Identificado

El `docker-compose.dev.yml` intentaba generar certificados autofirmados dentro del contenedor de Nginx, pero:
1. El contenedor de Nginx no tenía `openssl` instalado
2. Los certificados no persistían entre reinicios
3. El proceso era lento y propenso a errores

## Solución Implementada

### 1. Script de Generación de Certificados

Se creó `scripts/setup-dev-certs.sh` que:
- Genera certificados autofirmados ANTES de levantar Docker
- Los guarda en `nginx/certs-dev/` (persistente)
- Verifica si ya existen para no regenerarlos
- Usa OpenSSL del host (más rápido y confiable)

### 2. Docker Compose Simplificado

El `docker-compose.dev.yml` ahora:
- Monta `nginx/certs-dev/` como volumen de solo lectura
- No intenta generar certificados (más rápido)
- Usa certificados pre-generados

### 3. Script de Despliegue Actualizado

El `deploy.sh` ahora:
- Verifica si existen certificados antes de desplegar
- Los genera automáticamente si no existen
- Despliega con certificados listos

## Uso

### Opción 1: Script Automatizado (Recomendado)

```bash
./deploy.sh dev
```

Esto automáticamente:
1. Verifica si existen certificados
2. Los genera si no existen
3. Levanta todos los servicios
4. Muestra la URL de acceso

### Opción 2: Manual

```bash
# 1. Generar certificados
./scripts/setup-dev-certs.sh

# 2. Levantar servicios
docker compose -f docker-compose.dev.yml up -d

# 3. Acceder
# Abrir https://localhost en el navegador
```

## Verificación

### Verificar que los certificados existen

```bash
ls -la nginx/certs-dev/
```

Deberías ver:
```
-rw-rw-r-- 1 usuario usuario 1.4K Oct  3 12:03 selfsigned.crt
-rw------- 1 usuario usuario 1.7K Oct  3 12:03 selfsigned.key
```

### Verificar que Nginx está corriendo

```bash
docker compose -f docker-compose.dev.yml ps nginx-dev
```

Debería mostrar `Up` y los puertos `80/tcp, 443/tcp`

### Verificar que Superset responde

```bash
# Sin SSL (directo)
curl http://localhost:8088/health

# Con SSL (a través de Nginx)
curl -k https://localhost/health
```

Ambos deberían responder `OK`

## Acceso desde el Navegador

1. Abre https://localhost
2. El navegador mostrará una advertencia de seguridad (normal con certificados autofirmados)
3. Haz clic en "Avanzado" o "Advanced"
4. Haz clic en "Continuar a localhost (no seguro)" o "Proceed to localhost (unsafe)"
5. Deberías ver la pantalla de login de Superset

## Troubleshooting

### Error: "Permission denied" al generar certificados

```bash
# Asegúrate de que el directorio tenga los permisos correctos
sudo chown -R $USER:$USER nginx/certs-dev
./scripts/setup-dev-certs.sh
```

### Error: "Connection refused" al acceder a https://localhost

```bash
# Verifica que Nginx esté corriendo
docker compose -f docker-compose.dev.yml ps nginx-dev

# Verifica los logs de Nginx
docker compose -f docker-compose.dev.yml logs nginx-dev

# Reinicia Nginx
docker compose -f docker-compose.dev.yml restart nginx-dev
```

### Error: "502 Bad Gateway"

Esto significa que Nginx está corriendo pero no puede conectar con Superset.

```bash
# Verifica que Superset esté corriendo
docker compose -f docker-compose.dev.yml ps superset

# Verifica los logs de Superset
docker compose -f docker-compose.dev.yml logs superset

# Prueba acceder directamente a Superset (sin Nginx)
curl http://localhost:8088/health
```

### Los certificados expiraron (después de 365 días)

```bash
# Regenerar certificados
rm -rf nginx/certs-dev/*
./scripts/setup-dev-certs.sh

# Reiniciar Nginx
docker compose -f docker-compose.dev.yml restart nginx-dev
```

## Archivos Modificados

1. **docker-compose.dev.yml**
   - Simplificado el servicio nginx-dev
   - Monta certificados pre-generados

2. **deploy.sh**
   - Agrega verificación y generación automática de certificados

3. **scripts/setup-dev-certs.sh** (NUEVO)
   - Script para generar certificados autofirmados

4. **README.md**
   - Actualizado con instrucciones correctas

5. **INICIO_RAPIDO.md** (NUEVO)
   - Guía rápida con troubleshooting

## Ventajas de esta Solución

✅ **Más rápido**: No instala OpenSSL en cada inicio de Nginx
✅ **Más confiable**: Usa OpenSSL del host
✅ **Persistente**: Los certificados se guardan en el host
✅ **Reutilizable**: Los certificados se generan una sola vez
✅ **Automatizado**: El script deploy.sh lo hace todo
✅ **Verificable**: Puedes ver los certificados en nginx/certs-dev/

## Comparación

### Antes (No Funcionaba)
```yaml
nginx-dev:
  command: >
    /bin/sh -c "
    openssl req ... &&  # ❌ openssl no instalado
    nginx -g 'daemon off;'
    "
```

### Después (Funciona)
```yaml
nginx-dev:
  volumes:
    - ./nginx/certs-dev:/etc/nginx/certs:ro  # ✅ Certificados pre-generados
```

## Próximos Pasos

1. ✅ Probar el despliegue: `./deploy.sh dev`
2. ✅ Acceder a https://localhost
3. ✅ Configurar fuentes de datos
4. ✅ Crear dashboards

## Notas Importantes

- Los certificados autofirmados son **solo para desarrollo**
- Para producción, usa certificados SSL reales (Let's Encrypt, etc.)
- Los certificados generados son válidos por 365 días
- El navegador siempre mostrará advertencia con certificados autofirmados (es normal)

---

**Fecha de solución**: 3 de Octubre, 2025
**Estado**: ✅ Resuelto y probado
