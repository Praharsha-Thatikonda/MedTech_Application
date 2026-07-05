import json
import os
try:
    import redis
except ImportError:
    redis = None

class CacheStore:
    """
    Manages Key-Value Store (Redis) for Short-Term Memory.
    Used for Chat History and Session Caching.
    Falls back to In-Memory Dict or File if Redis is unavailable.
    """
    def __init__(self, host='localhost', port=6379, db=0):
        self.redis_client = None
        self.local_cache = {}
        self.use_redis = False
        
        if redis:
            try:
                self.redis_client = redis.Redis(host=host, port=port, db=db, decode_responses=True)
                # Quick ping to check connection
                self.redis_client.ping()
                self.use_redis = True
                print(f"[CacheStore] Redis connected on {host}:{port}")
            except Exception as e:
                print(f"[CacheStore] Redis connection failed: {e}. Using local memory.")
        else:
            print("[CacheStore] redis-py not installed. Using local memory.")

    def set_session_history(self, session_id, messages):
        """
        Stores chat history list for a session.
        """
        data = json.dumps(messages)
        if self.use_redis:
            try:
                self.redis_client.setex(f"session:{session_id}", 3600, data) # Expire in 1 hr
            except Exception as e:
                print(f"[CacheStore] Redis set failed: {e}")
                self.local_cache[session_id] = data
        else:
            self.local_cache[session_id] = data

    def get_session_history(self, session_id):
        """
        Retrieves chat history.
        """
        if self.use_redis:
            try:
                data = self.redis_client.get(f"session:{session_id}")
                if data:
                    return json.loads(data)
            except Exception as e:
                print(f"[CacheStore] Redis get failed: {e}")
        
        # Fallback
        data = self.local_cache.get(session_id)
        return json.loads(data) if data else []

    def clear_session(self, session_id):
        if self.use_redis:
            try:
                self.redis_client.delete(f"session:{session_id}")
            except:
                pass
        self.local_cache.pop(session_id, None)

# Singleton
cache_store = CacheStore()
