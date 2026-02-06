"""
Database indexes configuration for optimal query performance
Run this script once after setting up your MongoDB database
"""
import asyncio
import sys
from helper.database import rexbots

async def create_indexes():
    """Create database indexes for better query performance"""
    print("🔄 Creating database indexes...")
    
    try:
        # User collection indexes
        await rexbots.col.create_index("_id")
        await rexbots.col.create_index("username")
        await rexbots.col.create_index("expiry_time")
        await rexbots.col.create_index([("ban_status.is_banned", 1)])
        print("✅ User collection indexes created")
        
        # Verification data indexes
        await rexbots.verification_data.create_index([("user_id", 1), ("verified_at", -1)])
        await rexbots.verification_data.create_index("date")
        print("✅ Verification data indexes created")
        
        # Premium users indexes  
        await rexbots.col.create_index([("is_premium", 1), ("expiry_time", -1)])
        print("✅ Premium users indexes created")
        
        # Force subscribe channels indexes
        await rexbots.fsub_data.create_index("_id")
        await rexbots.fsub_data.create_index("mode")
        print("✅ Force subscribe indexes created")
        
        # Request force subscribe indexes
        await rexbots.rqst_fsub_Channel_data.create_index([("_id", 1), ("user_ids", 1)])
        print("✅ Request force subscribe indexes created")
        
        # Admin collection indexes
        await rexbots.admins_data.create_index("_id")
        print("✅ Admin collection indexes created")
        
        # Banned users indexes
        await rexbots.banned_users.create_index([("ban_status.is_banned", 1)])
        await rexbots.banned_users.create_index("ban_status.banned_on")
        print("✅ Banned users indexes created")
        
        print("\n✨ All database indexes created successfully!")
        print("📊 Your database is now optimized for better performance")
        
    except Exception as e:
        print(f"❌ Error creating indexes: {e}")
        sys.exit(1)

if __name__ == "__main__":
    asyncio.run(create_indexes())
