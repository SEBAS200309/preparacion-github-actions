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
