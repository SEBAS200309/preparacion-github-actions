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