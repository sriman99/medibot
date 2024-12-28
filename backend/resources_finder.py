import requests
import os

google_maps_api_key = os.getenv("GEMINI_API_KEY")

def find_health_resources(location):
    url = f"https://maps.googleapis.com/maps/api/place/nearbysearch/json"
    params = {
        "location": location,  # Example: "37.7749,-122.4194"
        "radius": 5000,  # 5 km radius
        "type": "pharmacy|hospital|clinic",
        "key": google_maps_api_key
    }

    response = requests.get(url, params=params)
    if response.status_code == 200:
        places = response.json().get("results", [])
        return [{"name": place["name"], "address": place["vicinity"]} for place in places]
    return {"error": "Failed to fetch resources"}
