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