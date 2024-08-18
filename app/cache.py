from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend
import redis

# Setup Redis connection
try:
    redis_client = redis.Redis(host='localhost', port=6379, db=0)
    print("Connected to Redis.")
except redis.ConnectionError as e:
    print(f"Redis connection error: {e}")


# Initialize FastAPI Cache
def init_cache():
    FastAPICache.init(RedisBackend(redis_client), prefix="fastapi-cache")
    print('Cache initialized!')
