#!/usr/bin/env bash
# Exit on error
set -o errexit

echo "=== Starting Render Build ==="

# Upgrade pip
pip install --upgrade pip

# Install dependencies
echo "Installing dependencies..."
pip install -r requirements.txt

# Collect static files
echo "Collecting static files..."
python manage.py collectstatic --no-input

# Run migrations
echo "Running database migrations..."
python manage.py migrate --no-input

echo "=== Build Complete ==="
