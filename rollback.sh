#!/bin/bash

# Configuration
APP_NAME="ml-service-v3"
STABLE_IMAGE="ml-model:stable"

echo "Rollback sequence initiated..."
echo "Stopping current failed container..."
docker stop $APP_NAME || true
docker rm $APP_NAME || true

echo "Checking for stable image..."
if [[ "$(docker images -q $STABLE_IMAGE 2> /dev/null)" == "" ]]; then
    echo "ERROR: Stable image not found. Cannot rollback."
    exit 1
fi

echo "Restarting with stable image: $STABLE_IMAGE"
docker run -d --name $APP_NAME -p 5000:5000 $STABLE_IMAGE

echo "Rollback successful. System restored to stable state."