import asyncio
from motor.motor_asyncio import AsyncIOMotorClient
from datetime import datetime

# Database Connection
MONGO_URL = "mongodb://localhost:27017"
client = AsyncIOMotorClient(MONGO_URL)
db = client["wikikisan"]

crop_data = [
    {
        "crop_name": "Chilli (Red)",
        "optimal_temperature": "20°C - 30°C",
        "soil_type": "Black soil or Well-drained loamy soil",
        "sowing_period": "July to August",
        "harvesting_time": "60-90 days after flowering",
        "common_diseases": ["Damping off", "Fruit rot", "Powdery mildew"],
        "is_wiki_article": True,
        "last_updated": datetime.now()
    },
    {
        "crop_name": "Paddy (Rice)",
        "optimal_temperature": "25°C - 35°C",
        "soil_type": "Clayey or Loamy soil (Water-retaining)",
        "sowing_period": "June (Kharif), November (Rabi)",
        "harvesting_time": "100-150 days",
        "common_diseases": ["Blast", "Blight", "Brown spot"],
        "is_wiki_article": True,
        "last_updated": datetime.now()
    }
]

async def seed_wiki():
    print("📚 Seeding Crop Wiki Library...")
    # Using 'wiki' collection
    collection = db["wiki"]
    
    # Clear existing wiki data to avoid duplicates
    await collection.delete_many({"is_wiki_article": True})
    
    result = await collection.insert_many(crop_data)
    print(f"✅ Successfully seeded {len(result.inserted_ids)} crop articles.")

if __name__ == "__main__":
    asyncio.run(seed_wiki())
