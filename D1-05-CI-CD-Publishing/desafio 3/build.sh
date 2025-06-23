#!/bin/bash
# build.sh
echo "Building application..."
mkdir -p dist

# Simular proceso de build
echo "console.log('Hello from built app!');" > dist/app.js
echo "Build completed successfully!"

# Crear archivo de versión
echo "v$(date +%Y%m%d-%H%M%S)" > dist/version.txt