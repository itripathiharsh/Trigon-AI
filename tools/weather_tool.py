import requests

class WeatherTool:
    def __init__(self):
        self.geo_base = "https://geocoding-api.open-meteo.com/v1/search"
        self.weather_base = "https://api.open-meteo.com/v1/forecast"
        self.headers = {"User-Agent": "AIOpsAssistant/1.0"}

    def get_current_weather(self, city: str):
        """
        Converts city name to coordinates and fetches real-time weather.
        """
        try:
            # 1. Geocoding (City -> Lat/Long)
            geo_params = {"name": city, "count": 1, "format": "json"}
            geo_res = requests.get(self.geo_base, params=geo_params, headers=self.headers, timeout=10)
            geo_data = geo_res.json()
            
            if "results" not in geo_data or not geo_data["results"]:
                return {"error": f"Could not find coordinates for {city}"}
            
            loc = geo_data["results"][0]
            
            # 2. Weather Fetch
            w_params = {
                "latitude": loc["latitude"],
                "longitude": loc["longitude"],
                "current_weather": True
            }
            w_res = requests.get(self.weather_base, params=w_params, headers=self.headers, timeout=10)
            w_data = w_res.json()
            
            current = w_data.get("current_weather", {})
            return {
                "location": loc.get("name"),
                "country": loc.get("country"),
                "temperature": f"{current.get('temperature')}°C",
                "windspeed": f"{current.get('windspeed')} km/h",
                "condition_code": current.get("weathercode") # Can be mapped to icons later
            }
        except Exception as e:
            return {"error": f"Weather fetch failed: {str(e)}"}