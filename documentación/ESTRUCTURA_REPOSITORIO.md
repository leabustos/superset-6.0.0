# Estructura del Repositorio

## 📁 Organización Final

```
superset-6.0.0/
│
├── 📄 README.md                    # Documentación principal
├── 📄 INICIO_RAPIDO.md             # Guía de inicio rápido
├── 📄 SOLUCION_CERTIFICADOS.md     # Detalles sobre certificados SSL
├── 📄 .env                         # Variables de entorno (no en git)
├── 📄 .gitignore                   # Archivos ignorados por git
│
├── 🐳 docker-compose.yml           # Producción con SSL
├── 🐳 docker-compose.dev.yml       # Desarrollo con certificados autofirmados
├── 🚀 deploy.sh                    # Script de despliegue automatizado
│
├── 📂 superset-config/             # Configuración de Superset
│   ├── README.md                   # Documentación de configuración
│   ├── Dockerfile                  # Imagen personalizada
│   ├── Dockerfile-oficial-superset # Referencia oficial
│   ├── superset_config.py          # Configuración personalizada (USADO)
│   └── config.py                   # Configuración base (referencia)
│
├── 📂 microservicios/              # Servicios modulares independientes
│   ├── README.md                   # Documentación completa de arquitectura
│   ├── docker-compose.db.yml
│   ├── docker-compose.redis.yml
│   ├── docker-compose.superset.yml
│   ├── docker-compose.worker.yml
│   ├── docker-compose.worker-beat.yml
│   ├── docker-compose.nginx-ssl.yml
│   └── docker-compose.nginx-dev.yml
│
├── 📂 nginx/                       # Configuración de Nginx
│   ├── nginx.conf                  # Configuración principal
│   ├── conf.d/
│   │   ├── superset_ssl.conf       # Producción
│   │   └── superset_dev.conf       # Desarrollo
│   ├── certs/                      # Certificados SSL (producción)
│   └── certs-dev/                  # Certificados autofirmados (desarrollo)
│
├── 📂 scripts/                     # Scripts de utilidad
│   ├── setup-dev-certs.sh          # Generar certificados autofirmados
│   ├── setup-production-certs.sh   # Configurar certificados SSL
│   └── generate-self-signed-certs.sh
│
└── 📂 docker/                      # Archivos auxiliares de Docker
    ├── docker-entrypoint-initdb.d/ # Scripts de inicialización de DB
    └── requirements-local.txt      # Dependencias Python adicionales
```

## 📚 Documentación

### Principal
- **README.md**: Documentación principal con inicio rápido, configuración y comandos
- **INICIO_RAPIDO.md**: Guía de 5 minutos con troubleshooting
- **SOLUCION_CERTIFICADOS.md**: Detalles sobre certificados SSL

### Por Módulo
- **microservicios/README.md**: Arquitectura modular completa, escalado, troubleshooting
- **superset-config/README.md**: Explicación de archivos de configuración

## 🎯 Archivos Clave

### Configuración
- `.env`: Variables de entorno (crear desde .env.example)
- `superset-config/superset_config.py`: Configuración de Superset
- `superset-config/Dockerfile`: Imagen Docker personalizada

### Despliegue
- `deploy.sh`: Script automatizado de despliegue
- `docker-compose.yml`: Producción
- `docker-compose.dev.yml`: Desarrollo

### Microservicios
- Cada archivo `docker-compose.*.yml` en `microservicios/` es independiente
- Pueden desplegarse por separado o en conjunto

## 🔍 Navegación Rápida

### Quiero empezar rápido
→ `README.md` → Sección "Inicio Rápido"

### Quiero entender la arquitectura
→ `microservicios/README.md`

### Quiero personalizar Superset
→ `superset-config/superset_config.py`

### Tengo un problema
→ `INICIO_RAPIDO.md` → Sección "Solución de Problemas"
→ `microservicios/README.md` → Sección "Troubleshooting"

### Quiero configurar SSL
→ `SOLUCION_CERTIFICADOS.md`

## 🧹 Limpieza Realizada

### Eliminado
- ❌ Documentación redundante en raíz
- ❌ Archivos de configuración duplicados
- ❌ Carpeta `docs/` con documentación antigua

### Consolidado
- ✅ Toda la documentación en 3 archivos principales
- ✅ Configuración en carpeta `superset-config/`
- ✅ Microservicios con su propia documentación

### Organizado
- ✅ Estructura clara y lógica
- ✅ Cada carpeta con su README
- ✅ Archivos agrupados por función

## 📝 Notas

- Los archivos `.env` y certificados no se suben a git (ver `.gitignore`)
- `config.py` y `Dockerfile-oficial-superset` son solo referencias
- El archivo usado es `superset_config.py`, no `config.py`
- Todos los docker-compose apuntan a `superset-config/Dockerfile`
