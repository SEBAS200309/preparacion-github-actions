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