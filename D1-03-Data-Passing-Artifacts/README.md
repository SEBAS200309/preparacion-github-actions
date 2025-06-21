# Concepto a Resolver: Paso de Datos entre Jobs y Gestión de Artefactos

Este conjunto de desafíos explora cómo compartir información entre diferentes jobs en un flujo de trabajo y cómo usar artefactos para almacenar y recuperar archivos generados durante una ejecución.

---

## Desafío: Pasar Outputs entre Jobs

Crea un nuevo archivo de flujo de trabajo en este directorio (`.github/workflows/`) llamado `coding_job_outputs.yml`.

Este flujo de trabajo debe tener dos jobs:
1.  **`generar_datos`**: Este job debe tener un step que genere un valor (por ejemplo, un número aleatorio o una cadena como "build-123") y lo defina como un `output` del step. Luego, este `output` del step debe ser expuesto como un `output` del `job`.
2.  **`consumir_datos`**: Este job debe depender de `generar_datos`. En uno de sus steps, debe acceder al `output` del job `generar_datos` e imprimirlo en la consola.

### Resultado Esperado:
* Un nuevo archivo `D1-03-Data-Passing-Artifacts/coding_job_outputs.yml` en tu repositorio.
* Una ejecución exitosa del flujo de trabajo.
* Los logs del job `consumir_datos` deben mostrar el valor generado por el job `generar_datos`.

---

## Desafío: Uso de Caché y Artefactos de Flujo de Trabajo

Crea un nuevo archivo de flujo de trabajo en este directorio (`.github/workflows/`) llamado `coding_artifacts.yml`.

Este flujo de trabajo debe:
1.  Usar una acción de **caché** (por ejemplo, `actions/cache@v3`) para almacenar las dependencias de `node_modules` (simulando un proyecto Node.js).
2.  Tener un job que simule la "construcción" de un proyecto y genere un archivo de texto simple (`output.txt`) con un contenido como "Construcción exitosa del proyecto A".
3.  **Subir este archivo `output.txt` como un artefacto** del flujo de trabajo (usando `actions/upload-artifact@v3`).
4.  Añadir un comentario en el workflow (o en el `README.md` de este desafío) indicando cómo se podrían **eliminar artefactos** de GitHub.

### Resultado Esperado:
* Un nuevo archivo `D1-03-Data-Passing-Artifacts/coding_artifacts.yml` en tu repositorio.
* Una ejecución exitosa del flujo de trabajo.
* Verificar que la caché se utiliza (la primera vez "cache miss", las siguientes "cache hit").
* Verificar que el artefacto `output.txt` se sube y es descargable desde la página de la ejecución del flujo de trabajo en GitHub.
* Entender la forma de eliminar artefactos (por ejemplo, a través de la interfaz de usuario de GitHub Actions o la API).

---

## Desafío: Depurar un Flujo de Trabajo con Fallo en la Subida/Descarga de Artefactos

Crea el archivo `D1-03-Data-Passing-Artifacts/debugging_artifact_fail.yml` con el siguiente contenido (que contiene errores intencionales):

```yaml
# D1-03-Data-Passing-Artifacts/.github/workflows/debugging_artifact_fail.yml
name: Debugging Artifact Fail

on: [push]

jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - name: Create file
        run: echo "Some content" > output.txt
      - name: Upload artifact (error here)
        uses: actions/upload-artifact@v3
        with:
          name: my-artifact
          path: non_existent_folder/output.txt # Error: Ruta incorrecta, no existe 'non_existent_folder'

  download:
    runs-on: ubuntu-latest
    needs: build
    steps:
      - name: Download artifact (will fail if upload fails or name is wrong)
        uses: actions/download-artifact@v3
        with:
          name: non-existent-artifact # Error: Nombre incorrecto si el artefacto de 'build' se llama 'my-artifact'
          path: ./downloaded-artifact
      - name: Verify downloaded content
        run: cat ./downloaded-artifact/output.txt
```

## Resultados

### Desafío: Pasar Outputs entre Jobs
[![trabajo con artifacts](https://github.com/LuisDelgado-LD/preparacion-github-actions/actions/workflows/coding_job_outputs.yml/badge.svg)](https://github.com/LuisDelgado-LD/preparacion-github-actions/actions/workflows/coding_job_outputs.yml)

Dado que nunca había trabajado en enviar output de un job a otro, mi primer destino fue [la documentación](https://docs.github.com/en/actions/writing-workflows/choosing-what-your-workflow-does/passing-information-between-jobs), lo primero que se menciona es acerca de la propiedad `needs`, la cual conocía sin embargo no había trabajado en ella por lo leí la documentación de [needs](https://docs.github.com/en/actions/writing-workflows/choosing-what-your-workflow-does/using-jobs-in-a-workflow#example-not-requiring-successful-dependent-jobs) para proseguir, además recordaba que era mandatorio definir un `id` para el step y poder referenciarlo posteriormente.


#### Código

```yaml
name: trabajo con artifacts

on:
  push:
    branches:
      - main 
  workflow_dispatch:
    

jobs:
  generar_datos:
    name: Generar datos 
    runs-on: ubuntu-latest
    steps:
      - id: GO
        name: Generar output
        run: echo "salida=Output capturado desde step en generar_datos" >> "$GITHUB_OUTPUT"
    outputs:
      output_del_step: ${{ steps.GO.outputs.salida }}
  
  consumir_datos:
    runs-on: ubuntu-latest
    needs: generar_datos
    steps:
      - name: Visualizar datos capturados de job anterior
        run: |
          echo "${{ needs.generar_datos.outputs.output_del_step }}"
```
#### Evidencia
![](Resultado%20coding_job_outputs%2001.png)
![](Resultado%20coding_job_outputs%2002.png)


### Desafío: Uso de Caché y Artefactos de Flujo de Trabajo
[![artifacts and cache](https://github.com/LuisDelgado-LD/preparacion-github-actions/actions/workflows/coding_artifacts.yml/badge.svg)](https://github.com/LuisDelgado-LD/preparacion-github-actions/actions/workflows/coding_artifacts.yml)

Dado que ya he trabajado con Actions de cache antes fuí directo a ver la documentación que necesito.
Como dejamos de lado los `echo` y empezamos a trabajar con información del repositorio la primera action que busqué fue [checkout](https://github.com/marketplace/actions/checkout) y utilicé la propiedad `with` para utilizar un repositorio que ya tiene dependencias de node
lo siguiente es trabajar con el action de `cache`, del cual ya estoy algo familiarizado, sin embargo nunca viene mal una releida a su [documentacion](https://github.com/marketplace/actions/cache) 
Finalmente, la documentación de [upload-artifact](https://github.com/marketplace/actions/upload-a-build-artifact) con la cual nunca había trabajado antes.

Por un error cometí algunos errores que detallo a continuación
Actions checkout:
Por no leer en profundidad la documentación y los ejemplos, pensé que al utilizar la propiedad `repository` dentro del `with` tenía que colocar la url completa, y es solo en formato `<nombre usuaro>/<nombre repo>` 
Otro error que cometí y resolví en el mismo commit anterior, fue en la propiedad `branches` indicar una rama inexistente, dado que en un inicio pensé en crearla para subir un proyecto en node, pero esta idea la deseche ya que consideré más productivo ejecutar el action `checkout` con un repositorio distinto.
Estos errores fueron corregidos en este [commit](https://github.com/LuisDelgado-LD/preparacion-github-actions/commit/b3b42534ccecc41e96cd4ab61957d9b75b3a66c7).
El otro error que cometí fue con la action `cache`, pensando que ya había declarado la `key` y el `restore-keys` además de un error en el comando `npm i` ya que había colocado `npm -i` 
Ambos errores fueron corregidos en este [commit](https://github.com/LuisDelgado-LD/preparacion-github-actions/commit/b6c7ce883a244c785d18370a84119bed9e1a7fea)

En todo caso, como era un entorno con node y el gestor npm, resulta más eficiente utilizar la cache específica para npm como por ejemplo [setup-node](https://github.com/actions/setup-node)


#### Código

```yaml
name: artifacts and cache

on:
  push:
    branches:
      - "*"
  workflow_dispatch:

jobs:
  crear-cache:
    name: github actions 
    runs-on: ubuntu-latest
    steps:
      - name: importar repositorio
        uses: actions/checkout@v4
        with:
          repository: LuisDelgado-LD/proyecto-integrador-dh-frontend
          
      - name: cache 
        uses: actions/cache@v4
        with:
          key: ${{ hashFiles('./package-lock.json') }}
          path: node_modules/
          restore-keys: ${{ hashFiles('./package-lock.json') }}
      - name: Build nodejs package
        run: npm i >> instalacion.txt
      - name: upload artifacts
        uses: actions/upload-artifact@v4
        with:
          name: "Resultado instalacion"
          path: "instalacion.txt"
          overwrite: true
```
#### Evidencia
##### creacion de artifact (sha256:9c3e26c1d4977d3e006eb2056db777137c7fb6de77e109b4782312afd7431ec0)
![](./resultado%20coding_artifacts1%2001.png)
##### artifact
[Resultado instalación 01.zip](./Resultado%20instalacion%2001.zip)
```txt

added 321 packages, and audited 322 packages in 8s

112 packages are looking for funding
  run `npm fund` for details

2 vulnerabilities (1 low, 1 moderate)

To address all issues, run:
  npm audit fix

Run `npm audit` for details.

```
##### cache miss
![](./resultado%20coding_artifacts1%2002.png)
##### subida de nuevo artifact (sha256:14d8c5f3bb938ee58d40880979776242880b676c41352c5baac52273a4791799)
![](./resultado%20coding_artifacts2%2001.png)
##### artifact
[Resultado instalación 02.zip](./Resultado%20instalacion%2002.zip)
```txt

up to date, audited 322 packages in 1s

112 packages are looking for funding
  run `npm fund` for details

2 vulnerabilities (1 low, 1 moderate)

To address all issues, run:
  npm audit fix

Run `npm audit` for details.

```
##### cache hit
![](./resultado%20coding_artifacts2%2002.png)

### Desafío: Depurar un Flujo de Trabajo con Fallo en la Subida/Descarga de Artefactos
[![Debugging Artifact Fail](https://github.com/LuisDelgado-LD/preparacion-github-actions/actions/workflows/debugging_artifact_fail.yml/badge.svg)](https://github.com/LuisDelgado-LD/preparacion-github-actions/actions/workflows/debugging_artifact_fail.yml)

Este desafío lo completé en 2 commits por intentar hacerlo rápido, los errores erán fácilmente reconocibles, aunque el error de las versiones de los actions hubiese sido igualmente fácil si hubiese leido la documentación correspondiente, cosa que no hice.
los commits de corrección fueron
[ac4f8ac2e359082a2f5757d0c6e624ab45fffe73](https://github.com/LuisDelgado-LD/preparacion-github-actions/commit/ac4f8ac2e359082a2f5757d0c6e624ab45fffe73)
[a8dc450678f6d81649a93e9834df9a30a44ff470](https://github.com/LuisDelgado-LD/preparacion-github-actions/commit/a8dc450678f6d81649a93e9834df9a30a44ff470)

#### Código

```yaml
name: Debugging Artifact Fail

on: [push]

jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - name: Create file
        run: echo "Some content" > output.txt
      - name: Upload artifact (error here)
        uses: actions/upload-artifact@v4
        with:
          name: my-artifact
          path: output.txt 

  download:
    runs-on: ubuntu-latest
    needs: build
    steps:
      - name: Download artifact (will fail if upload fails or name is wrong)
        uses: actions/download-artifact@v4
        with:
          name: my-artifact
          path: ./downloaded-artifact
      - name: Verify downloaded content
        run: cat ./downloaded-artifact/output.txt
```
#### Evidencia
![](./resultado%20debugging_artifact_fail%201.png)
![](./resultado%20debugging_artifact_fail%202.png)