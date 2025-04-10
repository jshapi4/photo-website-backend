#!/usr/bin/env bash

# Exit on error
set -o errexit

# Create a Python virtual environment if it doesn't exist
if [ ! -d ".venv" ]; then
    echo "Creating Python virtual environment..."
    python -m venv .venv
fi

# Activate the virtual environment
source .venv/bin/activate

# Install dependencies
echo "Installing dependencies..."
pip install --upgrade pip
pip install -r requirements.txt

# Run migrations
echo "Running migrations..."
python manage.py migrate

# Collect static files
echo "Collecting static files..."
python manage.py collectstatic --no-input

# Create a superuser automatically if DJANGO_SUPERUSER_* env variables are set
if [[ -n "$DJANGO_SUPERUSER_USERNAME" && -n "$DJANGO_SUPERUSER_EMAIL" && -n "$DJANGO_SUPERUSER_PASSWORD" ]]; then
    echo "Creating superuser..."
    python manage.py createsuperuser --noinput
fi