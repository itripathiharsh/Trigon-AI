import os
import requests
from dotenv import load_dotenv

load_dotenv()

class NewsTool:
    def __init__(self):
        # Using the key name we confirmed in your .env
        self.api_key = os.getenv("NEWS_API_KEY")

    def get_latest_news(self, query=None):
        """
        Fetches latest headlines or searches for a specific topic.
        """
        if not self.api_key:
            return {"error": "NEWS_API_KEY not found in environment."}

        # Select endpoint based on whether there is a search query
        url = "https://api.currentsapi.services/v1/search" if query else "https://api.currentsapi.services/v1/latest-news"
        
        # REQUIRED: Authorization must be in the header
        headers = {"Authorization": self.api_key}
        params = {"language": "en"}
        if query:
            params["keywords"] = query

        try:
            response = requests.get(url, headers=headers, params=params, timeout=10)
            if response.status_code != 200:
                return {"error": f"News API returned status {response.status_code}"}
            
            data = response.json()
            news_items = data.get("news", [])
            
            # Return top 5 results to keep the LLM context clean
            formatted_news = []
            for item in news_items[:5]:
                formatted_news.append({
                    "title": item.get("title"),
                    "author": item.get("author"),
                    "description": item.get("description"),
                    "url": item.get("url")
                })
            return formatted_news
            
        except Exception as e:
            return {"error": f"News retrieval failed: {str(e)}"}