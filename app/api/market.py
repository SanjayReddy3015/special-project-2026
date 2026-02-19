
from fastapi import APIRouter
import requests
import os

router = APIRouter()

# Data.gov.in API for Agmarknet
AGMARKNET_API_KEY = os.getenv("AGMARKNET_API_KEY", "your_api_key_here")

@router.get("/prices/{state}/{commodity}")
async def get_mandi_prices(state: str, commodity: str):
    # This is a sample URL for the Govt of India Data Portal
    url = f"https://api.data.gov.in/resource/9ef842fd-551f-497c-8069-14353d9e86c0?api-key={AGMARKNET_API_KEY}&format=json&filters[state]={state}&filters[commodity]={commodity}"
    
    try:
        res = requests.get(url).json()
        records = res.get("records", [])
        
        if not records:
            return {"success": False, "message": "No data available for this selection."}

        # Real-time Analysis: Calculate Average Price & Identify Best Market
        prices = [int(r['modal_price']) for r in records]
        avg_price = sum(prices) / len(prices)
        
        # Find the market with the highest price for the farmer
        best_market = max(records, key=lambda x: int(x['modal_price']))

        return {
            "success": True,
            "commodity": commodity,
            "analysis": {
                "average_price": round(avg_price, 2),
                "highest_price": best_market['modal_price'],
                "best_market_location": f"{best_market['market']}, {best_market['district']}",
                "price_unit": "INR/Quintal"
            },
            "raw_data": records[:5] # Send top 5 recent records
        }
    except Exception as e:
        return {"success": False, "error": "Unable to fetch market data."}
