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