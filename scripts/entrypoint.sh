#!/bin/bash
set -e

echo "Waiting for database..."
while ! nc -z $MYSQL_HOST 3306; do
  sleep 1
done
echo "Database is up!"

echo "Starting entrypoint script..."

flask db upgrade

python3 -m flask --app app:create_app run --host=0.0.0.0
