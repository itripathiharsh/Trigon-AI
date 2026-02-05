import os
import requests
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from dotenv import load_dotenv

load_dotenv()

class MediaTool:
    def __init__(self):
        # TMDB Setup
        self.tmdb_key = os.getenv("TMDB_API_KEY")
        self.tmdb_base_url = "https://api.themoviedb.org/3"

        # Spotify Setup
        sp_id = os.getenv("SPOTIPY_CLIENT_ID")
        sp_secret = os.getenv("SPOTIPY_CLIENT_SECRET")
        if sp_id and sp_secret:
            auth_manager = SpotifyClientCredentials(client_id=sp_id, client_secret=sp_secret)
            self.sp = spotipy.Spotify(auth_manager=auth_manager)
        else:
            self.sp = None

    def search_movies(self, movie_name: str):
        """Fetches movie details and cast from TMDB."""
        if not self.tmdb_key:
            return {"error": "TMDB API Key missing."}
        
        try:
            # 1. Search for the movie ID
            search_url = f"{self.tmdb_base_url}/search/movie"
            params = {"api_key": self.tmdb_key, "query": movie_name}
            res = requests.get(search_url, params=params).json()

            if not res.get("results"):
                return {"error": f"No movie found for '{movie_name}'"}
            
            movie = res["results"][0]
            movie_id = movie["id"]

            # 2. Get Credits (Cast)
            credits_url = f"{self.tmdb_base_url}/movie/{movie_id}/credits"
            credits_res = requests.get(credits_url, params={"api_key": self.tmdb_key}).json()
            cast = [member["name"] for member in credits_res.get("cast", [])[:5]]

            return {
                "title": movie["original_title"],
                "release_date": movie.get("release_date"),
                "rating": movie.get("vote_average"),
                "overview": movie.get("overview"),
                "top_cast": cast
            }
        except Exception as e:
            return {"error": str(e)}

    def search_music(self, query: str):
        """Fetches trending songs or artist details from Spotify."""
        if not self.sp:
            return {"error": "Spotify credentials missing."}
        
        try:
            # Search for tracks
            results = self.sp.search(q=query, limit=3, type='track')
            tracks = []
            for item in results['tracks']['items']:
                tracks.append({
                    "name": item['name'],
                    "artist": item['artists'][0]['name'],
                    "album": item['album']['name'],
                    "link": item['external_urls']['spotify']
                })
            return {"results": tracks}
        except Exception as e:
            return {"error": str(e)}