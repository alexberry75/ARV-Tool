# main.py
from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
import os
import requests

app = FastAPI()

# CORS so GPT can call it
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

ZILLOW_API_KEY = os.getenv("ZILLOW_API_KEY")

@app.get("/get_arv_estimate")
def get_arv_estimate(address: str = Query(...), budget: float = Query(...)):
    if not ZILLOW_API_KEY:
        return {"error": "Missing Zillow API key."}

    # Example simulated response — replace with your actual Zillow API logic
    comps = [
        {"address": "456 Oak St", "price": 640000, "sqft": 2050},
        {"address": "789 Pine St", "price": 665000, "sqft": 2150},
        {"address": "234 Elm St", "price": 670000, "sqft": 2080},
    ]

    avg_price_per_sqft = sum(c["price"] / c["sqft"] for c in comps) / len(comps)
    estimated_sqft = 2100  # Simulated — replace with Zillow property info
    arv = avg_price_per_sqft * estimated_sqft

    return {
        "arv": round(arv, 2),
        "price_per_sqft": round(avg_price_per_sqft, 2),
        "estimated_sqft": estimated_sqft,
        "comps_used": comps
    }
