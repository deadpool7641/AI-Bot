import requests
import os
import webbrowser
import time
from dotenv import load_dotenv

load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY")
GROQ_URL = "https://api.groq.com/openai/v1/chat/completions"


conversation_history = [
    {"role": "system", "content": "You are Jarvis, an intelligent desktop AI assistant. You are witty, sarcastic, and helpful."}
]

def add_history(role, content):
    conversation_history.append({"role": role, "content": content})

# -----------------------------------
# GROQ AI RESPONSE
# -----------------------------------

def ask_groq(prompt):
    if not GROQ_API_KEY:
        return "Groq API key missing in .env file."

    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json"
    }

    add_history("user", prompt)

    data = {
        "model": "llama-3.3-70b-versatile",
        "messages": conversation_history,
        "temperature": 0.7,
        "max_tokens": 800
    }

    for attempt in range(3):
        try:
            response = requests.post(GROQ_URL, headers=headers, json=data, timeout=25)

            if response.status_code == 200:
                content = response.json()["choices"][0]["message"]["content"]
                add_history("assistant", content)
                return content

            elif response.status_code == 401:
                return "Invalid Groq API key."

            elif response.status_code == 429:
                time.sleep(2)
                continue

            else:
                return f"Groq API error: {response.status_code}"

        except requests.exceptions.Timeout:
            if attempt == 2:
                return "Groq request timed out."

        except requests.exceptions.ConnectionError:
            return "Network error while contacting Groq."

        except Exception as e:
            return f"Groq error: {str(e)}"

    return "Groq service unavailable."


# -----------------------------------
# OPEN WEBSITE
# -----------------------------------

def open_website(site):
    """
    Opens any website intelligently.
    Accepts:
    - instagram
    - instagram.com
    - https://instagram.com
    """

    try:
        site = site.strip().lower()

        # Add https if missing
        if not site.startswith("http"):
            if "." not in site:
                site = site + ".com"
            site = "https://" + site

        webbrowser.open(site)
        return f"Opening {site}"

    except Exception as e:
        return f"Failed to open website: {e}"


# -----------------------------------
# GOOGLE SEARCH
# -----------------------------------

def search_google(query):
    try:
        url = f"https://www.google.com/search?q={query}"
        webbrowser.open(url)
        return f"Searching Google for {query}"
    except Exception as e:
        return f"Search error: {e}"


# -----------------------------------
# SMART WEB ROUTER
# -----------------------------------

SOCIAL_SITES = {
    "youtube": "youtube.com",
    "instagram": "instagram.com",
    "facebook": "facebook.com",
    "whatsapp": "web.whatsapp.com",
    "telegram": "web.telegram.org",
    "gmail": "mail.google.com",
    "linkedin": "linkedin.com",
    "reddit": "reddit.com",
    "twitter": "twitter.com",
    "x": "twitter.com",
    "chatgpt": "chat.openai.com"
}


def handle_web_command(command):
    """
    Detects and opens websites from natural language
    """

    c = command.lower()

    # Open known social/websites
    for key in SOCIAL_SITES:
        if key in c:
            return open_website(SOCIAL_SITES[key])

    # "open github"
    if c.startswith("open "):
        site = c.replace("open ", "").strip()
        return open_website(site)

    # "search python decorators"
    if c.startswith("search "):
        query = c.replace("search ", "").strip()
        return search_google(query)

    return None


# -----------------------------------
# INTERNET CHECK
# -----------------------------------

def check_internet():
    try:
        requests.get("https://google.com", timeout=5)
        return True
    except:
        return False