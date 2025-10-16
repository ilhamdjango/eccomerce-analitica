# #!/usr/bin/env sh
# set -e

# echo "=== Starting entrypoint ==="

# # --- DB host təyini ---
# export DB_HOST=${CLOUD_SQL_CONNECTION_NAME:+/cloudsql/$CLOUD_SQL_CONNECTION_NAME}
# export DB_USER=${DB_USER:-ecommerce_user}
# export DB_NAME=${DB_NAME:-ecommerce_db}
# export DB_PASSWORD=${DB_PASSWORD:-12345}
# export DB_PORT=${DB_PORT:-5432}

# echo "Using Postgres:"
# echo "  Host: $DB_HOST"
# echo "  Port: $DB_PORT"
# echo "  DB: $DB_NAME"
# echo "  User: $DB_USER"

# # --- Django Migrate və Static files ---
# echo "Running Django migrations..."
# python manage.py migrate --noinput

# echo "Collecting static files..."
# python manage.py collectstatic --noinput --clear

# # --- Optional: Superuser yaratmaq ---
# echo "Creating superuser if not exists..."
# python manage.py shell -c "
# from django.contrib.auth import get_user_model
# User = get_user_model()
# if not User.objects.filter(username='admin').exists():
#     User.objects.create_superuser('admin','admin@example.com','admin')
# "

# # --- Gunicorn serverini işə sal ---
# echo "Starting Gunicorn on 0.0.0.0:${PORT:-8080}..."
# exec gunicorn config.wsgi:application \
#     --bind 0.0.0.0:${PORT:-8080} \
#     --workers 2 \
#     --threads 2 \
#     --timeout 0 \
#     --access-logfile - \
#     --error-logfile -


#!/usr/bin/env sh
set -e

echo "Starting entrypoint..."

# Determine if running on Cloud Run
if [ "$RUNNING_ON_CLOUDRUN" = "true" ]; then
  echo "Detected Cloud Run environment. Using Cloud SQL socket..."
  export POSTGRES_HOST="/cloudsql/${CLOUD_SQL_CONNECTION_NAME}"
else
  echo "Local environment detected. Using standard host..."
fi

# Wait for Postgres
if [ -n "$POSTGRES_HOST" ]; then
  echo "Waiting for Postgres at $POSTGRES_HOST:${POSTGRES_PORT:-5432}..."
  for i in $(seq 1 30); do
    if pg_isready -h "$POSTGRES_HOST" -p "${POSTGRES_PORT:-5432}" -U "$POSTGRES_USER" -d "$POSTGRES_DB"; then
      echo "Postgres is ready!"
      break
    fi
    echo "Postgres not ready yet, retry $i/30"
    sleep 2
  done
  if ! pg_isready -h "$POSTGRES_HOST" -p "${POSTGRES_PORT:-5432}" -U "$POSTGRES_USER" -d "$POSTGRES_DB"; then
    echo "ERROR: Postgres never became ready. Exiting."
    exit 1
  fi
fi

# # Apply migrations
# echo "Running migrations..."
# python manage.py migrate --noinput || { echo "Migration failed!"; exit 1; }

# # Create superuser if not exists
# echo "Checking for superuser..."
# python manage.py shell -c "from django.contrib.auth import get_user_model; User = get_user_model(); User.objects.create_superuser('admin','admin@example.com','admin') if not User.objects.filter(username='admin').exists() else None"

# # Collect static files
# echo "Collecting static files..."
# python manage.py collectstatic --noinput --clear || { echo "Collectstatic failed!"; exit 1; }

# Start Gunicorn
echo "Starting Gunicorn on 0.0.0.0:$PORT"
exec gunicorn shop_service.wsgi:application --bind 0.0.0.0:$PORT --access-logfile - --error-logfile -
