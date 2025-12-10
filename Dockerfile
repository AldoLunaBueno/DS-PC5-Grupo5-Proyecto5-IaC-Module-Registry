# Etapa 1: Builder
FROM python:3.10-slim AS builder

# Evita archivos .pyc y buffers en logs
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

RUN apt-get update && apt-get install -y --no-install-recommends gcc

COPY requirements.txt .
RUN pip install --user --no-cache-dir -r requirements.txt

# Etapa 2: Runtime
FROM python:3.10-slim

WORKDIR /app

RUN apt-get update && apt-get install -y --no-install-recommends curl && \
    rm -rf /var/lib/apt/lists/*

# Creamos un grupo y un usuario del sistema sin password
RUN groupadd -r appuser && useradd -r -g appuser appuser

# Copiar paquetes instalados desde la etapa 'builder'
COPY --from=builder /root/.local /home/appuser/.local

# Asegurar que los binarios instalados estén en el PATH
ENV PATH=/home/appuser/.local/bin:$PATH

# Copiar el código de la aplicación y asignar permisos al usuario no root
COPY --chown=appuser:appuser . .

# Verifica cada 30s si la app responde, si falla 3 veces la marca como unhealthy
HEALTHCHECK --interval=30s --timeout=30s --start-period=5s --retries=3 \
  CMD curl -f http://localhost:8000/health || exit 1

USER appuser

EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]