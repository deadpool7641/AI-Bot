import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# -----------------------------------
# API CONFIG
# -----------------------------------

GROQ_API_KEY = os.getenv("GROQ_API_KEY")
NEWS_API_KEY = os.getenv("NEWS_API_KEY")
REPLICATE_API_TOKEN = os.getenv("REPLICATE_API_TOKEN")


# -----------------------------------
# ASSISTANT SETTINGS
# -----------------------------------

ASSISTANT_NAME = "Jarvis"
DEFAULT_LANGUAGE = "en"
URDU_LANGUAGE_CODE = "ur"


# -----------------------------------
# VOICE SETTINGS
# -----------------------------------

VOICE_RATE = 160
VOICE_GENDER = "male"   # male / female
ENABLE_VOICE_OUTPUT = True


# -----------------------------------
# UI SETTINGS
# -----------------------------------

THEME_MODE = "dark"     # dark / light
COLOR_THEME = "blue"
WINDOW_TITLE = "🧠 Jarvis Desktop AI"
WINDOW_SIZE = "1000x700"


# -----------------------------------
# MEMORY SETTINGS
# -----------------------------------

MEMORY_FILE_PATH = "Jarvis/data/memory.json"
ENABLE_MEMORY = True


# -----------------------------------
# SYSTEM AUTOMATION
# -----------------------------------

ENABLE_SYSTEM_COMMANDS = True
ENABLE_WEB_COMMANDS = True
ENABLE_NEWS = True
ENABLE_IMAGE_GEN = True


# -----------------------------------
# AI SETTINGS
# -----------------------------------

LLM_MODEL = "llama-3.3-70b-versatile"
LLM_TEMPERATURE = 0.7
MAX_RESPONSE_TOKENS = 800
