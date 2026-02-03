#To get the envs
import os
#import time # Para los assets
# Para formato moneda.
from typing import Any, Callable, Literal, TYPE_CHECKING, TypedDict

# REVISAR CONFIGURACIÓN / USO REDIS.

# PARA TABLEROS PÚBLICOS.
# PUBLIC_ROLE_LIKE = "Gamma"  # or create a custom role
# AUTH_ROLE_PUBLIC = "Public"

# Allow unauthenticated access
# GUEST_ROLE_NAME = "Gamma"  # or "Public"
# GUEST_TOKEN_JWT_SECRET = "your-secret-key-here"  # Generate a secure key
# GUEST_TOKEN_JWT_ALGO = "HS256"
# GUEST_TOKEN_HEADER_NAME = "X-Guest-Token"

# CSRF settings for public access (be careful with this in production)
#WTF_CSRF_ENABLED = False  # Or True with proper exemptions

# Enable dashboard embedding
#ENABLE_EMBEDDED_SUPERSET = True

# CORS settings for embedded dashboards
#ENABLE_CORS = True

# CORS_OPTIONS = {
#     'supports_credentials': True,
#     'allow_headers': ['*'],
#     'resources': ['*'],
#     'origins': ['*']  # Restrict this in production!
# }

################################################################################

# LIMPIAR
# Cache-busting version NO FUNCIONA.
#CACHE_BUST_VERSION = int(time.time())

# LIMPIAR
#FAVICONS = [{"href": f"/static/assets/images/favicon.png?v={CACHE_BUST_VERSION}", "type": "image/png"}]

# LIMPIAR
# THEME = {
#     "token": {
#         "brandLogoUrl": f"/static/assets/images/superset_logo_horiz.png?v={CACHE_BUST_VERSION}",
#         "brandLogoHref": "/",
#         "brandLogoTooltip": "PBA",
#         "brandSpinnerUrl": f"/static/assets/images/loading.gif?v={CACHE_BUST_VERSION}"
#     }
# }

FAVICONS = [{"href": "/static/assets/images/favicon.png", "type": "image/png"}]

# lIMPIAR
# THEME_DEFAULT = {
#     # Other theme configurations can go here
#     "brandSpinnerUrl": "/static/assets/images/loading.gif",
# }

THEME = {
    "token": {
        "brandLogoUrl": "/static/assets/images/superset_logo_horiz.png", # Path to your logo
        "brandLogoHref": "/", # Optional: URL to redirect to when the logo is clicked (e.g., home page)
        "brandLogoTooltip": "Tableros PBA", # Optional: Tooltip text
        "brandSpinnerUrl": "/static/assets/images/loading.gif"
    }
}

# Force disable browser cache for static assets
SEND_FILE_MAX_AGE_DEFAULT = 0

# superset_config.py
# lIMPIAR
#SQLALCHEMY_DATABASE_URI = '${DATABASE_DIALECT}://${DATABASE_PASSWORD}:${DATABASE_USER}@${DATABASE_HOST}:${DATABASE_PORT}/${DATABASE_DB}'
SQLALCHEMY_DATABASE_URI = os.getenv("SUPERSET_DATABASE_URI")



# REVISAR
# class D3Format(TypedDict, total=False):
#     decimal: str
#     thousands: str
#     grouping: list[int]
#     currency: list[str]

# D3_FORMAT: D3Format = {
#      "decimal": ",",           # - decimal place string (e.g., ".").
#      "thousands": ".",         # - group separator string (e.g., ",").
#      "grouping": [3],          # - array of group sizes (e.g., [3]), cycled as needed.
#      "currency": ["u$", ""]    # - currency prefix/suffix strings (e.g., ["$", ""])
# }

BABEL_DEFAULT_LOCALE = "es"

BABEL_DEFAULT_FOLDER = "superset/translations"

LANGUAGES = {
    "es": {"flag": "es", "name": "Spanish"},
    'en': {'flag': 'us', 'name': 'English'},
}

# REVISAR
# SUPERSET_D3_LOCALE = """
# {
#   "decimal": ",",
#   "thousands": ".",
#   "grouping": [3],
#   "currency": ["$", ""],
#   "dateTime": "%a %e %b %X %Y",
#   "date": "%d/%m/%Y",
#   "time": "%H:%M:%S",
#   "periods": ["AM", "PM"],
#   "days": ["Domingo", "Lunes", "Martes", "Miércoles", "Jueves", "Viernes", "Sábado"],
#   "shortDays": ["Dom", "Lun", "Mar", "Mié", "Jue", "Vie", "Sáb"],
#   "months": ["Enero", "Febrero", "Marzo", "Abril", "Mayo", "Junio", "Julio", "Agosto", "Septiembre", "Octubre", "Noviembre", "Diciembre"],
#   "shortMonths": ["Ene", "Feb", "Mar", "Abr", "May", "Jun", "Jul", "Ago", "Sep", "UFA", "Nov", "Dic"]
# } """

# REVISAR
#Agrego Variables  a pedido de luna  pantillas sql jinja
#ENABLE_TEMPLATE_PROCESSING: true

FEATURE_FLAGS = {
    'ENABLE_JAVASCRIPT_CONTROLS': True,
    'ENABLE_TEMPLATE_PROCESSING': True,
    'EMBEDDED_SUPERSET': True,
    "PUBLIC_ROLE_LIKE_GAMMA": True,
    "DASHBOARD_RBAC": True,
}

TALISMAN_CONFIG = {
    "content_security_policy": {
        "base-uri": ["'self'"],
        "default-src": ["'self'"],
        "img-src": [
            "'self'",
            "blob:",
            "data:",
            "https://apachesuperset.gateway.scarf.sh",
            "https://static.scarf.sh/",
            # "https://cdn.brandfolder.io", # Uncomment when SLACK_ENABLE_AVATARS is True  # noqa: E501
            "ows.terrestris.de",
        ],
        "worker-src": ["'self'", "blob:"],
        "connect-src": [
            "'self'",
            "https://api.mapbox.com",
            "https://events.mapbox.com",
        ],
        "object-src": "'none'",
        "style-src": [
            "'self'",
            "'unsafe-inline'",
        ],
        "script-src": ["'self'", "'strict-dynamic'", "'unsafe-eval'"],
    },
    "content_security_policy_nonce_in": ["script-src"],
    "force_https": False,
    "session_cookie_secure": False,
}

MAPBOX_API_KEY = "pk.eyJ1IjoiZGF0b3NlYyIsImEiOiJjbWJyeXkzMTAwZzQzMm1weDlyZzZ1Y21hIn0.niXWgE2weTFlgPrcP7xn7w"

# THEME_DEFAULT = {
#     "token": {
#         "brandLogoAlt": "Tableros PBA",  # This changes the browser title/alt text
#     }
# }