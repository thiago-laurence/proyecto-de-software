#!/bin/sh

echo "Starting entrypoint.sh..."

# Creando base de datos
poetry run flask resetdb
# Instanciando datos iniciales
poetry run flask seedsdb

echo "Finish entrypoint.sh..."

# Ejecuta el comando final
exec "$@"