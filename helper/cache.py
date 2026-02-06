"""
Simple in-memory caching system for frequently accessed data
Helps reduce database queries and improve performance
"""
import time
from typing import Any, Optional

class SimpleCache:
    """Thread-safe simple cache with TTL support"""
    
    def __init__(self, default_ttl: int = 300):
        """
        Initialize cache
        
        Args:
            default_ttl: Default time-to-live in seconds (default: 5 minutes)
        """
        self._cache = {}
        self._default_ttl = default_ttl
    
    def get(self, key: str) -> Optional[Any]:
        """
        Get value from cache
        
        Args:
            key: Cache key
            
        Returns:
            Cached value or None if not found or expired
        """
        if key not in self._cache:
            return None
        
        value, expiry = self._cache[key]
        
        # Check if expired
        if time.time() > expiry:
            del self._cache[key]
            return None
        
        return value
    
    def set(self, key: str, value: Any, ttl: Optional[int] = None) -> None:
        """
        Set value in cache
        
        Args:
            key: Cache key
            value: Value to cache
            ttl: Time-to-live in seconds (uses default if not specified)
        """
        ttl = ttl or self._default_ttl
        expiry = time.time() + ttl
        self._cache[key] = (value, expiry)
    
    def delete(self, key: str) -> None:
        """
        Delete value from cache
        
        Args:
            key: Cache key
        """
        if key in self._cache:
            del self._cache[key]
    
    def clear(self) -> None:
        """Clear all cached values"""
        self._cache.clear()
    
    def cleanup_expired(self) -> int:
        """
        Remove expired entries from cache
        
        Returns:
            Number of entries removed
        """
        current_time = time.time()
        expired_keys = [
            key for key, (_, expiry) in self._cache.items() 
            if current_time > expiry
        ]
        
        for key in expired_keys:
            del self._cache[key]
        
        return len(expired_keys)
    
    def size(self) -> int:
        """Get current cache size"""
        return len(self._cache)

# Global cache instances
user_cache = SimpleCache(ttl=300)  # 5 minutes for user data
admin_cache = SimpleCache(ttl=600)  # 10 minutes for admin list
channel_cache = SimpleCache(ttl=600)  # 10 minutes for channel list
verification_cache = SimpleCache(ttl=180)  # 3 minutes for verification status
