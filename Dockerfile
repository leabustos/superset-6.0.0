# Use the official Superset 5.0.0 image as the base
#FROM apache/superset:5.0.0

# Switch to the root user to install system dependencies
#USER root

# Install build essentials and PostgreSQL development libraries required for psycopg2
#RUN apt-get update && \
#    apt-get install -y --no-install-recommends \
#    gcc \
#    libpq-dev \
#    python3-dev \
#    pkg-config && \
#    rm -rf /var/lib/apt/lists/*

# Switch back to the Superset user
#USER superset

# Install psycopg2-binary using uv within the Superset virtual environment
# Superset 5.0.0 uses uv as the package manager
#RUN . /app/.venv/bin/activate && \
#    uv pip install psycopg2-binary

# change this to apache/superset:5.0.0 or whatever version you want to build from;
# otherwise the default is the latest commit on GitHub master branch
# FROM apache/superset:5.0.0

# ARG BUILD_TRANSLATIONS=true

# USER root

# # Set environment variable for Playwright
# ENV PLAYWRIGHT_BROWSERS_PATH=/usr/local/share/playwright-browsers

# # 1. Install system build dependencies
# RUN apt-get update && \
#     apt-get install -y --no-install-recommends \
#     gcc \
#     libpq-dev && \
#     rm -rf /var/lib/apt/lists/* && \
#     pip install --no-cache-dir --upgrade uv && \
#     # Install packages using uv into the virtual environment
#     . /app/.venv/bin/activate && \
#     uv pip install \
#     #RUN pip install \
#     # install psycopg2 for using PostgreSQL metadata store - could be a MySQL package if using that backend:
#     psycopg2-binary \
#     # install db2 driver:
#     #ibm_db \
#     #ibm_db_sda \
#     # add the driver(s) for your data warehouse(s), in this example oracle:
#     pymssql \
#     # package needed for using single-sign on authentication:
#     Authlib \
#     # openpyxl to be able to upload Excel files
#     openpyxl \
#     # Pillow for Alerts & Reports to generate PDFs of dashboards
#     Pillow \
#     # install Playwright for taking screenshots for Alerts & Reports. This assumes the feature flag PLAYWRIGHT_REPORTS_AND_THUMBNAILS is enabled
#     # That feature flag will default to True starting in 6.0.0
#     # Playwright works only with Chrome.
#     # If you are still using Selenium instead of Playwright, you would instead install here the selenium package and a headless browser & webdriver
#     playwright \
#     #for superset cors to public dashboards
#     flask-cors \ 
#     && playwright install-deps \
#     && PLAYWRIGHT_BROWSERS_PATH=/usr/local/share/playwright-browsers playwright install chromium

# #COPY superset_config.py /app/pythonpath/superset_config.py \
# #     messages.po /app/superset/translations/es/LC_MESSAGES/messages.po \
# #     public_init.py /app/public_init.py \
# #LOGOS
# #     /assets/loading_pba_TEXT.gif /app/superset/static/assets/images/loading.gif \
# #     /assets/pba-logo-horiz.png /app/superset/static/assets/images/favicon.png \
# #    /assets/pba-logo-horiz.png /app/superset/static/assets/images/superset-logo-horiz.png

# # Single COPY for all files
# COPY ./custom/ /custom/

# RUN \
#   # Move config files
#   cp /custom/superset_config.py /app/pythonpath/superset_config.py && \
#   cp /custom/messages.po        /app/superset/translations/es/LC_MESSAGES/messages.po &&  \
#   cp /custom/public_init.py     /app/public_init.py &&  \
#   # Copy assets
#   cp /custom/loading.gif /app/superset/static/assets/images/loading.gif && \
#   cp /custom/logo.png    /app/superset/static/assets/images/favicon.png && \
#   cp /custom/logo.png    /app/superset/static/assets/images/superset-logo-horiz.png && \
#   chmod +x /app/public_init.py

# # Switch back to the superset user
# USER superset

# # Run the initialization after superset init
# CMD ["/app/docker/entrypoints/run-server.sh"]
FROM apache/superset:5.0.0

ARG BUILD_TRANSLATIONS=true

USER root

# Variabel de entorno para Playwright
ENV PLAYWRIGHT_BROWSERS_PATH=/usr/local/share/playwright-browsers

# ----- CAPA 1: Dependencias -----
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    gcc \
    libpq-dev && \
    rm -rf /var/lib/apt/lists/*

# ----- CAPA 2: Python packages -----
# Use the full path to pip and uv to avoid source activation complexity
RUN pip install --no-cache-dir --upgrade uv && \
    uv pip install \
    # install psycopg2 for using PostgreSQL metadata store - could be a MySQL package if using that backend:
    psycopg2-binary \
    # install db2 driver:
    #ibm_db \
    #ibm_db_sda \
    # add the driver(s) for your data warehouse(s), in this example oracle:
    pymssql \
    # package needed for using single-sign on authentication:
    Authlib \
    # openpyxl to be able to upload Excel files
    openpyxl \
    # Pillow for Alerts & Reports to generate PDFs of dashboards
    Pillow \
    # install Playwright for taking screenshots for Alerts & Reports. This assumes the feature flag PLAYWRIGHT_REPORTS_AND_THUMBNAILS is enabled
    # That feature flag will default to True starting in 6.0.0
    # Playwright works only with Chrome.
    # If you are still using Selenium instead of Playwright, you would instead install here the selenium package and a headless browser & webdriver
    playwright \
    #for superset cors to public dashboards
    flask-cors \ 
    && playwright install-deps \
    && PLAYWRIGHT_BROWSERS_PATH=/usr/local/share/playwright-browsers playwright install chromium

# ----- CAPA 3: Copia de archivos custom -----
COPY ./custom/ /custom/

# Se deben agregar a una carpeta /custom a la raíz principal del proyecto:
#   - loading.gif (animación de loading).
#   - favicon.png (logo para el navegador/marcador).
#   - logo-horiz.png (Logo para la UI de Superset).

RUN cp /custom/superset_config.py /app/pythonpath/superset_config.py && \
    cp /custom/messages.po /app/superset/translations/es/LC_MESSAGES/messages.po && \
    # cp /custom/public_init.py /app/public_init.py && \ # Para TABLEROS PÚBLICOS.
    #Borrar loading gif que dan problemas
    cp /custom/loading.gif /app/build/lib/superset/static/assets/loading.cff8a5da.gif && \
    cp /custom/loading.gif /app/superset/static/assets/loading.cff8a5da.gif && \
    cp /custom/loading.gif /app/.venv/lib/python3.10/site-packages/superset/static/assets/loading.cff8a5da.gif && \
    #Copy custom assets
    cp /custom/loading.gif /app/build/lib/superset/static/assets/images/loading.gif && \
    cp /custom/loading.gif /app/.venv/lib/python3.10/site-packages/superset/static/assets/images/loading.gif && \
    cp /custom/loading.gif /app/superset/static/assets/images/loading.gif && \
    cp /custom/favicon.png /app/superset/static/assets/images/favicon.png && \
    cp /custom/logo-horiz.png /app/superset/static/assets/images/superset-logo-horiz.png && \
    # chmod +x /app/public_init.py # Para TABLEROS PÚBLICOS.

# ----- FINAL: Cambio a Superset user para correr entrypoint -----
USER superset

CMD ["/app/docker/entrypoints/run-server.sh"]


# Variaciones a borrar

#RUN pip install \
# install psycopg2 for using PostgreSQL metadata store - could be a MySQL package if using that backend:
#    psycopg2-binary \
    # add the driver(s) for your data warehouse(s), oracle:
#    python-oracledb \
    # package needed for using single-sign on authentication:
#    Authlib \
    # openpyxl to be able to upload Excel files
#    openpyxl \
    # Pillow for Alerts & Reports to generate PDFs of dashboards
#    Pillow \
    # install Playwright for taking screenshots for Alerts & Reports. This assumes the feature flag PLAYWRIGHT_REPORTS_AND_THUMBNAILS is enabled
    # That feature flag will default to True starting in 6.0.0
    # Playwright works only with Chrome.
    # If you are still using Selenium instead of Playwright, you would instead install here the selenium package and a headless browser & webdriver
#    playwright \
    # Install Playwright dependencies and browser
#    RUN playwright install-deps && \
#    PLAYWRIGHT_BROWSERS_PATH=/usr/local/share/playwright-browsers playwright install chromium

# Install packages using uv into the virtual environment
#RUN uv pip install \
# install psycopg2 for using PostgreSQL metadata store - could be a MySQL package if using that backend:
#    psycopg2-binary \
    # add the driver(s) for your data warehouse(s), oracle:
#    python-oracledb \
    # package needed for using single-sign on authentication:
#    Authlib \
    # openpyxl to be able to upload Excel files
#    openpyxl \
    # Pillow for Alerts & Reports to generate PDFs of dashboards
#    Pillow \
    # install Playwright for taking screenshots for Alerts & Reports. This assumes the feature flag PLAYWRIGHT_REPORTS_AND_THUMBNAILS is enabled
    # That feature flag will default to True starting in 6.0.0
    # Playwright works only with Chrome.
    # If you are still using Selenium instead of Playwright, you would instead install here the selenium package and a headless browser & webdriver
#    playwright \
#    && playwright install-deps \
#    && PLAYWRIGHT_BROWSERS_PATH=/usr/local/share/playwright-browsers playwright install chromium
    
#RUN superset db upgrade

#RUN superset init

# Switch back to the superset user
#USER superset

#CMD ["/app/docker/entrypoints/run-server.sh"]

#FROM postgres:16
# Copy your SQL scripts into the image
#COPY ./docker/docker-entrypoint-initdb.d/ /docker-entrypoint-initdb.d/
# Set the execute permissions
#RUN chmod +x /docker-entrypoint-initdb.d/*.sql

#https://download.oracle.com/otn_software/linux/instantclient/2390000/instantclient-basic-linux.x64-23.9.0.25.07.zip

# Install the required locale
#RUN apt-get update && \
#    apt-get install -y locales && \
#    localedef -i es_ES -c -f UTF-8 -A /usr/share/locale/locale.alias es_ES.UTF-8

# Set default locale environment variables
#ENV LANG es_ES.UTF-8

# Argumento para versión del cliente Oracle
#ARG ORACLE_VERSION=instantclient_23_9

# Instalación de dependencias del sistema y Python
#RUN apt-get update && \
#    apt-get install --no-install-recommends -y \
#        wget unzip apt-utils libaio1 curl && \
#    pip install --no-cache-dir \
#        gevent psycopg2 redis watchdog cx_Oracle && \
#    apt-get clean && rm -rf /var/lib/apt/lists/*

# Instalación del cliente Oracle
# Copiar el ZIP ya descargado
#COPY extra/instantclient-basic-linux.x64-23.5.zip /oracle/

# Instalar Oracle Instant Client desde el ZIP
# RUN cd /oracle && \
#     unzip instantclient-basic-linux.x64-23.5.zip && \
#     rm instantclient-basic-linux.x64-23.5.zip && \
#     mkdir -p /oracle && \
#     ln -s /oracle/instantclient_23_5 /oracle/instantclient && \
#     ln -sf /oracle/instantclient/libclntsh.so.23.1 /oracle/instantclient/libclntsh.so && \
#     echo /oracle/instantclient > /etc/ld.so.conf.d/oracle-instantclient.conf && \
#     ldconfig
# ENV LD_LIBRARY_PATH=/oracle/instantclient \
#     ORACLE_HOME=/oracle/instantclient

# Configuración y recursos personalizados
#COPY -f config/images/bareos.png /app/superset/static/assets/images/bareos.png
#COPY -f config/images/loading.gif /app/superset/static/assets/images/loading.gif

# COPY docker/docker-init.sh /app/docker-init.sh
# RUN chmod +x /app/docker-init.sh
