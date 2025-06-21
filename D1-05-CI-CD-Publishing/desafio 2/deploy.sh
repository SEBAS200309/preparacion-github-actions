#!/bin/bash
# deploy.sh
ENVIRONMENT=$1
CONFIG_FILE="config/${ENVIRONMENT}.json"

if [ ! -f "$CONFIG_FILE" ]; then
    echo "Error: Configuration file for $ENVIRONMENT not found"
    exit 1
fi

echo "Deploying to $ENVIRONMENT environment..."
echo "Using configuration: $CONFIG_FILE"

# Simular despliegue
sleep 5

echo "Deployment to $ENVIRONMENT completed successfully!"