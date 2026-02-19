
from fastapi import APIRouter, HTTPException
import requests
import os
from datetime import datetime

router = APIRouter()

# You would get this from https://openweathermap.org/api
OPENWEATHER_API_KEY = os.getenv("OPENWEATHER_API_KEY", "your_api_key_here")

def analyze_farming_conditions(temp, humidity, rain):
    """
    Business logic to provide actionable advice to farmers.
    """
    advice = "Conditions are normal for general farming."
    if rain > 0:
        advice = "Rain detected. Avoid spraying pesticides or fertilizers today."
    elif humidity > 80 and temp > 25:
        advice = "High humidity & heat: Increased risk of fungal infections in crops like Chillies."
    elif temp > 35:
        advice = "Extreme heat: Ensure evening irrigation to prevent crop wilting."
        
    return advice

@router.get("/current/{city}")
async def get_weather_analysis(city: str):
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={OPENWEATHER_API_KEY}&units=metric"
    
    try:
        response = requests.get(url).json()
        if response.get("cod") != 200:
            raise HTTPException(status_code=400, detail="City not found")
            
        temp = response["main"]["temp"]
        humidity = response["main"]["humidity"]
        rain = response.get("rain", {}).get("1h", 0)
        
        analysis = analyze_farming_conditions(temp, humidity, rain)
        
        return {
            "success": True,
            "data": {
                "city": response["name"],
                "temperature": f"{temp}°C",
                "humidity": f"{humidity}%",
                "condition": response["weather"][0]["description"],
                "farming_advice": analysis,
                "timestamp": datetime.now()
            }
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
