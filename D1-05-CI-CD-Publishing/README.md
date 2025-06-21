# Concepto a Resolver: CI/CD y Publishing en GitHub Actions

El concepto de CI/CD (Continuous Integration/Continuous Deployment) y Publishing se refiere a la automatización de procesos de construcción, pruebas, empaquetado y distribución de aplicaciones. En GitHub Actions, esto incluye la creación de artefactos, publicación en registros, despliegue a diferentes entornos y gestión de releases.

---

## Desafío 1: Construcción y Publicación de Artefactos Python

Crea un workflow que construya una aplicación Python, ejecute pruebas y publique los artefactos resultantes.

**Archivos a crear:**
- `.github/workflows/build-publish.yml`
- `app.py`
- `test_app.py`
- `requirements.txt`
- `setup.py`

**Contenido de ejemplo:**

```python
# app.py
def calcular_suma(a, b):
    return a + b

def calcular_producto(a, b):
    return a * b

if __name__ == "__main__":
    print("Calculadora básica")
    print(f"Suma: {calcular_suma(5, 3)}")
    print(f"Producto: {calcular_producto(5, 3)}")
```

```python
# test_app.py
import unittest
from app import calcular_suma, calcular_producto

class TestCalculadora(unittest.TestCase):
    def test_suma(self):
        self.assertEqual(calcular_suma(2, 3), 5)
        self.assertEqual(calcular_suma(-1, 1), 0)
    
    def test_producto(self):
        self.assertEqual(calcular_producto(4, 5), 20)
        self.assertEqual(calcular_producto(0, 10), 0)

if __name__ == '__main__':
    unittest.main()
```

```txt
# requirements.txt
pytest==7.4.0
setuptools==68.0.0
wheel==0.40.0
```


### Resultado Esperado:
- El workflow debe ejecutarse sin errores en push y pull request
- Las pruebas deben pasar correctamente
- Se debe generar un artefacto llamado "python-package" con los archivos de distribución
- El artefacto debe estar disponible para descarga en la pestaña Actions

---

## Desafío 2: Pipeline Multi-Stage con Environments

Implementa un pipeline que despliegue a múltiples entornos (staging y production) con aprobaciones manuales.

**Archivos a crear:**
- `.github/workflows/multi-stage-deploy.yml`
- `deploy.sh`
- `config/staging.json`
- `config/production.json`

**Contenido de ejemplo:**

```bash
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
```

```json
{
  "environment": "staging",
  "api_url": "https://api-staging.example.com",
  "database": "staging_db",
  "debug": true
}
```

### Resultado Esperado:
- El build debe completarse y generar artefactos
- El despliegue a staging debe ejecutarse automáticamente después del build
- El despliegue a production debe requerir aprobación manual
- Cada stage debe usar la configuración correcta del entorno

---

## Desafío 3: Publicación Automática de Releases

Crea un workflow que genere releases automáticos basados en tags semánticos y publique los artefactos.

**Archivos a crear:**
- `.github/workflows/release.yml`
- `package.json`
- `CHANGELOG.md`
- `build.sh`

**Contenido de ejemplo:**

```json
{
  "name": "my-app",
  "version": "1.0.0",
  "description": "Sample application for GitHub Actions",
  "main": "index.js",
  "scripts": {
    "build": "./build.sh",
    "test": "echo 'Tests passed'"
  },
  "author": "GitHub Actions Student",
  "license": "MIT"
}
```

```bash
#!/bin/bash
# build.sh
echo "Building application..."
mkdir -p dist

# Simular proceso de build
echo "console.log('Hello from built app!');" > dist/app.js
echo "Build completed successfully!"

# Crear archivo de versión
echo "v$(date +%Y%m%d-%H%M%S)" > dist/version.txt
```

### Resultado Esperado:
- El workflow debe activarse solo cuando se crea un tag que comience con 'v'
- Debe generar un build de la aplicación
- Debe crear un release en GitHub con notas generadas automáticamente
- Debe adjuntar los artefactos comprimidos al release

---

## Desafío 4: Resolución de Problemas - Pipeline de CI/CD Roto

**ESTE ES UN DESAFÍO DE DEBUGGING**: El siguiente workflow tiene múltiples errores que debes identificar y corregir.

**Archivos a crear:**
- `.github/workflows/broken-pipeline.yml` (con errores intencionales)
- `app.py`
- `requirements.txt`
- `Dockerfile`

**Contenido con errores:**

```yaml
# .github/workflows/broken-pipeline.yml (CONTIENE ERRORES)
name: Broken CI/CD Pipeline

on:
  push:
    branchs: [ main, develop ]  # Error 1: typo en "branches"
  pull_request:
    branches: [ main ]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      
      - name: Setup Python
        uses: actions/setup-python@v4
        with:
          python-version: 3.9  # Error 2: falta comillas en la versión
      
      - name: Install dependencies
        run: |
          python -m pip install --upgrade pip
          pip install -r requirements.txt
      
      - name: Run tests
        run: python -m pytest tests/ --verbose
        
  build:
    needs: test
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      
      - name: Build Docker image
        run: |
          docker build -t myapp:$GITHUB_SHA .  # Error 3: variable mal referenciada
          docker tag myapp:$GITHUB_SHA myapp:latest
      
      - name: Save Docker image
        run: |
          docker save myapp:latest > myapp.tar
      
      - name: Upload artifact
        uses: actions/upload-artifact@v3
        with:
          name: docker-image
          path: myapp.tar

  deploy:
    needs: [test, build]
    runs-on: ubuntu-latest
    environment: production
    if: github.ref == 'refs/heads/main'
    steps:
      - name: Download artifact
        uses: actions/download-artifact@v3
        with:
          name: docker-image
      
      - name: Load Docker image
        run: docker load < myapp.tar
      
      - name: Deploy application
        run: |
          echo "Deploying to production..."
          docker run -d -p 8080:8080 --name myapp-prod myapp:latest
          
      - name: Health check
        run: |
          sleep 10
          curl -f http://localhost:8080/health || exit 1  # Error 4: el endpoint puede no existir
```

```python
# app.py
from flask import Flask, jsonify

app = Flask(__name__)

@app.route('/')
def hello():
    return jsonify({"message": "Hello World!"})

@app.route('/health')
def health():
    return jsonify({"status": "healthy"})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
```

```dockerfile
# Dockerfile
FROM python:3.9-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY app.py .

EXPOSE 8080
CMD ["python", "app.py"]
```

**Pistas para debugging:**
- Revisa la sintaxis YAML cuidadosamente
- Verifica las referencias a variables de GitHub Actions
- Asegúrate de que los tipos de datos sean correctos
- Considera si todos los endpoints y rutas existen
- Piensa en las dependencias entre jobs

### Resultado Esperado:
- Identificar y corregir al menos 4 errores en el workflow
- El pipeline debe ejecutarse completamente sin fallos
- Los tests deben pasar
- La imagen Docker debe construirse correctamente
- El despliegue debe funcionar solo en la rama main
- El health check debe ser exitoso

---

## Desafío 5: Publicación Multi-Registry con Matrix Strategy

Implementa un workflow que publique una aplicación en múltiples registros usando matrix strategy.

**Archivos a crear:**
- `.github/workflows/multi-registry-publish.yml`
- `Dockerfile`
- `docker-compose.yml`
- `publish.sh`

**Contenido de ejemplo:**

```yaml
# .github/workflows/multi-registry-publish.yml
name: Multi-Registry Publishing

on:
  push:
    tags: ['v*']
  workflow_dispatch:
    inputs:
      version:
        description: 'Version to publish'
        required: true
        default: 'latest'

jobs:
  build-and-publish:
    runs-on: ubuntu-latest
    strategy:
      matrix:
        registry:
          - { name: "GitHub", url: "ghcr.io", username: "${{ github.actor }}", token: "${{ secrets.GITHUB_TOKEN }}" }
          - { name: "Docker Hub", url: "docker.io", username: "${{ secrets.DOCKERHUB_USERNAME }}", token: "${{ secrets.DOCKERHUB_TOKEN }}" }
    
    steps:
      - uses: actions/checkout@v4
      
      - name: Set up Docker Buildx
        uses: docker/setup-buildx-action@v2
      
      - name: Login to ${{ matrix.registry.name }}
        uses: docker/login-action@v2
        with:
          registry: ${{ matrix.registry.url }}
          username: ${{ matrix.registry.username }}
          password: ${{ matrix.registry.token }}
      
      - name: Extract metadata
        id: meta
        uses: docker/metadata-action@v4
        with:
          images: ${{ matrix.registry.url }}/${{ github.repository }}
          tags: |
            type=ref,event=tag
            type=raw,value=latest,enable={{is_default_branch}}
            type=raw,value=${{ github.event.inputs.version }},enable=${{ github.event_name == 'workflow_dispatch' }}
      
      - name: Build and push
        uses: docker/build-push-action@v4
        with:
          context: .
          push: true
          tags: ${{ steps.meta.outputs.tags }}
          labels: ${{ steps.meta.outputs.labels }}
          cache-from: type=gha
          cache-to: type=gha,mode=max
      
      - name: Verify publication
        run: |
          echo "Published to ${{ matrix.registry.name }} successfully!"
          echo "Tags: ${{ steps.meta.outputs.tags }}"
```

```dockerfile
# Dockerfile
FROM node:18-alpine

WORKDIR /app

# Crear una aplicación simple
RUN echo 'const express = require("express");' > app.js && \
    echo 'const app = express();' >> app.js && \
    echo 'app.get("/", (req, res) => res.json({message: "Hello from multi-registry app!"}));' >> app.js && \
    echo 'app.listen(3000, () => console.log("Server running on port 3000"));' >> app.js

# Instalar dependencias
RUN npm init -y && npm install express

EXPOSE 3000
CMD ["node", "app.js"]
```

### Resultado Esperado:
- El workflow debe ejecutarse para tags y manual dispatch
- Debe publicar simultáneamente en múltiples registros usando matrix
- Las imágenes deben tener tags apropiados basados en el evento trigger
- Debe usar cache de GitHub Actions para optimizar builds
- Cada registry debe recibir la misma imagen con tags consistentes