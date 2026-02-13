import tkinter as tk
from tkinter import messagebox, scrolledtext
import webbrowser
import pyttsx3
import replicate.client
import requests
import replicate
import speech_recognition as sr
import threading
import musicLibrary

from langdetect import detect
from gtts import gTTS
import pygame
import os
import asyncio
import edge_tts
import uuid
import random
import time
from deep_translator import GoogleTranslator
from threading import Lock
import customtkinter as ctk
from dotenv import load_dotenv   

# Load environment variables
load_dotenv()

# Initialize TTS
engine = pyttsx3.init()

# API Keys
newsapi = os.getenv("NEWS_API_KEY")
replicate_token = os.getenv("REPLICATE_API_TOKEN")
groq_key = os.getenv("GROQ_API_KEY")


# =========================
# LANGUAGE + TRANSLATION
# =========================

def translate_to(text, target_lang):
    try:
        return GoogleTranslator(source='auto', target=target_lang).translate(text)
    except:
        return text

def detect_language(text):
    try:
        return detect(text)
    except:
        return "en"


# =========================
# HUMAN JARVIS SPEECH ENGINE
# =========================

speak_lock = Lock()

async def get_edge_tts_audio(text, voice, filename):
    communicate = edge_tts.Communicate(text, voice)
    await communicate.save(filename)

def speak(text, lang='en'):
    with speak_lock:
        try:
            # Don't repeat user's own words
            if text.startswith("You:"):
                return

            filename = f"output_{uuid.uuid4()}.mp3"

            if lang == 'ur':
                tts = gTTS(text=text, lang='ur')
                tts.save(filename)
            else:
                # Jarvis-style British AI voice
                voice = "en-GB-RyanNeural"
                asyncio.run(get_edge_tts_audio(text.replace("Jarvis:", ""), voice, filename))

            pygame.mixer.init()
            pygame.mixer.music.load(filename)
            pygame.mixer.music.play()
            while pygame.mixer.music.get_busy():
                pygame.time.Clock().tick(10)
            pygame.mixer.quit()

            if os.path.exists(filename):
                os.remove(filename)

        except Exception as e:
            print(f"Speak error: {e}")


# =========================
# CYBER TERMINAL OUTPUT
# =========================

def typewriter_effect(text, tag):
    for char in text:
        output_area.insert(tk.END, char, tag)
        output_area.see(tk.END)
        app.update()
        time.sleep(0.008)
    output_area.insert(tk.END, "\n")

def log_output(text, lang="en"):
    tag = "info"
    if text.startswith("You:"):
        tag = "user"
    elif text.startswith("Jarvis:"):
        tag = "jarvis"
    elif "Error" in text:
        tag = "error"
    elif text == "Listening...":
        tag = "status"

    if tag == "jarvis":
        typewriter_effect(text, tag)
    else:
        output_area.insert(tk.END, text + "\n", tag)

    output_area.see(tk.END)
    speak(text, lang=lang)


# =========================
# GROQ AI
# =========================

conversation_history = [
    {"role": "system", "content": "You are J.A.R.V.I.S., Tony Stark's advanced AI assistant. You are witty, sarcastic, highly intelligent, and polite. Address the user as 'Sir'. Keep responses concise."}
]

def ask_groq(prompt):
    global conversation_history
    headers = {
        "Authorization": f"Bearer {groq_key}",
        "Content-Type": "application/json"
    }

    conversation_history.append({"role": "user", "content": prompt})

    data = {
        "model": "llama-3.3-70b-versatile",
        "messages": conversation_history
    }

    try:
        response = requests.post("https://api.groq.com/openai/v1/chat/completions", headers=headers, json=data)
        if response.status_code == 200:
            ai_response = response.json()['choices'][0]['message']['content']
            conversation_history.append({"role": "assistant", "content": ai_response})
            return ai_response
        else:
            return "Jarvis systems are not fully connected yet."
    except:
        return "Network connection issue."


# =========================
# IMAGE GENERATION
# =========================

def generate_image(prompt):
    log_output("Jarvis: Generating image...")
    try:
        client = replicate.Client(api_token=replicate_token)
        output = client.run("stability-ai/sdxl", input={"prompt": prompt})
        image_url = output[0]
        webbrowser.open(image_url)
        log_output(f"Jarvis: Image generated successfully.")
    except:
        log_output("Error generating image.")


# =========================
# COMMAND ROUTER (UNCHANGED)
# =========================

def process_command(c):
    user_lang = detect_language(c)
    if c.lower().startswith("open "):
        site = c.lower().replace("open ", "").strip()
        sites = {
            "google": "https://google.com",
            "youtube": "https://youtube.com",
            "instagram": "https://instagram.com",
            "facebook": "https://facebook.com",
            "twitter": "https://twitter.com",
            "whatsapp": "https://web.whatsapp.com",
            "linkedin": "https://linkedin.com",
            "reddit": "https://reddit.com",
            "gmail": "https://mail.google.com"
        }
        if site in sites:
            webbrowser.open(sites[site])
        else:
            webbrowser.open(f"https://{site}.com" if "." not in site else f"https://{site}")
        log_output(f"Jarvis: Opening {site}...")
        conversation_history.append({"role": "user", "content": c})
        conversation_history.append({"role": "assistant", "content": f"Opening {site}..."})

    elif "news" in c.lower():
        r = requests.get(f"https://newsapi.org/v2/top-headlines?country=us&apiKey={newsapi}")
        if r.status_code == 200:
            data = r.json()
            for article in data.get('articles', [])[:5]:
                log_output(f"Jarvis: {article['title']}")
        else:
            log_output("Failed to fetch news.")
        conversation_history.append({"role": "user", "content": c})
        conversation_history.append({"role": "assistant", "content": "Here are the latest news headlines."})

    elif c.lower().startswith("play"):
        song = c.lower().split(" ")[1]
        link = musicLibrary.music[song]
        webbrowser.open(link)
        conversation_history.append({"role": "user", "content": c})
        conversation_history.append({"role": "assistant", "content": f"Playing {song}."})

    elif "generate image" in c.lower() or "draw" in c.lower():
        prompt = c.lower().replace("generate image of", "").replace("draw", "").strip()
        generate_image(prompt)
        conversation_history.append({"role": "user", "content": c})
        conversation_history.append({"role": "assistant", "content": "Generating image."})

    else:
        response = ask_groq(c)
        if user_lang == "ur":
            response = translate_to(response, "ur")
        log_output("Jarvis: " + response)


# =========================
# VOICE
# =========================

def voice_command():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        recognizer.adjust_for_ambient_noise(source, duration=0.5)
        log_output("Listening...")
        try:
            audio = recognizer.listen(source, timeout=5, phrase_time_limit=10)
            command = recognizer.recognize_google(audio)
            log_output("You: " + command)
            process_command(command)
        except:
            log_output("Listening timed out.")


def start_voice_thread():
    threading.Thread(target=voice_command).start()


def run_text_command():
    text = text_entry.get()
    if text.strip():
        log_output("You: " + text)
        threading.Thread(target=process_command, args=(text,)).start()
    text_entry.delete(0, tk.END)


# =========================
# CYBERPUNK GUI
# =========================

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

app = ctk.CTk()
app.title("Jarvis AI")
app.geometry("1100x700")
app.state("zoomed")
app.configure(fg_color="#05070A")

main_container = ctk.CTkFrame(app, fg_color="transparent")
main_container.pack(fill="both", expand=True, padx=30, pady=30)

header_frame = ctk.CTkFrame(main_container, fg_color="transparent")
header_frame.pack(fill="x", pady=(0, 20))

title_label = ctk.CTkLabel(
    header_frame,
    text="JARVIS",
    font=ctk.CTkFont(family="Orbitron", size=42, weight="bold"),
    text_color="#00F0FF"
)
title_label.pack(side="left")

status_label = ctk.CTkLabel(
    header_frame,
    text="ONLINE",
    font=ctk.CTkFont(size=14, weight="bold"),
    text_color="#00FF9C"
)
status_label.pack(side="left", padx=12, pady=(12, 0))

# Neon animation
def animate_title():
    colors = ["#00F0FF","#00FFFF","#00BFFF"]
    title_label.configure(text_color=random.choice(colors))
    app.after(600, animate_title)
animate_title()

# Output area
output_frame = ctk.CTkFrame(main_container, fg_color="#0A0F14", corner_radius=18, border_width=1, border_color="#00F0FF")
output_frame.pack(fill="both", expand=True, pady=(0,20))

output_area = ctk.CTkTextbox(output_frame, font=("Consolas", 16), wrap="word", fg_color="transparent", text_color="#E0FFFF")
output_area.pack(fill="both", expand=True, padx=20, pady=20)

# Neon text styles
output_area._textbox.tag_config("user", foreground="#00F0FF", font=("Consolas",16,"bold"))
output_area._textbox.tag_config("jarvis", foreground="#E0FFFF")
output_area._textbox.tag_config("error", foreground="#FF1744")
output_area._textbox.tag_config("status", foreground="#00FF9C")
output_area._textbox.tag_config("info", foreground="#90A4AE")

# Input HUD
input_frame = ctk.CTkFrame(main_container, fg_color="#0A0F14", corner_radius=30, border_width=1, border_color="#00F0FF")
input_frame.pack(fill="x", ipady=5)

voice_button = ctk.CTkButton(
    input_frame,
    text="🎙",
    width=55,
    height=55,
    fg_color="transparent",
    hover_color="#002F36",
    text_color="#00F0FF",
    font=ctk.CTkFont(size=26),
    corner_radius=30,
    command=start_voice_thread
)
voice_button.pack(side="left", padx=(10,5), pady=5)

def pulse():
    voice_button.configure(font=ctk.CTkFont(size=random.choice([26,28,30])))
    app.after(900,pulse)
pulse()

text_entry = ctk.CTkEntry(input_frame, height=45, font=("Consolas", 16), placeholder_text="Speak or type...", fg_color="transparent", border_width=0, text_color="#FFFFFF")
text_entry.pack(side="left", fill="x", expand=True, padx=10, pady=10)
text_entry.bind("<Return>", lambda e: run_text_command())

text_button = ctk.CTkButton(
    input_frame,
    text="➤",
    width=45,
    height=45,
    fg_color="#00F0FF",
    hover_color="#00B8D4",
    text_color="#05070A",
    font=ctk.CTkFont(size=20, weight="bold"),
    corner_radius=22,
    command=run_text_command
)
text_button.pack(side="left", padx=(5,10), pady=10)

app.mainloop()