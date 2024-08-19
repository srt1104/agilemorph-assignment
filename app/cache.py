from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend
import redis

# Setup Redis connection
try:
    redis_client = redis.Redis(host='localhost', port=6379, db=0)
    print("Connected to Redis.")
except redis.ConnectionError as e:
    redis_client = None
    print(f"Failed to connect to Redis: {e}")


# Initialize FastAPI Cache
def init_cache():
    """
    Initializes the cache backend for FastAPI using Redis.
    """
    if redis_client:
        FastAPICache.init(RedisBackend(redis_client), prefix="my-cache")
        print('Cache initialized!')
    else:
        print("Redis connection is not available, skipping cache initialization.")
