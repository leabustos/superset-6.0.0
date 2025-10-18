# 🚀 Inicio Rápido - Superset 6.0.0

## Despliegue en 3 Pasos

### 1. Configurar Variables de Entorno

```bash
# Copiar archivo de ejemplo
cp .env.example .env

# Editar credenciales
nano .env
```

Configura al menos:
```bash
ADMIN_USERNAME=admin
ADMIN_PASSWORD=tu_password_seguro_aqui
ADMIN_EMAIL=admin@tudominio.com
SECRET_KEY=$(openssl rand -base64 42)
```

### 2. Desplegar

**Para Desarrollo:**
```bash
./deploy.sh dev
```

**Para Producción:**
```bash
# Primero configura tus certificados SSL
./scripts/setup-production-certs.sh /ruta/a/cert.crt /ruta/a/cert.key

# Luego despliega con 5 workers
./deploy.sh prod 5
```

### 3. Acceder

- **Desarrollo**: https://localhost (acepta el certificado autofirmado)
- **Producción**: https://tu-dominio.com

Usuario: El que configuraste en `ADMIN_USERNAME`  
Contraseña: La que configuraste en `ADMIN_PASSWORD`

## Solución de Problemas Comunes

### "No puedo acceder a https://localhost"

1. Verifica que todos los servicios estén corriendo:
   ```bash
   docker compose -f docker-compose.dev.yml ps
   ```

2. Verifica que los certificados existan:
   ```bash
   ls -la nginx/certs-dev/
   ```

3. Si no existen, genera los certificados:
   ```bash
   ./scripts/setup-dev-certs.sh
   docker compose -f docker-compose.dev.yml restart nginx-dev
   ```

4. Verifica los logs de Nginx:
   ```bash
   docker compose -f docker-compose.dev.yml logs nginx-dev
   ```

### "El navegador dice que la conexión no es segura"

Esto es normal con certificados autofirmados. Haz clic en "Avanzado" → "Continuar a localhost (no seguro)".

### "Superset no carga"

1. Verifica que Superset esté corriendo:
   ```bash
   docker compose -f docker-compose.dev.yml ps superset
   ```

2. Verifica los logs:
   ```bash
   docker compose -f docker-compose.dev.yml logs superset
   ```

3. Prueba acceder directamente sin SSL:
   ```bash
   curl http://localhost:8088/health
   ```

### "Error de base de datos"

1. Verifica que PostgreSQL esté corriendo:
   ```bash
   docker compose -f docker-compose.dev.yml ps db
   ```

2. Reinicia desde cero:
   ```bash
   docker compose -f docker-compose.dev.yml down -v
   ./deploy.sh dev
   ```

## Comandos Útiles

```bash
# Ver estado de servicios
docker compose -f docker-compose.dev.yml ps

# Ver logs en tiempo real
docker compose -f docker-compose.dev.yml logs -f

# Ver logs de un servicio específico
docker compose -f docker-compose.dev.yml logs -f superset

# Reiniciar un servicio
docker compose -f docker-compose.dev.yml restart superset

# Detener todo
docker compose -f docker-compose.dev.yml down

# Detener y borrar datos (¡CUIDADO!)
docker compose -f docker-compose.dev.yml down -v
```

## Próximos Pasos

1. ✅ Conecta tu primera fuente de datos
2. ✅ Crea tu primer gráfico
3. ✅ Crea tu primer dashboard
4. ✅ Lee la documentación completa en [README.md](README.md)

## Ayuda

- Documentación completa: [README.md](README.md)
- Guía de despliegue: [DEPLOYMENT_GUIDE.md](DEPLOYMENT_GUIDE.md)
- Arquitectura: [RESUMEN_ARQUITECTURA.md](RESUMEN_ARQUITECTURA.md)
