import logging
from motor.motor_asyncio import AsyncIOMotorClient
from app.core.config import settings

logger = logging.getLogger(__name__)

class Database:
    """
    Singleton class to manage MongoDB connection pooling.
    """
    client: AsyncIOMotorClient = None
    db = None

db = Database()

async def connect_to_mongo():
    """
    Called on app startup to initialize the connection pool.
    """
    try:
        db.client = AsyncIOMotorClient(
            settings.DATABASE_URL,
            maxPoolSize=10,
            minPoolSize=1,
            serverSelectionTimeoutMS=5000
        )
        # Check if the connection is successful by pinging the server
        await db.client.admin.command('ping')
        db.db = db.client.get_database("wikikisan")
        logger.info("✅ Successfully connected to MongoDB.")
    except Exception as e:
        logger.error(f"❌ Could not connect to MongoDB: {e}")
        raise e

async def close_mongo_connection():
    """
    Called on app shutdown to close all active connections.
    """
    if db.client:
        db.client.close()
        logger.info("🔌 MongoDB connection closed.")

def get_db():
    """
    Dependency to be used in FastAPI routes.
    """
    return db.db
