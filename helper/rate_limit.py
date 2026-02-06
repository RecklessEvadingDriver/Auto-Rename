"""
Rate limiting system to prevent abuse and spam
Implements token bucket algorithm for fair rate limiting
"""
import time
from typing import Dict, Tuple
from collections import defaultdict

class RateLimiter:
    """Token bucket rate limiter"""
    
    def __init__(self, rate: int, per: int):
        """
        Initialize rate limiter
        
        Args:
            rate: Number of actions allowed
            per: Time period in seconds
        """
        self.rate = rate
        self.per = per
        self.allowance: Dict[int, Tuple[float, float]] = defaultdict(lambda: (rate, time.time()))
    
    def is_allowed(self, user_id: int) -> bool:
        """
        Check if user is allowed to perform action
        
        Args:
            user_id: User's Telegram ID
            
        Returns:
            True if action is allowed, False otherwise
        """
        current = time.time()
        tokens, last_check = self.allowance[user_id]
        
        # Calculate time passed and refill tokens
        time_passed = current - last_check
        tokens += time_passed * (self.rate / self.per)
        
        # Cap tokens at max rate
        if tokens > self.rate:
            tokens = self.rate
        
        # Check if we have at least one token
        if tokens >= 1:
            tokens -= 1
            self.allowance[user_id] = (tokens, current)
            return True
        else:
            self.allowance[user_id] = (tokens, current)
            return False
    
    def get_retry_after(self, user_id: int) -> int:
        """
        Get seconds to wait before retry
        
        Args:
            user_id: User's Telegram ID
            
        Returns:
            Seconds to wait
        """
        tokens, _ = self.allowance[user_id]
        tokens_needed = 1 - tokens
        return int(tokens_needed * (self.per / self.rate)) + 1
    
    def reset(self, user_id: int) -> None:
        """Reset rate limit for user"""
        if user_id in self.allowance:
            del self.allowance[user_id]
    
    def cleanup_old_entries(self, max_age: int = 3600) -> int:
        """
        Remove old entries to save memory
        
        Args:
            max_age: Max age in seconds (default: 1 hour)
            
        Returns:
            Number of entries removed
        """
        current = time.time()
        old_users = [
            user_id for user_id, (_, last_check) in self.allowance.items()
            if current - last_check > max_age
        ]
        
        for user_id in old_users:
            del self.allowance[user_id]
        
        return len(old_users)

# Rate limiters for different operations
# Allow 10 file renames per minute
rename_limiter = RateLimiter(rate=10, per=60)

# Allow 5 commands per 10 seconds
command_limiter = RateLimiter(rate=5, per=10)

# Allow 3 admin commands per minute
admin_command_limiter = RateLimiter(rate=3, per=60)

# Allow 20 messages per minute (general spam prevention)
message_limiter = RateLimiter(rate=20, per=60)
