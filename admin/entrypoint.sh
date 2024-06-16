#!/bin/sh

echo "Starting entrypoint.sh..."

# Instalando dependencias
apk add --no-cache gcc musl-dev libffi-dev openssl-dev

# Instalando poetry
pip install poetry==1.6.1

# Instalando dependencias del proyecto
poetry install

# Creando base de datos
poetry run flask resetdb

# Instanciando datos iniciales
poetry run flask seedsdb

echo "Finish entrypoint.sh..."

# Ejecuta el comando final
exec "$@"