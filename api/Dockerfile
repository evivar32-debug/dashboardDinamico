FROM python:3.12-slim

# Evita archivos .pyc y permite ver logs en tiempo real
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

# Instalamos dependencias del sistema para PostgreSQL
# Se añade 'gcc' y 'pkg-config' para asegurar la compilación de psycopg2
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libpq-dev \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Actualizamos pip e instalamos requerimientos
COPY requirements.txt .
RUN pip install --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Copiamos el contenido de la carpeta /api al WORKDIR /app
COPY . .

EXPOSE 8000

# Usamos el servidor de desarrollo para esta etapa
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]