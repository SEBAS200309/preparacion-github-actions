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

```text
# requirements.txt
flask==2.0.1
pytest==7.4.0
pytest-flask==1.2.0
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


## Resultados

### Desafío 1: Construcción y Publicación de Artefactos Python
[![Practica publicacion package](https://github.com/LuisDelgado-LD/preparacion-github-actions/actions/workflows/build-publish.yml/badge.svg)](https://github.com/LuisDelgado-LD/preparacion-github-actions/actions/workflows/build-publish.yml)

Mi primera investigación fue averiguar sobre la propiedad [on.pull_request](https://docs.github.com/en/actions/writing-workflows/choosing-when-your-workflow-runs/events-that-trigger-workflows#pull_request) la cual encontré interesante y con varios tipos de actividad disponibles
Aproveché que tengo que trabajar sobre un directorio específico para utilizar el filtro por [path](https://docs.github.com/en/actions/writing-workflows/workflow-syntax-for-github-actions#onpushpull_requestpull_request_targetpathspaths-ignore)
Luego, como siempre me fui a la documentación habitual de [actions/checkout](https://github.com/marketplace/actions/checkout) y [actions/upload-artifact](https://github.com/marketplace/actions/upload-a-build-artifact#usage)
Además como se tiene que trabajar con python para este ejercicio, busqué alguna actions que me sirviera, encontrando [actions/setup-python](https://github.com/marketplace/actions/setup-python) permitiendo cachear las dependencias instaladas.
Un problema que tuve fue el uso del [working-directory](https://docs.github.com/en/actions/writing-workflows/workflow-syntax-for-github-actions#jobsjob_idstepsworking-directory) y tuve varios problemas relacionados a la ruta de la carpeta dentro del repositorio donde se encontraban los archivos necesarios.
En el commit [89977f1](https://github.com/LuisDelgado-LD/preparacion-github-actions/commit/89977f10375e7b7bb2d61c1919435544463c4051) hago la solución definitiva sin embargo antes pase por los commits
[d929ee1](https://github.com/LuisDelgado-LD/preparacion-github-actions/commit/d929ee19455434057f97d90d9484699d4c98471b)
[fe18cbf](https://github.com/LuisDelgado-LD/preparacion-github-actions/commit/fe18cbfaf42365eb1ea822a61ea90b1046a2cf32)
Ya obteniendo el resultado esperado, aproveche el objetivo del workflow para generar jobs adicionales y dependencias utilizando la propiedad needs 
Creo que el workflow es mejorable, por ejemplo agregando un if para ejecutar el step de descarga de paquetes de ip solo si hay un miss en la cache
pero quiero enfocarme en seguir con mi aprendizaje 

#### Código

```yaml
name: Practica publicacion package

on:
  push: 
    paths:
      - "D1-05-CI-CD-Publishing/desafío 1/**"
  pull_request:
    types: opened
    paths:
      - "D1-05-CI-CD-Publishing/desafío 1/**"
  workflow_dispatch:
jobs:
  install_requeriments:
    name: creacion de entorno base
    runs-on: ubuntu-latest
    steps:
      - name: clonar repositorio
        uses: actions/checkout@v4
      - name: cache step
        uses: actions/setup-python@v5
        with:
          cache: 'pip' 
          python-version: '3.13'
      - name: instalación de dependencias
        run: pip download -r requirements.txt
        working-directory: "D1-05-CI-CD-Publishing/desafío 1/"
  tests:
    needs: install_requeriments
    runs-on: ubuntu-latest
    name: Pruebas de codigo
    steps:
      - name: clonar repositorio
        uses: actions/checkout@v4
      - name: cache step
        uses: actions/setup-python@v5
        with:
          cache: 'pip' 
          python-version: '3.13'
      - name: instalación de dependencias
        run: pip install -r requirements.txt
        working-directory: "D1-05-CI-CD-Publishing/desafío 1/"
      - name: tests
        run: pytest | tee resultado_tests.txt 2>&1 
        working-directory: "D1-05-CI-CD-Publishing/desafío 1/"
      - name: Subir resultados de tests
        uses: actions/upload-artifact@v4
        with:
          name: tests_logs.txt
          path: "D1-05-CI-CD-Publishing/desafío 1/resultado_tests.txt"
          overwrite: true
  build:
    needs: install_requeriments
    runs-on: ubuntu-latest
    name: Construccion del paquete
    steps:
      - name: clonar repositorio
        uses: actions/checkout@v4
      - name: cache step
        uses: actions/setup-python@v5
        with:
          cache: 'pip' 
          python-version: '3.13'
      - name: instalación de dependencias
        run: pip install -r requirements.txt
        working-directory: "D1-05-CI-CD-Publishing/desafío 1/"
      - name: creación de paquete
        run: python setup.py sdist bdist_wheel
        working-directory: "D1-05-CI-CD-Publishing/desafío 1/"
      - name: Subir paquete creado
        uses: actions/upload-artifact@v4
        with:
          name: python-package-${{ github.sha }}
          path: "D1-05-CI-CD-Publishing/desafío 1/dist/*"
```

#### Evidencia

##### Artefactos
[python package](./python-package-b865788a6c290ba6405982e52e27682d2c90f70e.zip)
[logs](./tests_logs.txt.zip)

![](./resultado%20build-publish.png)

### Desafío 2: Pipeline Multi-Stage con Environments
[![Despliegue en multi stage](https://github.com/LuisDelgado-LD/preparacion-github-actions/actions/workflows/multi-stage-deploy.yml/badge.svg)](https://github.com/LuisDelgado-LD/preparacion-github-actions/actions/workflows/multi-stage-deploy.yml)

Este desafío creo que es fácil, sin embargo la complicación radica en la "aprobación manual" que es el concepto a prácticar. Como siempre el primer paso es buscar en la documentación.
Mi primera aproximación fue la propiedad [jobs.<id>.steps.[*].env](https://docs.github.com/en/actions/writing-workflows/workflow-syntax-for-github-actions#jobsjob_idstepsenv) con el cual ya había trabajado en workflows anteriores.
Luego decidí enfocar la búsqueda en como lograr la aprobación manual, en esta tarea encontre los [environment para despliegues](https://docs.github.com/en/actions/managing-workflow-runs-and-deployments/managing-deployments/managing-environments-for-deployment).
Tomando esta aproximación seguí los pasos para [crear un entorno](https://docs.github.com/en/actions/managing-workflow-runs-and-deployments/managing-deployments/managing-environments-for-deployment#creating-an-environment), en este caso cree 2 entornos distintos con el fin de observar la diferencia en la asignación de valores a la variable dependiendo del entorno.
Luego seguí los pasos para [configurar la aprobación](https://docs.github.com/en/actions/managing-workflow-runs-and-deployments/managing-deployments/reviewing-deployments)
y me dispuse a configurar las variables contextuales en el workflow no sin antes pasar por su [respectiva documentación](https://docs.github.com/en/actions/writing-workflows/choosing-what-your-workflow-does/accessing-contextual-information-about-workflow-runs)
ya con la información clara procedí a crear el primer [commit](https://github.com/LuisDelgado-LD/preparacion-github-actions/commit/5db6e826670af5628416c7627f734faca13b789e) con el workflow.
Debo indicar que este desafío fue el que más commits generó debido a diversos errores que iré detallando.
#### Error1
[5db6e82](https://github.com/LuisDelgado-LD/preparacion-github-actions/commit/5db6e826670af5628416c7627f734faca13b789e) subi el workflow sin haber subido previamente los archivos del directorio D1-05-CI-CD-Publishing/desafio 2/, esto se corrigio en [913c838](https://github.com/LuisDelgado-LD/preparacion-github-actions/commit/913c8388ed9659d910bc5a3b326378646ec0f815).
El siguiente error fue con el uso de las variables, como en un inicio estaba pensando utilizar el contexto `env` y luego lo cambié por `vars` olvidé hacer este cambio en el workflow, esto lo corregi fácilmente en el commit [b931830](https://github.com/LuisDelgado-LD/preparacion-github-actions/commit/b931830fe724c1642a4774d939ee69d74d9453b7). Sin embargo el workflow no solicitó la aprobación, el error fue simple, no guardar los cambios en la configuración del environment del repo.
Un commit interesante fue [acf8558](https://github.com/LuisDelgado-LD/preparacion-github-actions/commit/acf8558f1fcc47b123fcc606c3a17f47e9cfa3e4) ya que corrigio un error en el uso de las variables, lo que me ayudó a afianzar la comprensión del formato yaml
Un detalle que olvidé en el workflow inicial fue el requisito de generar los artefactos, decidí aprovechar de reforzar conocimientos de desafíos anteriores utilizando la propiedad `steps.outputs` 
Nuevamente me ocurrió el mismo error del desafío anterior, el `working-directory` fue mal configurado en los nuevos steps por lo que el workflow falló 
Luego se generaron una serie de commits con errores asociados principalmente a la captura del mensaje deseado (`echo "Deployment to $ENVIRONMENT completed successfully!"`) desde la perspectiva de la programación por lo que no entraré en detalles

#### Código

```yaml
name: Despliegue en multi stage

on:
  push: 
  workflow_dispatch:

jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - name: Relleno
        run: echo "Este step no hace nada realmente"
  staging:
    environment: staging
    runs-on: ubuntu-latest
    needs: build 
    name: Job de staging
    steps:
      - name: clonar repositorio
        uses: actions/checkout@v4
      - name: Hacer despliegue en ${{ vars.ETAPA }}
        working-directory: "D1-05-CI-CD-Publishing/desafio 2/"
        run: bash deploy.sh ${{ vars.ETAPA }} | tee resultado_${{ vars.ETAPA }}.txt
      - name: Guardar resultado
        id: results-staging
        working-directory: "D1-05-CI-CD-Publishing/desafio 2/"
        run: |
          echo "${{ vars.ETAPA }}=$(cat resultado_${{ vars.ETAPA }}.txt| grep -i Deployment)" >> "$GITHUB_OUTPUT"
    outputs:
        log-staging: ${{ steps.results-staging.outputs.staging }}
  production:
    name: Job de prod
    environment: "production"
    runs-on: ubuntu-latest
    needs: [build, staging ]
    steps:
      - name: clonar repositorio
        uses: actions/checkout@v4
      - name: Hacer despliegue en ${{ vars.etapa }}
        working-directory: "D1-05-CI-CD-Publishing/desafio 2/"
        run: bash deploy.sh ${{ vars.etapa }} | tee resultado_${{ vars.ETAPA }}.txt
      - name: Guardar resultado
        id: results-production
        working-directory: "D1-05-CI-CD-Publishing/desafio 2/"
        run: |
          echo "${{ vars.ETAPA }}=$(cat resultado_${{ vars.ETAPA }}.txt | grep -i Deployment)" >> "$GITHUB_OUTPUT"
    outputs:
        log-production: ${{ steps.results-production.outputs.production }}
  upload_artifacts:
    name: Generar evidencias
    runs-on: ubuntu-latest
    needs: [build, staging, production]
    steps:
      - name: Recolectar evidencias
        run: |
          echo ${{ needs.staging.outputs.log-staging }} > resultados.txt
          echo ${{ needs.production.outputs.log-production }} >> resultados.txt
          cat resultados.txt
      - name: artifacts
        uses: actions/upload-artifact@v4
        with:
          path: resultados.txt
```

#### Evidencia
#### Configuración del environment en el repositorio
![](./Creacion%20environment%2001.png)
![](./Creacion%20environment%2002.png)

#### configuración de las variables en el environment creado
![](./Creacion%20variables%20environment.png)

#### Resultado del workflow solicitando aprobación
![](./resultado%20multi-stage-deploy%2001.png)

![](./resultado%20multi-stage-deploy%2002.png)

![](./resultado%20multi-stage-deploy%2003.png)

#### Artifact
[sha256:2ae80609911c3537d804915c522fa01ad94e91e6b45cf6a711d1fa8b8dfce97c](./artifact.zip)
```txt
Deployment to staging completed successfully!
Deployment to production completed successfully!
```

### Desafío 3: Publicación Automática de Releases
[![Releases](https://github.com/LuisDelgado-LD/preparacion-github-actions/actions/workflows/release.yml/badge.svg)](https://github.com/LuisDelgado-LD/preparacion-github-actions/actions/workflows/release.yml)

Este desafío estuvo bastante difícil, mi traba principal fue el registro en el registro npm de github pero también pude indagar en un experimento que queria hacer hace un rato.
Con ayuda de GPT-4.1 me sentí más seguro en probar la propiedad `jobs.[id].defaults.run.working-directory`, mi miedo residia en que, como el directorio no existe el step de `actions/checkout` fallaría, sin embargo consultando al mismo LLM me aclaró que la propiedad `jobs.[id].defaults.run.working-directory` modifica la variable `pwd` y que `actions/checkout` utiliza la variable `$GITHUB_WORKSPACE` tal como aparece en la [documentación](https://github.com/marketplace/actions/checkout).
Mi siguiente investigación se centro en la subida del paquete, ya antes había trabajado con la subida de imagenes de contenedor en los repositorios [proyecto-integrador-dh-backend](https://github.com/LuisDelgado-LD/proyecto-integrador-dh-backend) y [proyecto-integrador-dh-frontend](https://github.com/LuisDelgado-LD/proyecto-integrador-dh-frontend) sin embargo descubrí la gran diferencia entre lo que había hecho para `github registry container` y lo que tenía que hacer ahora con `github package` 
En ambos casos debo crear un [`token clásico`](https://docs.github.com/en/packages/working-with-a-github-packages-registry/working-with-the-npm-registry), lei sobre el token por defecto que se utiliza en github Actions [`GITHUB_TOKEN`](https://docs.github.com/en/actions/security-for-github-actions/security-guides/automatic-token-authentication) 
También aproveche de utilizar una variable que me llamó la atención que considero que es bastante útil para este ejercicio donde estamos trabajando con tags `${{ github.action_ref }}`, sin embargo me equivoqué pensando que esta variable contiene el valor del tag que dispara el workflow, esto lo corregí en el commit [229ead2](https://github.com/LuisDelgado-LD/preparacion-github-actions/commit/229ead2f8e9b396a55f92d9e89146566b84c2b05) cambiandolo por `${{ github.ref }}` logrando que el step con `actions/checkout` traiga solamente lo necesario. Se adjunta el mensaje de error con `${{ github.action_ref }}`

```error
Fetching the repository
  /usr/bin/git -c protocol.version=2 fetch --no-tags --prune --no-recurse-submodules --depth=1 origin +refs/heads/v4*:refs/remotes/origin/v4* +refs/tags/v4*:refs/tags/v4*
  The process '/usr/bin/git' failed with exit code 1
  Waiting 18 seconds before trying again
  /usr/bin/git -c protocol.version=2 fetch --no-tags --prune --no-recurse-submodules --depth=1 origin +refs/heads/v4*:refs/remotes/origin/v4* +refs/tags/v4*:refs/tags/v4*
  The process '/usr/bin/git' failed with exit code 1
  Waiting 12 seconds before trying again
  /usr/bin/git -c protocol.version=2 fetch --no-tags --prune --no-recurse-submodules --depth=1 origin +refs/heads/v4*:refs/remotes/origin/v4* +refs/tags/v4*:refs/tags/v4*
  Error: The process '/usr/bin/git' failed with exit code 1
```

Luego tuve varios problemas con la autenticación de npm, al principio probé lo indicado en este post de [stackoverflow](https://stackoverflow.com/a/78610466) que no resultó, hasta que probé en el commit
[37a9c8d](https://github.com/LuisDelgado-LD/preparacion-github-actions/commit/37a9c8d639f681cfac2cc66d50cc7fb070ecd1d2) ya que había leído sintaxis similares [aquí](https://github.com/healthplace/npmrc-registry-login-action/blob/master/index.js) y [aquí](https://stackoverflow.com/a/72984096)
Con lo que se logró que se ejecutará el workflow


#### Código

```yaml
name: Releases

on:
  push:
    tags:
      - 'v*'

jobs:
  compile:
    runs-on: ubuntu-latest 
    name: Compilación del paquete
    defaults:
      run:
        working-directory: D1-05-CI-CD-Publishing/desafio 3
    steps:
      - name: Checkout del proyecto
        uses: actions/checkout@v4
        with:
          ref: ${{ github.ref }}
      - name: Instalación entorno node
        uses: actions/setup-node@v4
      - name:  configurar repositorio
        run: |
          echo "@$(echo $GITHUB_REPOSITORY | cut -d/ -f1):registry=https://npm.pkg.github.com/" > .npmrc
          echo "//npm.pkg.github.com/:_authToken=${{ secrets.PACKAGE }}" >> .npmrc
      - name: Compilación
        run: |
          bash build.sh
      - name: publicacion
        run: npm publish
        env:
          NODE_AUTH_TOKEN: ${{ secrets.PACKAGE }}
```

#### Evidencias
##### Creación del token
###### Paso 1
![](./desafio%203/Acceso%20para%20crear%20token%20clásico%2001.png)
###### Paso 2
![](./desafio%203/Acceso%20para%20crear%20token%20clásico%2002.png)
###### Paso 3
![](./desafio%203/Acceso%20para%20crear%20token%20clásico%2003.png)
###### Paso 4
![](./desafio%203/Acceso%20para%20crear%20token%20clásico%2004.png)
###### Paso 5
![](./desafio%203/Acceso%20para%20crear%20token%20clásico%2005.png)
###### Paso 6
![](./desafio%203/Acceso%20para%20crear%20token%20clásico%2006.png)

![](./resultado%20release.png)

### Desafío 4: Resolución de Problemas - Pipeline de CI/CD Roto
[![Broken CI/CD Pipeline](https://github.com/LuisDelgado-LD/preparacion-github-actions/actions/workflows/broken-pipeline.yml/badge.svg)](https://github.com/LuisDelgado-LD/preparacion-github-actions/actions/workflows/broken-pipeline.yml)

Siento que este desafío se sale de los margenes necesarios para realizar el examen de certificación GitHub Actions, sin embargo, no dejé de sacar nuevo conocimiento. El primero de ellos fue conocer 
el [listado de paqueteria instalada por defecto](https://github.com/actions/runner-images/blob/main/images/ubuntu/Ubuntu2404-Readme.md) en los runners que se utilizan, evidentemente dependiendo de la familia que se utilice (`ubuntu-latest`, `ubuntu-24.04`, `ubuntu-22.04`, `macos-15-large`, `macos-15`, `macos-15-xlarge`, `macos-latest-large`, `macos-14-large`, `macos-latest`, `macos-14`, `macos-latest-xlarge`, `macos-14-xlarge`, `macos-13`, `macos-13-large`, `macos-13-xlarge`, `windows-2025`, `windows-latest`, `windows-2022`, `windows-2019`).
También al parecer como descubrí en una investigación anterior *todos* los actions utilizan por defecto la variable `$GITHUB_WORKSPACE` y no es un efecto exclusivo del actions `actions/checkout` sino que un estandar que se aplica a todos los actions

Los demás errores fueron principalmente asociados al código

#### Código

```yaml
# .github/workflows/broken-pipeline.yml (CONTIENE ERRORES)
name: Broken CI/CD Pipeline

on:
  push:
    branches: [ main, develop ]  
  pull_request:
    branches: [ main ]

jobs:
  test:
    defaults:
      run:
        working-directory: "D1-05-CI-CD-Publishing/desafio 4/"
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      
      - name: Setup Python
        uses: actions/setup-python@v4
        with:
          python-version: 3.9 
      
      - name: Install dependencies
        run: |
          python -m pip install --upgrade pip
          pip install -r requirements.txt
      
      - name: Run tests
        run: python -m pytest tests/ --verbose
        
  build:
    defaults:
      run:
        working-directory: "D1-05-CI-CD-Publishing/desafio 4/"
    needs: test
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      
      - name: Build Docker image
        run: |
          docker build -t myapp:${{ GITHUB.SHA }} .  
          docker tag myapp:${{ GITHUB.SHA }} myapp:latest
      
      - name: Save Docker image
        run: |
          docker save myapp:latest | tee myapp.tar
      
      - name: Upload artifact
        uses: actions/upload-artifact@v4
        with:
          name: docker-image
          path: "D1-05-CI-CD-Publishing/desafio 4/myapp.tar"

  deploy:
    needs: [test, build]
    runs-on: ubuntu-latest
    environment: production
    if: github.ref == 'refs/heads/main'
    steps:
      - name: Download artifact
        uses: actions/download-artifact@v4
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
          curl -f http://localhost:8080/health || exit 1  
```

#### Evidencia
![](./resultado%20broken-pipeline.png)



### Desafío 5: Publicación Multi-Registry con Matrix Strategy

Este desafío no se hizo ya que el chatbot incluyó el código de respuesta, adicionalmente se debian realizar gestiones adicionales como crear cuenta en docker registry, de igual forma conocí las propiedades `workflow_dispatch.inputs.`, me hubiese gustado trabajar con matrices ya que hasta el momento no he visto, pero lo dejaré como tarea pendiente ya que espero que venga un ejercicio específico para eso en el futuro