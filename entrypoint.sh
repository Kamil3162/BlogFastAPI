#!/bin/bash
# entrypoint.sh

# Wait for postgres to be ready
echo "Waiting for postgres..."
#while ! nc -z postgres 5432; do
 # sleep 0.1
#done
sleep 1.0
echo "PostgreSQL started"

# Run migrations
echo "Running migrations"
alembic upgrade head

# Start application
echo "Starting application"
uvicorn app.main:app --host 0.0.0.0 --port 8000
