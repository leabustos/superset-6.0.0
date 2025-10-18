FROM apache/superset:6.0.0rc2
USER root

# Install system dependencies
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    locales \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Configure Spanish locale
RUN localedef -i es_ES -c -f UTF-8 -A /usr/share/locale/locale.alias es_ES.UTF-8
ENV LANG=es_ES.UTF-8

# Install Python packages in the virtual environment
RUN . /app/.venv/bin/activate && \
    uv pip install --no-cache \
    psycopg2-binary \
    oracledb \
    Authlib \
    openpyxl \
    Pillow

# Switch back to superset user for security
USER superset

CMD ["/app/docker/docker-bootstrap.sh", "app-gunicorn"]
