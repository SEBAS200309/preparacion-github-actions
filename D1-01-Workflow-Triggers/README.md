# Concepto a Resolver: Trabajar con eventos que activan flujos de trabajo

Este conjunto de desafíos se centra en la configuración de diferentes tipos de eventos que pueden activar una ejecución de GitHub Actions, incluyendo eventos comunes como `push` y `pull_request`, así como eventos programados (`schedule`) y manuales (`workflow_dispatch`).

---

## Desafío: Creación de un Flujo de Trabajo Básico con Triggers Comunes

Crea un nuevo archivo de flujo de trabajo en este directorio (`.github/workflows/`) llamado `coding_push_pr.yml`.

Este flujo de trabajo debe configurarse para ejecutarse automáticamente bajo las siguientes condiciones:
1.  Cuando se realiza un `push` a la rama `main`.
2.  Cuando se abre, sincroniza o reabre un `pull_request` dirigido a la rama `main`.

El flujo de trabajo debe contener un solo `job` llamado `ejecutar_comandos` con un `step` que simplemente imprima "¡El flujo de trabajo se activó por un push o pull request!" en la consola.

### Resultado Esperado:
* Un nuevo archivo `D1-01-Workflow-Triggers/coding_push_pr.yml` en tu repositorio.
* Ver una ejecución exitosa del flujo de trabajo en la pestaña "Actions" de GitHub cuando:
    * Hagas un `push` a la rama `main`.
    * Crees un nuevo `pull_request` dirigido a `main`.
    * Realices un `push` a una rama de un `pull_request` existente dirigido a `main`.
* Los logs del job `ejecutar_comandos` deben mostrar la frase especificada.

---

## Desafío: Configurar flujos de trabajo para eventos programados y manuales

Crea un nuevo archivo de flujo de trabajo en este directorio (`.github/workflows/`) llamado `coding_schedule_manual.yml`.

Este flujo de trabajo debe configurarse para:
1.  Ejecutarse automáticamente **todos los días a las 03:00 AM UTC** (utilizando el evento `schedule`).
2.  Permitir la **activación manual** desde la interfaz de usuario de GitHub (utilizando el evento `workflow_dispatch`).

El flujo de trabajo debe contener un job llamado `tarea_programada_o_manual` con un step que imprima un mensaje que indique cómo fue activado (puedes usar variables de contexto como `github.event_name` para esto).

### Resultado Esperado:
* Un nuevo archivo `D1-01-Workflow-Triggers/coding_schedule_manual.yml` en tu repositorio.
* Verificar que el flujo de trabajo aparece en la sección "Actions" con la opción "Run workflow" disponible para su activación manual.
* Una ejecución exitosa visible en la pestaña "Actions" cuando lo actives manualmente.
* Los logs del job `tarea_programada_o_manual` deben mostrar el mensaje correcto según el evento que lo activó (por ejemplo, "Se activó por workflow_dispatch").

---

## Desafío: Depurar un Flujo de Trabajo que no se Activa Correctamente

Crea el archivo `D1-01-Workflow-Triggers/debugging_trigger_fail.yml` con el siguiente contenido (que contiene un error intencional):

```yaml
# D1-01-Workflow-Triggers/.github/workflows/debugging_trigger_fail.yml
name: Depuración de Trigger Fallido

on:
  push:
    branches:
      - !main # Esto es un error intencional, no funcionará como se espera para "no main"

jobs:
  check-branch:
    runs-on: ubuntu-latest
    steps:
      - name: Show branch
        run: echo "Esta rama es: ${{ github.ref }}"
```

## Resultados
### Desafío: Creación de un Flujo de Trabajo Básico con Triggers Comunes
[![Coding Push PR](https://github.com/LuisDelgado-LD/preparacion-github-actions/actions/workflows/coding_push_pr.yml/badge.svg)](https://github.com/LuisDelgado-LD/preparacion-github-actions/actions/workflows/coding_push_pr.yml)
#### Código

```yaml
name: Coding Push PR

on:
  push:
    branches:
      - main
  pull_request:
    branches:
      - main

jobs:
  ejecutar_comandos:
    runs-on: ubuntu-latest
    steps:
      - name: echo
        run: echo "¡El flujo de trabajo se activó por un push o pull request!"
```
#### Evidencia
![](./resultado%20coding_push_pr.png)

### Desafío: Configurar flujos de trabajo para eventos programados y manuales
[![cron](https://github.com/LuisDelgado-LD/preparacion-github-actions/actions/workflows/coding_schedule_manual.yml/badge.svg?event=schedule)](https://github.com/LuisDelgado-LD/preparacion-github-actions/actions/workflows/coding_schedule_manual.yml)

[![cron](https://github.com/LuisDelgado-LD/preparacion-github-actions/actions/workflows/coding_schedule_manual.yml/badge.svg?event=workflow_dispatch)](https://github.com/LuisDelgado-LD/preparacion-github-actions/actions/workflows/coding_schedule_manual.yml)
#### Código
Para este desafío me apoyé en la documentación ya que desconocía la sintaxis del trigger `schedule`  
[https://docs.github.com/es/actions/writing-workflows/choosing-when-your-workflow-runs/events-that-trigger-workflows#schedule](https://docs.github.com/es/actions/writing-workflows/choosing-when-your-workflow-runs/events-that-trigger-workflows#schedule)

```yaml
name: cron

on:
  workflow_dispatch:
  # https://docs.github.com/es/actions/writing-workflows/choosing-when-your-workflow-runs/events-that-trigger-workflows#schedule
  schedule:
    - cron: '0 3 * * *'
jobs:
  tarea_programada_o_manual:
    runs-on: ubuntu-latest
    steps:
      - name: log
        run: echo "Ejecutado desde ${{github.event_name}}"

```
#### Evidencia
![](./resultado%20coding_schedule_manual%20ejecucion%20manual.png)

### Desafío: Depurar un Flujo de Trabajo que no se Activa Correctamente
[![Depuración de Trigger Fallido](https://github.com/LuisDelgado-LD/preparacion-github-actions/actions/workflows/debugging_trigger_fail.yml/badge.svg)](https://github.com/LuisDelgado-LD/preparacion-github-actions/actions/workflows/debugging_trigger_fail.yml)
[![Depuración de Trigger Fallido](https://github.com/LuisDelgado-LD/preparacion-github-actions/actions/workflows/debugging_trigger_fail.yml/badge.svg?branch=d1-4)](https://github.com/LuisDelgado-LD/preparacion-github-actions/actions/workflows/debugging_trigger_fail.yml)

Este desafío estuvo interesante, a pesar que la ia indicó un solo error en realidad eran 2. Para el primero la solución fue simple, basto con ver los ejemplos para darme cuenta que la lista debe ser de texto y por lo tanto debe estar rodeado de comillas simples `'` o dobles `"`. 
El segundo error aún no tengo 100% claro como se resolvío, mi teoría más fuerte es un problema con la sintaxis y el uso de ":" dentro del valor de `run` 

#### Código
```yaml
name: Depuración de Trigger Fallido

on:
  push:
    branches-ignore:
      - 'main' # Esto es un error intencional, no funcionará como se espera para "no main"
      # https://docs.github.com/en/actions/writing-workflows/choosing-when-your-workflow-runs/events-that-trigger-workflows#push

jobs:
  check-branch:
    runs-on: ubuntu-latest
    steps:
      - name: Show branch
        run: |
          echo "Esta rama es: ${{ github.ref }}"
```
#### Evidencia
![](./resultado%20debugging_trigger_fail.png)
