"""
File processing queue system for efficient concurrent file handling
Prevents system overload by managing file processing requests
"""
import asyncio
from typing import Dict, Callable, Any
from datetime import datetime
import logging

logger = logging.getLogger(__name__)

class FileProcessingQueue:
    """Manages file processing with concurrency limits"""
    
    def __init__(self, max_concurrent: int = 5):
        """
        Initialize file processing queue
        
        Args:
            max_concurrent: Maximum concurrent file processing tasks
        """
        self.max_concurrent = max_concurrent
        self.semaphore = asyncio.Semaphore(max_concurrent)
        self.active_tasks: Dict[int, Dict[str, Any]] = {}
        self.queue_size = 0
        
    async def process(self, user_id: int, task_func: Callable, *args, **kwargs) -> Any:
        """
        Process a file task with concurrency control
        
        Args:
            user_id: User's Telegram ID
            task_func: Async function to execute
            *args, **kwargs: Arguments for the task function
            
        Returns:
            Result from task function
        """
        self.queue_size += 1
        
        async with self.semaphore:
            # Track active task
            self.active_tasks[user_id] = {
                'started_at': datetime.now(),
                'function': task_func.__name__
            }
            
            try:
                logger.info(f"Processing file for user {user_id} - Queue: {self.get_queue_status()}")
                result = await task_func(*args, **kwargs)
                return result
            finally:
                # Clean up
                if user_id in self.active_tasks:
                    del self.active_tasks[user_id]
                self.queue_size -= 1
    
    def is_user_processing(self, user_id: int) -> bool:
        """Check if user has an active processing task"""
        return user_id in self.active_tasks
    
    def get_user_task_info(self, user_id: int) -> Dict[str, Any]:
        """Get information about user's active task"""
        return self.active_tasks.get(user_id, {})
    
    def get_active_count(self) -> int:
        """Get number of active processing tasks"""
        return len(self.active_tasks)
    
    def get_queue_status(self) -> str:
        """Get queue status string"""
        return f"{self.get_active_count()}/{self.max_concurrent} active, {self.queue_size} in queue"
    
    async def cancel_user_task(self, user_id: int) -> bool:
        """
        Cancel a user's processing task
        
        Args:
            user_id: User's Telegram ID
            
        Returns:
            True if task was found and cancelled
        """
        if user_id in self.active_tasks:
            del self.active_tasks[user_id]
            logger.info(f"Cancelled task for user {user_id}")
            return True
        return False

# Global file processing queue
# Adjust max_concurrent based on your server resources
file_queue = FileProcessingQueue(max_concurrent=5)
