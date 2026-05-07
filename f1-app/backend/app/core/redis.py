import json
import logging
from functools import wraps
from typing import Any, Callable
import redis
from app.config import settings

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize Redis client
try:
    redis_client = redis.from_url(settings.redis_url, decode_responses=True)
    # Test connection
    redis_client.ping()
    logger.info(f"Connected to Redis at {settings.redis_url}")
except Exception as e:
    logger.warning(f"Failed to connect to Redis: {e}. Caching will be disabled.")
    redis_client = None

def cache_response(expire_seconds: int = 3600):
    """
    Decorator to cache API responses in Redis.
    """
    def decorator(func: Callable):
        @wraps(func)
        def wrapper(*args, **kwargs) -> Any:
            if redis_client is None:
                return func(*args, **kwargs)

            # Generate a unique cache key based on function name and arguments
            # Filter out the DB session and other non-serializable objects
            cache_kwargs = {k: v for k, v in kwargs.items() if k not in ['db', 'session']}
            key_parts = [func.__name__]
            if args:
                # Only include simple types in key parts from args
                key_parts.append(str([a for a in args if isinstance(a, (str, int, float, bool))]))
            if cache_kwargs:
                key_parts.append(str(sorted(cache_kwargs.items())))
            
            cache_key = f"api_cache:{':'.join(key_parts)}"
            
            try:
                # Try to get from cache
                cached_val = redis_client.get(cache_key)
                if cached_val:
                    logger.info(f"Cache hit for {cache_key}")
                    return json.loads(cached_val)
            except Exception as e:
                logger.error(f"Redis cache error: {e}")

            # Execute the actual function
            result = func(*args, **kwargs)

            # Only cache successful results (not errors represented as dicts with "Error")
            if isinstance(result, dict) and "Error" in result:
                return result

            try:
                # Store in cache
                redis_client.setex(
                    cache_key,
                    expire_seconds,
                    json.dumps(result)
                )
                logger.info(f"Cached response for {cache_key}")
            except Exception as e:
                logger.error(f"Redis storage error: {e}")

            return result
        return wrapper
    return decorator
