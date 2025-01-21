#!/bin/bash
set -e

APP_VERSION=$(grep -oP 'version\s*=\s*"\K[^"]+' pyproject.toml)

echo "BUILDING DOCKER IMAGE..."
docker build -t "superlists:$APP_VERSION" -t "superlists:latest" .
echo "FINISHED BUILDING IMAGE"

cleanup() {
    echo "REMOVING IMAGES..."
    docker rmi "superlists:latest" "superlists:$APP_VERSION"
    echo "SUCCESSFULLY REMOVED IMAGES"
}

# Will remove images after exiting the container with ^C too
trap cleanup EXIT

echo "STARTING CONTAINER..."
docker run --rm \
    --name app \
    -p 8888:8888 \
    --mount type=bind,source=./src/db.sqlite3,target=/src/db.sqlite3 \
    -e DJANGO_SECRET_KEY="secret" \
    -e DJANGO_ALLOWED_HOST="localhost" \
    -it superlists
