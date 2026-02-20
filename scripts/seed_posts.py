import requests
import json
from datetime import datetime

# URL of your local FastAPI server
API_URL = "http://localhost:8000/api/v1/community/posts"

farmer_posts = [
    {
        "title": "Best organic pesticide for Gadwal Red Chilli?",
        "content": "I am seeing some white spots on my chilli leaves. Is there a natural neem-based solution?",
        "type": "question",
        "category": "crops",
        "language": "en",
        "tags": ["chilli", "organic", "pests"]
    },
    {
        "title": "Success Story: 20% increase in Paddy yield",
        "content": "By switching to the SRI (System of Rice Intensification) method, I saved water and got a better harvest.",
        "type": "success_story",
        "category": "crops",
        "language": "en",
        "tags": ["paddy", "innovation", "water-saving"]
    },
    {
        "title": "వరి సాగులో మెళకువలు (Paddy Farming Tips)",
        "content": "ఈ ఖరీఫ్ సీజన్‌లో వరి సాగు చేసే రైతులకు కొన్ని ముఖ్యమైన సూచనలు...",
        "type": "tip",
        "category": "crops",
        "language": "te",
        "tags": ["వరి", "ఖరీఫ్"]
    }
]

def seed_community():
    print("🌱 Seeding Farmer Discussions...")
    for post in farmer_posts:
        response = requests.post(API_URL, json=post)
        if response.status_code == 201:
            print(f"✅ Created: {post['title']}")
        else:
            print(f"❌ Failed: {post['title']} - {response.text}")

if __name__ == "__main__":
    seed_community()
