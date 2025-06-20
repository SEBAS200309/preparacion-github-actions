# Concepto a Resolver: Uso de Secretos y Variables de Entorno

Este conjunto de desafíos te guiará a través de la configuración y el uso de secretos para información sensible y la definición de variables de entorno personalizadas en tus flujos de trabajo de GitHub Actions. También aborda la depuración de problemas comunes relacionados con su acceso.

---

## Desafío: Acceder a un Secreto de Repositorio en un Flujo de Trabajo

Crea un nuevo archivo de flujo de trabajo en este directorio (`.github/workflows/`) llamado `coding_repo_secret.yml`.

1.  Ve a la configuración de tu repositorio en GitHub (**Settings > Secrets and variables > Actions > Repository secrets**) y crea un nuevo "Repository Secret" llamado `MY_SUPER_SECRET`. Asígnale un valor de tu elección (por ejemplo, "ValorSecreto123").
2.  En el flujo de trabajo, crea un job llamado `usar_secreto` con un step que intente imprimir el valor de `MY_SUPER_SECRET` en la consola.
3.  **¡Importante!** Para el `step` que imprime el secreto, asegúrate de que el valor del secreto no quede expuesto directamente en los logs de GitHub Actions. Investiga cómo puedes enmascarar los secretos en los logs (`core.setSecret` en JavaScript, o usando el comando `add-mask` con `echo`).

### Resultado Esperado:
* Un secreto de repositorio `MY_SUPER_SECRET` configurado en GitHub.
* Un nuevo archivo `D1-02-Secrets-Env-Vars/coding_repo_secret.yml` en tu repositorio.
* Una ejecución exitosa del flujo de trabajo.
* Los logs del job `usar_secreto` deben mostrar el valor del secreto **enmascarado** (por ejemplo, `***`) en lugar del valor real, confirmando que se accedió correctamente pero se protegió su visibilidad.

---

## Desafío: Definir y Utilizar Variables de Entorno Personalizadas y Predeterminadas

Crea un nuevo archivo de flujo de trabajo en este directorio (`.github/workflows/`) llamado `coding_custom_env.yml`.

Este flujo de trabajo debe contener un job llamado `test_envs` con los siguientes requisitos:
1.  Define una variable de entorno personalizada llamada `PROYECTO_NOMBRE` con el valor "MiProyectoApp" a nivel del `job`.
2.  Define otra variable de entorno personalizada llamada `VERSION_APP` con el valor "1.0.0" a nivel de un `step` específico dentro del mismo `job`.
3.  En un step, imprime el valor de `PROYECTO_NOMBRE`.
4.  En otro step, imprime el valor de `VERSION_APP`.
5.  En un tercer step, imprime el valor de una variable de entorno predeterminada de GitHub Actions, por ejemplo, `GITHUB_RUN_ID` o `GITHUB_REPOSITORY`.

### Resultado Esperado:
* Un nuevo archivo `D1-02-Secrets-Env-Vars/coding_custom_env.yml` en tu repositorio.
* Una ejecución exitosa del flujo de trabajo.
* Los logs del job `test_envs` deben mostrar los valores correctos para `PROYECTO_NOMBRE`, `VERSION_APP` y la variable predeterminada de GitHub.

---

## Desafío: Depurar un Flujo de Trabajo que Falla al Acceder a Variables de Entorno o Secretos

Crea el archivo `D1-02-Secrets-Env-Vars/debugging_secret_access_fail.yml` con el siguiente contenido (que contiene errores intencionales):

```yaml
# D1-02-Secrets-Env-Vars/.github/workflows/debugging_secret_access_fail.yml
name: Debugging Secret/Env Access

on: [push]

env:
  # Variable de entorno de job definida incorrectamente (sintaxis)
  JOB_ENV_VAR: $incorrect-env-access

jobs:
  access-data:
    runs-on: ubuntu-latest
    steps:
      - name: Try to access job env
        run: echo "Job Env: {{ env.JOB_ENV_VAR }}" # Error: Sintaxis de acceso a variable de entorno en 'run'
      - name: Try to access step env (will fail if above is fixed)
        env:
          STEP_ENV_VAR: "StepValue"
        run: echo "Step Env: $STEP_ENV_VAR"
      - name: Try to access a secret
        run: echo "Secret: ${{ secrets.NON_EXISTENT_SECRET }}" # Error: Secreto inexistente
```