"""
User analytics and statistics module
Provides insights into bot usage and user behavior
"""
from datetime import datetime, timedelta
from typing import Dict, List
import logging

logger = logging.getLogger(__name__)

class Analytics:
    """Bot analytics and statistics"""
    
    def __init__(self, database):
        """
        Initialize analytics
        
        Args:
            database: Database instance
        """
        self.db = database
    
    async def get_user_stats(self, user_id: int) -> Dict:
        """
        Get statistics for a specific user
        
        Args:
            user_id: User's Telegram ID
            
        Returns:
            Dictionary with user statistics
        """
        try:
            user = await self.db.get_user(user_id)
            
            if not user:
                return {}
            
            stats = {
                'user_id': user_id,
                'username': user.get('username', 'Unknown'),
                'join_date': user.get('join_date', 'Unknown'),
                'rename_count': user.get('rename_count', 0),
                'is_premium': user.get('is_premium', False),
                'has_custom_format': bool(user.get('format_template')),
                'has_custom_thumbnail': bool(user.get('file_id')),
                'has_custom_caption': bool(user.get('caption')),
            }
            
            return stats
            
        except Exception as e:
            logger.error(f"Error getting user stats: {e}")
            return {}
    
    async def get_bot_stats(self) -> Dict:
        """
        Get overall bot statistics
        
        Returns:
            Dictionary with bot statistics
        """
        try:
            total_users = await self.db.total_users_count()
            premium_users = await self.db.all_premium_users()
            
            # Get users from last 24 hours
            yesterday = datetime.now() - timedelta(days=1)
            recent_users = 0
            
            all_users = await self.db.get_all_users()
            async for user in all_users:
                join_date_str = user.get('join_date')
                if join_date_str:
                    try:
                        join_date = datetime.fromisoformat(join_date_str)
                        if join_date > yesterday:
                            recent_users += 1
                    except:
                        pass
            
            stats = {
                'total_users': total_users,
                'premium_users': premium_users,
                'new_users_24h': recent_users,
                'timestamp': datetime.now().isoformat()
            }
            
            return stats
            
        except Exception as e:
            logger.error(f"Error getting bot stats: {e}")
            return {}
    
    async def get_top_users(self, limit: int = 10) -> List[Dict]:
        """
        Get top users by rename count
        
        Args:
            limit: Number of users to return
            
        Returns:
            List of user dictionaries
        """
        try:
            all_users = await self.db.get_all_users()
            users_list = []
            
            async for user in all_users:
                users_list.append({
                    'user_id': user.get('_id'),
                    'username': user.get('username', 'Unknown'),
                    'rename_count': user.get('rename_count', 0)
                })
            
            # Sort by rename count
            users_list.sort(key=lambda x: x['rename_count'], reverse=True)
            
            return users_list[:limit]
            
        except Exception as e:
            logger.error(f"Error getting top users: {e}")
            return []
    
    async def increment_rename_count(self, user_id: int) -> bool:
        """
        Increment rename count for user
        
        Args:
            user_id: User's Telegram ID
            
        Returns:
            True if successful
        """
        try:
            user = await self.db.get_user(user_id)
            if user:
                user['rename_count'] = user.get('rename_count', 0) + 1
                await self.db.update_user(user)
                return True
            return False
        except Exception as e:
            logger.error(f"Error incrementing rename count: {e}")
            return False
