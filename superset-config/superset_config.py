# ============================================
# SUPERSET CONFIGURATION FILE
# ============================================
# Este archivo contiene la configuración personalizada de Superset
# Sobrescribe los valores por defecto de config.py
#
# Documentación oficial:
# https://superset.apache.org/docs/configuration/configuring-superset

import os
from datetime import timedelta
from typing import Optional
from celery.schedules import crontab

# ============================================
# SEGURIDAD
# ============================================

# Clave secreta para firmar sesiones y tokens
# IMPORTANTE: Cambiar en producción usando una clave generada con:
# openssl rand -base64 42
SECRET_KEY = os.environ.get("SECRET_KEY", "CHANGE_ME_TO_A_COMPLEX_RANDOM_SECRET_KEY")

# Validar que se haya configurado una clave secreta
if SECRET_KEY == "CHANGE_ME_TO_A_COMPLEX_RANDOM_SECRET_KEY":
    raise ValueError(
        "Por favor configura SECRET_KEY en el archivo .env con una clave segura. "
        "Genera una con: openssl rand -base64 42"
    )

# ============================================
# BASE DE DATOS
# ============================================

# Configuración de la base de datos principal (metadatos de Superset)
SQLALCHEMY_DATABASE_URI = (
    f"postgresql+psycopg2://"
    f"{os.environ.get('DATABASE_USER', 'superset')}:"
    f"{os.environ.get('DATABASE_PASSWORD', 'superset')}@"
    f"{os.environ.get('DATABASE_HOST', 'db')}:"
    f"{os.environ.get('DATABASE_PORT', '5432')}/"
    f"{os.environ.get('DATABASE_DB', 'superset')}"
)

# Pool de conexiones
SQLALCHEMY_ENGINE_OPTIONS = {
    "pool_size": 10,
    "pool_recycle": 3600,
    "pool_pre_ping": True,
    "max_overflow": 20,
    "connect_args": {
        "connect_timeout": 10,
    }
}

# Deshabilitar tracking de modificaciones (mejora performance)
SQLALCHEMY_TRACK_MODIFICATIONS = False

# ============================================
# REDIS - CACHÉ
# ============================================

# Configuración de caché con Redis
REDIS_HOST = os.environ.get("REDIS_HOST", "redis")
REDIS_PORT = os.environ.get("REDIS_PORT", "6379")
REDIS_DB = os.environ.get("REDIS_DB", "0")

# Caché para objetos de Superset (dashboards, charts, etc.)
CACHE_CONFIG = {
    "CACHE_TYPE": "RedisCache",
    "CACHE_DEFAULT_TIMEOUT": int(timedelta(days=1).total_seconds()),
    "CACHE_KEY_PREFIX": "superset_",
    "CACHE_REDIS_HOST": REDIS_HOST,
    "CACHE_REDIS_PORT": REDIS_PORT,
    "CACHE_REDIS_DB": REDIS_DB,
}

# Caché para resultados de queries
DATA_CACHE_CONFIG = {
    "CACHE_TYPE": "RedisCache",
    "CACHE_DEFAULT_TIMEOUT": int(timedelta(hours=1).total_seconds()),
    "CACHE_KEY_PREFIX": "superset_data_",
    "CACHE_REDIS_HOST": REDIS_HOST,
    "CACHE_REDIS_PORT": REDIS_PORT,
    "CACHE_REDIS_DB": REDIS_DB,
}

# Caché para thumbnails de dashboards
THUMBNAIL_CACHE_CONFIG = {
    "CACHE_TYPE": "RedisCache",
    "CACHE_DEFAULT_TIMEOUT": int(timedelta(days=7).total_seconds()),
    "CACHE_KEY_PREFIX": "superset_thumbnail_",
    "CACHE_REDIS_HOST": REDIS_HOST,
    "CACHE_REDIS_PORT": REDIS_PORT,
    "CACHE_REDIS_DB": REDIS_DB,
}

# ============================================
# CELERY - TAREAS ASÍNCRONAS
# ============================================

REDIS_CELERY_DB = os.environ.get("REDIS_CELERY_DB", "1")
REDIS_RESULTS_DB = os.environ.get("REDIS_RESULTS_DB", "2")


class CeleryConfig:
    broker_url = f"redis://{REDIS_HOST}:{REDIS_PORT}/{REDIS_CELERY_DB}"
    result_backend = f"redis://{REDIS_HOST}:{REDIS_PORT}/{REDIS_RESULTS_DB}"
    
    # Importar tareas
    imports = (
        "superset.sql_lab",
        "superset.tasks.scheduler",
        "superset.tasks.thumbnails",
        "superset.tasks.cache",
    )
    
    # Configuración de workers
    worker_prefetch_multiplier = 1
    task_acks_late = True
    task_reject_on_worker_lost = True
    
    # Timeouts
    broker_transport_options = {
        "visibility_timeout": int(timedelta(hours=1).total_seconds()),
        "socket_keepalive": True,
    }
    
    # Serialización
    task_serializer = "json"
    result_serializer = "json"
    accept_content = ["json"]
    timezone = "UTC"
    enable_utc = True
    
    # Rate limiting para SQL Lab
    task_annotations = {
        "sql_lab.get_sql_results": {
            "rate_limit": "100/s",
        },
    }
    
    # Tareas programadas
    beat_schedule = {
        "reports.scheduler": {
            "task": "reports.scheduler",
            "schedule": crontab(minute="*", hour="*"),
        },
        "reports.prune_log": {
            "task": "reports.prune_log",
            "schedule": crontab(minute=0, hour=0),
        },
    }


CELERY_CONFIG = CeleryConfig

# ============================================
# CONFIGURACIÓN DE SUPERSET
# ============================================

# Nombre de la aplicación
APP_NAME = "Superset"

# Ícono de la aplicación
APP_ICON = "/static/assets/images/superset-logo-horiz.png"

# Límites de filas
ROW_LIMIT = int(os.environ.get("ROW_LIMIT", "50000"))
SAMPLES_ROW_LIMIT = 1000
DISPLAY_MAX_ROW = 10000

# Límites de SQL Lab
DEFAULT_SQLLAB_LIMIT = 1000
SQLLAB_TIMEOUT = int(os.environ.get("SQLLAB_TIMEOUT", "300"))
SQLLAB_ASYNC_TIME_LIMIT_SEC = int(
    os.environ.get("SQLLAB_ASYNC_TIME_LIMIT_SEC", "21600")
)

# Timeout del servidor web
SUPERSET_WEBSERVER_TIMEOUT = int(timedelta(minutes=5).total_seconds())

# ============================================
# FEATURES FLAGS
# ============================================

FEATURE_FLAGS = {
    # Habilitar alertas y reportes
    "ALERT_REPORTS": os.environ.get("SUPERSET_FEATURE_ALERT_REPORTS", "false").lower() == "true",
    
    # Habilitar thumbnails de dashboards
    "THUMBNAILS": os.environ.get("SUPERSET_FEATURE_THUMBNAILS", "false").lower() == "true",
    
    # Habilitar queries asíncronas globales
    "GLOBAL_ASYNC_QUERIES": os.environ.get("SUPERSET_FEATURE_GLOBAL_ASYNC_QUERIES", "false").lower() == "true",
    
    # Habilitar SQL Lab backend persistence
    "SQLLAB_BACKEND_PERSISTENCE": True,
    
    # Habilitar dashboard native filters
    "DASHBOARD_NATIVE_FILTERS": True,
    
    # Habilitar dashboard cross filters
    "DASHBOARD_CROSS_FILTERS": True,
    
    # Habilitar embeddable charts
    "EMBEDDABLE_CHARTS": True,
    
    # Habilitar drill to detail
    "DRILL_TO_DETAIL": True,
    
    # Habilitar drill by
    "DRILL_BY": True,
    
    # Habilitar tagging system
    "TAGGING_SYSTEM": False,
    
    # Habilitar dashboard RBAC
    "DASHBOARD_RBAC": False,
    
    # Habilitar SSH tunneling
    "SSH_TUNNELING": False,
}

# ============================================
# SEGURIDAD Y CORS
# ============================================

# Habilitar CORS
ENABLE_CORS = True
CORS_OPTIONS = {
    "supports_credentials": True,
    "allow_headers": ["*"],
    "resources": ["*"],
    "origins": ["*"],  # En producción, especificar dominios permitidos
}

# Deshabilitar Talisman en desarrollo
# En producción, habilitar y configurar apropiadamente
TALISMAN_ENABLED = os.environ.get("SUPERSET_ENV", "development") == "production"

# Configuración de cookies de sesión
SESSION_COOKIE_HTTPONLY = True
SESSION_COOKIE_SECURE = False  # Cambiar a True en producción con HTTPS
SESSION_COOKIE_SAMESITE = "Lax"

# ============================================
# AUTENTICACIÓN
# ============================================

# Tipo de autenticación (DB por defecto)
from flask_appbuilder.security.manager import AUTH_DB
AUTH_TYPE = AUTH_DB

# Permitir auto-registro de usuarios (deshabilitado por defecto)
AUTH_USER_REGISTRATION = False

# Rol por defecto para nuevos usuarios
AUTH_USER_REGISTRATION_ROLE = "Public"

# ============================================
# LOGGING
# ============================================

# Nivel de log
import logging

LOG_LEVEL = logging.INFO
if os.environ.get("FLASK_DEBUG", "false").lower() == "true":
    LOG_LEVEL = logging.DEBUG

# Formato de log
LOG_FORMAT = "%(asctime)s:%(levelname)s:%(name)s:%(message)s"

# Habilitar logs de eventos en la base de datos
from superset.utils.log import DBEventLogger
EVENT_LOGGER = DBEventLogger()

# ============================================
# EMAIL (SMTP)
# ============================================

# Configuración de SMTP para alertas y reportes
SMTP_HOST = os.environ.get("SMTP_HOST", "localhost")
SMTP_STARTTLS = os.environ.get("SMTP_STARTTLS", "true").lower() == "true"
SMTP_SSL = os.environ.get("SMTP_SSL", "false").lower() == "true"
SMTP_USER = os.environ.get("SMTP_USER", "superset")
SMTP_PORT = int(os.environ.get("SMTP_PORT", "25"))
SMTP_PASSWORD = os.environ.get("SMTP_PASSWORD", "")
SMTP_MAIL_FROM = os.environ.get("SMTP_MAIL_FROM", "superset@superset.local")

# ============================================
# MAPBOX
# ============================================

# API Key para visualizaciones de mapas
MAPBOX_API_KEY = os.environ.get("MAPBOX_API_KEY", "")

# ============================================
# WEBDRIVER (para screenshots y reportes)
# ============================================

# Tipo de webdriver (firefox o chrome)
WEBDRIVER_TYPE = "firefox"

# URL base para acceder a Superset
WEBDRIVER_BASEURL = "http://superset:8088/"

# Configuración de ventana para screenshots
WEBDRIVER_WINDOW = {
    "dashboard": (1600, 2000),
    "slice": (3000, 1200),
}

# ============================================
# CONFIGURACIÓN ADICIONAL
# ============================================

# Habilitar proxy fix (si está detrás de un proxy/load balancer)
ENABLE_PROXY_FIX = True
PROXY_FIX_CONFIG = {
    "x_for": 1,
    "x_proto": 1,
    "x_host": 1,
    "x_port": 1,
    "x_prefix": 1,
}

# Deshabilitar rate limiting en desarrollo
RATELIMIT_ENABLED = os.environ.get("SUPERSET_ENV", "development") == "production"

# Idioma por defecto
BABEL_DEFAULT_LOCALE = "en"

# Zona horaria por defecto
DEFAULT_TIME_ZONE = "UTC"

# ============================================
# CONFIGURACIÓN DE DESARROLLO
# ============================================

# Modo debug (solo desarrollo)
DEBUG = os.environ.get("FLASK_DEBUG", "false").lower() == "true"

# Mostrar stacktraces en errores (solo desarrollo)
SHOW_STACKTRACE = DEBUG

# Habilitar profiling (solo desarrollo)
PROFILING = False

# ============================================
# MENSAJE DE INICIO
# ============================================

if __name__ != "__main__":
    print("=" * 60)
    print("Superset Configuration Loaded")
    print("=" * 60)
    print(f"Environment: {os.environ.get('SUPERSET_ENV', 'development')}")
    print(f"Debug Mode: {DEBUG}")
    print(f"Database: {SQLALCHEMY_DATABASE_URI.split('@')[1] if '@' in SQLALCHEMY_DATABASE_URI else 'N/A'}")
    print(f"Redis: {REDIS_HOST}:{REDIS_PORT}")
    print("=" * 60)