import requests
import os
from dotenv import load_dotenv

load_dotenv()
NEWS_API_KEY = os.getenv("NEWS_API_KEY")


def get_news():
    if not NEWS_API_KEY:
        return ["News API key missing."]

    try:
        url = f"https://newsapi.org/v2/top-headlines?country=us&apiKey={NEWS_API_KEY}"
        response = requests.get(url, timeout=10)

        if response.status_code == 200:
            articles = response.json().get("articles", [])
            return [a["title"] for a in articles[:5]]

        return ["Failed to fetch news."]
    except Exception as e:
        return [f"News error: {e}"]
