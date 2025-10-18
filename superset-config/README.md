# Configuración de Superset

Esta carpeta contiene los archivos de configuración y construcción de Superset.

## Archivos

### Dockerfile
Imagen Docker personalizada de Superset que incluye:
- PostgreSQL driver (psycopg2-binary)
- Oracle driver (oracledb)
- Locale español (es_ES.UTF-8)
- Paquetes adicionales: Authlib, openpyxl, Pillow

### superset_config.py
Configuración personalizada de Superset que sobrescribe los valores por defecto.
Incluye configuración de:
- Base de datos (PostgreSQL)
- Redis (caché y Celery)
- Celery (workers y beat)
- Feature flags
- Seguridad y autenticación

### config.py
Archivo de configuración base de Superset (referencia).
No se usa directamente, solo como referencia.

### Dockerfile-oficial-superset
Dockerfile oficial de Apache Superset (referencia).
Útil para comparar y entender la estructura oficial.

## Uso

Los archivos se referencian automáticamente en los docker-compose:
- `Dockerfile` se usa para construir la imagen
- `superset_config.py` se monta en `/app/pythonpath/superset_config.py`

## Personalización

Para personalizar Superset, edita `superset_config.py`.
Consulta la documentación oficial: https://superset.apache.org/docs/configuration/configuring-superset
