#!/bin/bash
set -e

APP_VERSION=$(grep -oP 'version\s*=\s*"\K[^"]+' pyproject.toml)

echo "BUILDING DOCKER IMAGE..."
docker build -t "superlists:$APP_VERSION" -t "superlists:latest" .
echo "FINISHED BUILDING IMAGE"

echo "STARTING CONTAINER..."
docker run \
    --name app \
    -p 8888:8888 \
    --mount type=bind,source=./src/db.sqlite3,target=/src/db.sqlite3 \
    -e DJANGO_SECRET_KEY="secret" \
    -e DJANGO_ALLOWED_HOST="localhost" \
    -it superlists
