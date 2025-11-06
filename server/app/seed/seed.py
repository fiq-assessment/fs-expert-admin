"""Seed database with users, products, and orders"""
import asyncio
from datetime import datetime, timedelta
import random
from motor.motor_asyncio import AsyncIOMotorClient
from bson import ObjectId
import sys
sys.path.append('..')
from app.core.auth import hash_password

MONGODB_URI = "mongodb://fiqtestuser:F9dAd0e0w!!%40@mysql1.interview.servers.fulfillmentiq.com:27017/fiqtest?authMechanism=SCRAM-SHA-1&authSource=admin"
DB_NAME = "fiqtest"

async def seed_data():
    client = AsyncIOMotorClient(MONGODB_URI)
    db = client[DB_NAME]
    
    # Clear existing data
    await db.users.delete_many({})
    await db.products.delete_many({})
    await db.orders.delete_many({})
    
    # Create users
    users = []
    for email, password, role in [
        ("admin@example.com", "admin123", "admin"),
        ("editor@example.com", "editor123", "editor"),
        ("viewer@example.com", "viewer123", "viewer")
    ]:
        result = await db.users.insert_one({
            "email": email,
            "password": hash_password(password),
            "role": role,
            "createdAt": datetime.utcnow()
        })
        users.append({"id": str(result.inserted_id), "email": email, "role": role})
        print(f"✓ Created {role}: {email} / {password}")
    
    # Create products
    product_ids = []
    for i in range(15):
        result = await db.products.insert_one({
            "name": f"Product {i+1}",
            "description": f"Description for product {i+1}",
            "priceCents": random.randint(1000, 50000),
            "stock": random.randint(10, 100),
            "category": random.choice(["Electronics", "Books", "Apparel"]),
            "createdAt": datetime.utcnow() - timedelta(days=random.randint(0, 60)),
            "updatedAt": datetime.utcnow()
        })
        product_ids.append(result.inserted_id)
    
    print(f"✓ Created {len(product_ids)} products")
    
    # Create orders
    for i in range(50):
        num_items = random.randint(1, 3)
        order_items = []
        
        for _ in range(num_items):
            product_id = random.choice(product_ids)
            product = await db.products.find_one({"_id": product_id})
            order_items.append({
                "productId": str(product_id),
                "productName": product["name"],
                "qty": random.randint(1, 3),
                "priceCents": product["priceCents"]
            })
        
        await db.orders.insert_one({
            "userId": users[0]["id"],
            "items": order_items,
            "totalCents": sum(item["qty"] * item["priceCents"] for item in order_items),
            "status": "confirmed",
            "createdAt": datetime.utcnow() - timedelta(days=random.randint(0, 30))
        })
    
    print(f"✓ Created 50 orders")
    
    client.close()

if __name__ == "__main__":
    asyncio.run(seed_data())

