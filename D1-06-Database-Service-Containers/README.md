# Concepto a Resolver: Ejecución de Servicios de Base de Datos en GitHub Actions

Este concepto explora cómo configurar y utilizar servicios de bases de datos, como PostgreSQL, MySQL o Redis, directamente dentro de tus flujos de trabajo de GitHub Actions para pruebas o tareas que requieran una base de datos efímera.


## Desafío 1: PostgreSQL Básico para Pruebas Unitarias

Configura un servicio de PostgreSQL para ejecutar pruebas unitarias que requieren una base de datos.

**Archivos a crear:**

  - `.github/workflows/test-with-postgres.yml` (TÚ DEBES CREARLO)
  - `test_db_connection.py` (proporcionado)

**Archivos de apoyo proporcionados:**

```python
# test_db_connection.py - Script de prueba de conexión a PostgreSQL
import os
import psycopg2

def test_connection():
    try:
        conn = psycopg2.connect(
            host=os.getenv('DB_HOST', 'localhost'),
            database=os.getenv('DB_NAME', 'testdb'),
            user=os.getenv('DB_USER', 'user'),
            password=os.getenv('DB_PASSWORD', 'password')
        )
        cursor = conn.cursor()
        cursor.execute("SELECT 1")
        result = cursor.fetchone()[0]
        conn.close()
        print(f"Conexión exitosa a PostgreSQL. Resultado de la consulta: {result}")
        return True
    except Exception as e:
        print(f"Error al conectar o consultar la base de datos: {e}")
        return False

if __name__ == "__main__":
    if test_connection():
        exit(0)
    else:
        exit(1)
```

**Instrucciones del workflow:**
Tu workflow debe:

  - Activarse en el evento `push` a la rama `main`.
  - Definir un trabajo que utilice un contenedor de servicio de PostgreSQL.
  - Asegurarse de que el servicio de PostgreSQL esté disponible para el contenedor principal del trabajo.
  - Establecer las variables de entorno necesarias para la conexión a la base de datos dentro del trabajo.
  - Instalar `psycopg2` en el paso de Python.
  - Ejecutar el script `test_db_connection.py` para verificar la conexión a la base de datos.

### Resultado Esperado:

  - El workflow se ejecuta exitosamente en cada `push` a `main`.
  - El log del trabajo muestra la instalación de `psycopg2`.
  - El log del trabajo muestra el mensaje "Conexión exitosa a PostgreSQL."

-----

## Desafío 2: Servicio Redis para Cacheo de Aplicaciones

Implementa un servicio de Redis para simular un almacenamiento en caché en tu aplicación.

**Archivos a crear:**

  - `.github/workflows/redis-cache-simulation.yml` (TÚ DEBES CREARLO)
  - `simulate_cache.py` (proporcionado)

**Archivos de apoyo proporcionados:**

```python
# simulate_cache.py - Script de simulación de cacheo con Redis
import os
import redis

def simulate_cache_operations():
    try:
        r = redis.Redis(
            host=os.getenv('REDIS_HOST', 'localhost'),
            port=int(os.getenv('REDIS_PORT', 6379)),
            db=0
        )
        print("Conectado a Redis.")
        r.set('mykey', 'myvalue')
        value = r.get('mykey')
        print(f"Obtenido de Redis: mykey = {value.decode('utf-8')}")
        r.delete('mykey')
        print("Clave 'mykey' eliminada.")
        return True
    except Exception as e:
        print(f"Error al conectar o realizar operaciones en Redis: {e}")
        return False

if __name__ == "__main__":
    if simulate_cache_operations():
        exit(0)
    else:
        exit(1)
```

**Instrucciones del workflow:**
Tu workflow debe:

  - Activarse manualmente con `workflow_dispatch`.
  - Definir un trabajo que utilice un contenedor de servicio de Redis.
  - Asegurarse de que el servicio de Redis esté accesible desde el contenedor principal.
  - Establecer las variables de entorno `REDIS_HOST` y `REDIS_PORT` para el script de Python.
  - Instalar la librería `redis` de Python.
  - Ejecutar el script `simulate_cache.py` para interactuar con el servicio Redis.

### Resultado Esperado:

  - El workflow puede ser ejecutado manualmente.
  - Los logs del trabajo muestran la conexión exitosa a Redis y las operaciones de `set`, `get` y `delete`.
  - El trabajo finaliza exitosamente.

-----

## Desafío 3: Configuración de Múltiples Servicios de Base de Datos

Crea un workflow que levante dos servicios de base de datos diferentes, como MySQL y PostgreSQL, y verifique su accesibilidad.

**Archivos a crear:**

  - `.github/workflows/multi-db-services.yml` (TÚ DEBES CREARLO)
  - `check_mysql_connection.py` (proporcionado)
  - `check_postgres_connection.py` (proporcionado)

**Archivos de apoyo proporcionados:**

```python
# check_mysql_connection.py - Script de prueba de conexión a MySQL
import os
import mysql.connector

def test_mysql_connection():
    try:
        conn = mysql.connector.connect(
            host=os.getenv('MYSQL_HOST', 'localhost'),
            database=os.getenv('MYSQL_DB', 'test_mysql_db'),
            user=os.getenv('MYSQL_USER', 'user'),
            password=os.getenv('MYSQL_PASSWORD', 'password')
        )
        cursor = conn.cursor()
        cursor.execute("SELECT 1")
        result = cursor.fetchone()[0]
        conn.close()
        print(f"Conexión exitosa a MySQL. Resultado de la consulta: {result}")
        return True
    except Exception as e:
        print(f"Error al conectar o consultar MySQL: {e}")
        return False

if __name__ == "__main__":
    if test_mysql_connection():
        exit(0)
    else:
        exit(1)
```

```python
# check_postgres_connection.py - Script de prueba de conexión a PostgreSQL
import os
import psycopg2

def test_postgres_connection():
    try:
        conn = psycopg2.connect(
            host=os.getenv('PG_HOST', 'localhost'),
            database=os.getenv('PG_DB', 'test_pg_db'),
            user=os.getenv('PG_USER', 'user'),
            password=os.getenv('PG_PASSWORD', 'password')
        )
        cursor = conn.cursor()
        cursor.execute("SELECT 1")
        result = cursor.fetchone()[0]
        conn.close()
        print(f"Conexión exitosa a PostgreSQL. Resultado de la consulta: {result}")
        return True
    except Exception as e:
        print(f"Error al conectar o consultar PostgreSQL: {e}")
        return False

if __name__ == "__main__":
    if test_postgres_connection():
        exit(0)
    else:
        exit(1)
```

**Instrucciones del workflow:**
Tu workflow debe:

  - Activarse en cada `pull_request` a la rama `main`.
  - Configurar dos servicios de base de datos: uno de **MySQL** y otro de **PostgreSQL** dentro del mismo trabajo.
  - Asegurarse de que ambos servicios estén disponibles para el contenedor principal del trabajo.
  - Establecer las variables de entorno necesarias para la conexión a cada base de datos (host, db, user, password) para ambos scripts.
  - Instalar `mysql-connector-python` y `psycopg2`.
  - Ejecutar `check_mysql_connection.py` y `check_postgres_connection.py` en pasos separados para verificar la conectividad.

### Resultado Esperado:

  - El workflow se activa en cada PR.
  - Ambos scripts de Python se ejecutan y sus logs muestran "Conexión exitosa a MySQL." y "Conexión exitosa a PostgreSQL."
  - El trabajo finaliza exitosamente.

-----

# Concepto a Resolver: Resolución de Problemas/Debugging en Servicios de Contenedores

Este concepto se enfoca en la identificación y corrección de errores comunes al configurar y utilizar servicios de contenedores en GitHub Actions, incluyendo problemas de conectividad, variables de entorno y configuración de puertos.

-----

## Desafío 4: Depuración de Servicio de Base de Datos con Errores

Debes identificar y corregir los errores en un workflow existente que intenta levantar un servicio de base de datos MySQL y conectarse a él.

**Archivos a crear:**

  - `.github/workflows/debug-mysql-service.yml` (NO LO CREES, YA ESTÁ PROPORCIONADO CON ERRORES)
  - `faulty_db_connection.py` (proporcionado)

**Archivos de apoyo proporcionados:**

```yaml
# .github/workflows/debug-mysql-service.yml (CON ERRORES INTENCIONALES)
name: Debug MySQL Service

on: [push]

jobs:
  test-mysql-connection:
    runs-on: ubuntu-latest
    services:
      mysql:
        image: mysql:8.0
        env:
          MYSQL_DATABASE: myappdb
          MYSQL_USER: myuser
          MYSQL_PASSWORD: mypassword
        ports:
          - 3306:3306
    steps:
    - name: Checkout code
      uses: actions/checkout@v4

    - name: Set up Python
      uses: actions/setup-python@v5
      with:
        python-version: '3.9'

    - name: Install dependencies
      run: pip install mysql-connector-python

    - name: Wait for MySQL to be ready
      run: sleep 10 # Waiting for DB to start

    - name: Test DB connection
      run: python faulty_db_connection.py
      env:
        MYSQL_HOST: localhost
        MYSQL_DB: myappdb
        MYSQL_USER: myuser
        MYSQL_PASSWORD: mypassword
```

```python
# faulty_db_connection.py - Script de prueba de conexión a MySQL
import os
import mysql.connector
import time

def test_mysql_connection():
    max_attempts = 5
    for attempt in range(max_attempts):
        try:
            conn = mysql.connector.connect(
                host=os.getenv('MYSQL_HOST'),
                database=os.getenv('MYSQL_DB'),
                user=os.getenv('MYSQL_USER'),
                password=os.getenv('MYSQL_PASSWORD'),
                port=3306 # Asegúrate de que el puerto sea el correcto
            )
            cursor = conn.cursor()
            cursor.execute("SELECT 1")
            result = cursor.fetchone()[0]
            conn.close()
            print(f"Conexión exitosa a MySQL. Resultado de la consulta: {result}")
            return True
        except mysql.connector.Error as err:
            print(f"Intento {attempt + 1}: Error al conectar o consultar MySQL: {err}")
            if attempt < max_attempts - 1:
                time.sleep(5) # Espera antes de reintentar
    return False

if __name__ == "__main__":
    if test_mysql_connection():
        exit(0)
    else:
        exit(1)
```

**Instrucciones del workflow:**
Tu objetivo es **corregir** el workflow `.github/workflows/debug-mysql-service.yml` proporcionado para que el script `faulty_db_connection.py` se conecte exitosamente al servicio MySQL.

**Pistas sutiles:**

  - Presta atención a cómo los servicios de contenedores se comunican con el contenedor principal. ¿Hay algún detalle faltante o incorrecto en la configuración del servicio?
  - Revisa cómo se exponen y acceden los puertos de los servicios.
  - Asegúrate de que las variables de entorno para la conexión a la base de datos se propaguen correctamente y sean consistentes.
  - Observa detenidamente los mensajes de error en los logs de GitHub Actions cuando el workflow falle.

### Resultado Esperado:

  - El workflow corregido se ejecuta exitosamente.
  - El log del paso "Test DB connection" muestra "Conexión exitosa a MySQL."
  - El trabajo finaliza con un estado de éxito (verde).