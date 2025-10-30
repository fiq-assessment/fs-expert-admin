from motor.motor_asyncio import AsyncIOMotorClient
import redis.asyncio as redis
from .config import settings

client = AsyncIOMotorClient(settings.MONGODB_URI)
db = client[settings.DB_NAME]
redis_client = redis.from_url(settings.REDIS_URL, decode_responses=True)

async def init_db():
    """Initialize database indexes"""
    await db.users.create_index([("email", 1)], unique=True)
    await db.users.create_index([("role", 1)])
    await db.products.create_index([("category", 1)])
    await db.products.create_index([("createdAt", -1)])
    await db.orders.create_index([("userId", 1)])
    await db.orders.create_index([("createdAt", -1)])
    print("✓ Database indexes created")

async def invalidate_stats_cache():
    """Invalidate cached statistics"""
    await redis_client.delete("stats:top_products")

