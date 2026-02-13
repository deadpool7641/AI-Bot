import webbrowser
import musicLibrary

from Jarvis.config import (
    ENABLE_MEMORY,
    ENABLE_NEWS,
    ENABLE_IMAGE_GEN,
    ENABLE_SYSTEM_COMMANDS,
    ENABLE_WEB_COMMANDS,
    ASSISTANT_NAME
)

from modules.news import get_news
from modules.image_generator import generate_image
from modules.system_actions import open_app, shutdown_pc
from modules.web_actions import ask_groq, open_website, search_google, add_history
from modules.translator import detect_language, translate_to
from modules.memory import remember, recall


# -----------------------------------
# MAIN COMMAND ROUTER
# -----------------------------------

def process_command(command, log_output):
    print("NEW COMMAND HANDLER ACTIVE")

    c = command.lower()
    user_lang = detect_language(command)

    def execute(result):
        log_output(result)
        add_history("user", command)
        add_history("assistant", str(result))

    try:

        # ---------------- MEMORY ----------------
        if ENABLE_MEMORY:
            if "my name is" in c:
                name = command.split("is")[-1].strip()
                remember("username", name)
                log_output(f"I will remember that, {name}")
                return

            elif "what is my name" in c:
                name = recall("username")
                log_output(
                    f"Your name is {name}" if name else "I don't know your name yet."
                )
                return


        # ---------------- SMART WEB OPEN (PRIMARY) ----------------
        # Any "open <site>" or social keyword goes here FIRST

        if "open" in c:

            if "youtube" in c:
                execute(open_website("youtube.com"))
                return

            if "instagram" in c:
                execute(open_website("instagram.com"))
                return

            if "facebook" in c:
                execute(open_website("facebook.com"))
                return

            if "whatsapp" in c:
                execute(open_website("web.whatsapp.com"))
                return

            if "telegram" in c:
                execute(open_website("web.telegram.org"))
                return

            if "gmail" in c:
                execute(open_website("mail.google.com"))
                return

            if "linkedin" in c:
                execute(open_website("linkedin.com"))
                return

            if "reddit" in c:
                execute(open_website("reddit.com"))
                return

            if "twitter" in c or "x" in c:
                execute(open_website("twitter.com"))
                return

            # generic open website
            site = c.replace("open", "").strip()
            execute(open_website(site))
            return


        # ---------------- GOOGLE SEARCH ----------------
        if c.startswith("search"):
            query = c.replace("search", "").strip()
            execute(search_google(query))
            return


        # ---------------- NEWS ----------------
        if ENABLE_NEWS and "news" in c:
            log_output("Fetching news...")
            add_history("user", command)
            news_summary = "Here are the latest news headlines:\n"
            for article in get_news():
                log_output(article)
                news_summary += f"- {article}\n"
            add_history("assistant", news_summary)
            return


        # ---------------- IMAGE ----------------
        if ENABLE_IMAGE_GEN and ("generate image" in c or "draw" in c):
            prompt = c.replace("generate image of", "").replace("draw", "").strip()
            log_output("Generating image...")
            url = generate_image(prompt)
            log_output(url)
            add_history("user", command)
            add_history("assistant", f"Generated image: {url}")
            return


        # ---------------- MUSIC ----------------
        if c.startswith("play"):
            song = c.split("play")[-1].strip()
            if song in musicLibrary.music:
                webbrowser.open(musicLibrary.music[song])
                log_output(f"Playing {song}")
                add_history("user", command)
                add_history("assistant", f"Playing {song}")
            else:
                log_output("Song not found.")
                add_history("user", command)
                add_history("assistant", "Song not found.")
            return


        # ---------------- SYSTEM ----------------
        if ENABLE_SYSTEM_COMMANDS:
            if "shutdown" in c:
                execute(shutdown_pc())
                return


        # ---------------- AI FALLBACK ----------------
        log_output("Thinking...")
        response = ask_groq(command)

        if user_lang == "ur":
            response = translate_to(response, "ur")
            log_output(response, lang="ur")
        else:
            log_output(response)

    except Exception as e:
        log_output(f"{ASSISTANT_NAME} error: {e}")