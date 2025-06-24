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