#!/usr/bin/env sh
set -e

echo "=== Starting entrypoint ==="

# --- DB host təyini ---
export DB_HOST=${CLOUD_SQL_CONNECTION_NAME:+/cloudsql/$CLOUD_SQL_CONNECTION_NAME}
export DB_USER=${DB_USER:-ecommerce_user}
export DB_NAME=${DB_NAME:-ecommerce_db}
export DB_PASSWORD=${DB_PASSWORD:-12345}
export DB_PORT=${DB_PORT:-5432}

echo "Using Postgres:"
echo "  Host: $DB_HOST"
echo "  Port: $DB_PORT"
echo "  DB: $DB_NAME"
echo "  User: $DB_USER"

# # --- Django Migrate və Static files ---
echo "Running Django migrations..."
python manage.py migrate --noinput

# echo "Collecting static files..."
python manage.py collectstatic --noinput --clear

# # --- Optional: Superuser yaratmaq ---
echo "Creating superuser if not exists..."
python manage.py shell -c "
from django.contrib.auth import get_user_model
User = get_user_model()
if not User.objects.filter(username='admin').exists():
    User.objects.create_superuser('admin','admin@example.com','admin')
"

# --- Gunicorn serverini işə sal ---
echo "Starting Gunicorn on 0.0.0.0:${PORT:-8080}..."
exec gunicorn config.wsgi:application \
    --bind 0.0.0.0:${PORT:-8080} \
    --workers 2 \
    --threads 2 \
    --timeout 0 \
    --access-logfile - \
    --error-logfile -

 #
