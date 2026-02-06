#!/usr/bin/env python3
"""
Maintenance script for Auto-Rename Bot
Performs cleanup and optimization tasks
"""
import asyncio
import sys
from datetime import datetime, timedelta
from helper.database import rexbots
from helper.cache import user_cache, admin_cache, channel_cache, verification_cache
from helper.rate_limit import (
    rename_limiter, command_limiter, 
    admin_command_limiter, message_limiter
)
import logging

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

async def cleanup_expired_premium():
    """Remove expired premium users"""
    logger.info("🔄 Checking for expired premium users...")
    try:
        expired_users = await rexbots.get_expired()
        count = 0
        for user in expired_users:
            await rexbots.remove_premium_access(user['_id'])
            count += 1
        logger.info(f"✅ Removed {count} expired premium users")
        return count
    except Exception as e:
        logger.error(f"❌ Error cleaning expired premium: {e}")
        return 0

def cleanup_rate_limiters():
    """Clean up old rate limiter entries"""
    logger.info("🔄 Cleaning up rate limiter data...")
    try:
        total = 0
        total += rename_limiter.cleanup_old_entries()
        total += command_limiter.cleanup_old_entries()
        total += admin_command_limiter.cleanup_old_entries()
        total += message_limiter.cleanup_old_entries()
        logger.info(f"✅ Removed {total} old rate limiter entries")
        return total
    except Exception as e:
        logger.error(f"❌ Error cleaning rate limiters: {e}")
        return 0

def cleanup_caches():
    """Clean up expired cache entries"""
    logger.info("🔄 Cleaning up cache data...")
    try:
        total = 0
        total += user_cache.cleanup_expired()
        total += admin_cache.cleanup_expired()
        total += channel_cache.cleanup_expired()
        total += verification_cache.cleanup_expired()
        logger.info(f"✅ Removed {total} expired cache entries")
        return total
    except Exception as e:
        logger.error(f"❌ Error cleaning caches: {e}")
        return 0

async def show_statistics():
    """Display bot statistics"""
    logger.info("📊 Gathering statistics...")
    try:
        total_users = await rexbots.total_users_count()
        premium_users = await rexbots.all_premium_users()
        admins = await rexbots.get_all_admins()
        channels = await rexbots.show_channels()
        
        logger.info("=" * 50)
        logger.info("📊 BOT STATISTICS")
        logger.info("=" * 50)
        logger.info(f"Total Users: {total_users}")
        logger.info(f"Premium Users: {premium_users}")
        logger.info(f"Admins: {len(admins)}")
        logger.info(f"Force Subscribe Channels: {len(channels)}")
        logger.info(f"User Cache Size: {user_cache.size()}")
        logger.info(f"Admin Cache Size: {admin_cache.size()}")
        logger.info(f"Channel Cache Size: {channel_cache.size()}")
        logger.info("=" * 50)
    except Exception as e:
        logger.error(f"❌ Error getting statistics: {e}")

async def main():
    """Main maintenance routine"""
    logger.info("🚀 Starting maintenance tasks...")
    logger.info(f"⏰ Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    # Show current statistics
    await show_statistics()
    
    # Cleanup tasks
    logger.info("\n🧹 Starting cleanup tasks...")
    
    premium_cleaned = await cleanup_expired_premium()
    rate_limiter_cleaned = cleanup_rate_limiters()
    cache_cleaned = cleanup_caches()
    
    # Summary
    logger.info("\n" + "=" * 50)
    logger.info("✅ MAINTENANCE SUMMARY")
    logger.info("=" * 50)
    logger.info(f"Expired Premium Removed: {premium_cleaned}")
    logger.info(f"Rate Limiter Entries Cleaned: {rate_limiter_cleaned}")
    logger.info(f"Cache Entries Cleaned: {cache_cleaned}")
    logger.info("=" * 50)
    
    # Show updated statistics
    logger.info("\n")
    await show_statistics()
    
    logger.info("\n✨ Maintenance completed successfully!")

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.info("\n⚠️  Maintenance interrupted by user")
        sys.exit(0)
    except Exception as e:
        logger.error(f"\n❌ Fatal error during maintenance: {e}")
        sys.exit(1)
