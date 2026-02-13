import tkinter as tk
import customtkinter as ctk
import threading

from modules.voice_engine import listen_for_command, start_wake_listener
from modules.command_handler import process_command
from modules.tts_engine import speak


# -------------------------------
# OUTPUT HANDLER (UI + SPEECH)
# -------------------------------

def log_output(text, lang="en"):
    output_area.insert(tk.END, text + "\n")
    output_area.see(tk.END)
    speak(text, lang=lang)


# -------------------------------
# VOICE COMMAND FLOW
# -------------------------------

def voice_command():
    command = listen_for_command(log_output)
    if command:
        process_command(command, log_output)


def start_voice_thread():
    threading.Thread(target=voice_command, daemon=True).start()


# -------------------------------
# TEXT COMMAND FLOW
# -------------------------------

def run_text_command():
    text = text_entry.get()

    if text.strip():
        log_output("You: " + text)
        threading.Thread(
            target=process_command,
            args=(text, log_output),
            daemon=True
        ).start()

    text_entry.delete(0, tk.END)


# -------------------------------
# ENTER KEY SUPPORT
# -------------------------------

def on_enter(event):
    run_text_command()


# -------------------------------
# GUI SETUP
# -------------------------------

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

app = ctk.CTk()
app.title("🧠 Jarvis Desktop AI")
app.geometry("1000x700")
app.state("zoomed")


avatar_img = ctk.CTkImage(light_image=None,
                          dark_image=ctk.Image.open("Jarvis/assets/images/jarvis.png"),
                          size=(120,120))

avatar_label = ctk.CTkLabel(app, image=avatar_img, text="")
avatar_label.pack(pady=5)

# TITLE
title = ctk.CTkLabel(
    app,
    text="🧠 Jarvis AI Assistant",
    font=ctk.CTkFont(size=26, weight="bold")
)
title.pack(pady=20)


# OUTPUT AREA
output_area = ctk.CTkTextbox(
    app,
    height=500,
    font=("Segoe UI", 14),
    wrap="word"
)
output_area.pack(padx=20, pady=10, fill="both", expand=True)


# INPUT FRAME
input_frame = ctk.CTkFrame(app, corner_radius=20)
input_frame.pack(pady=15, padx=20, fill="x", side="bottom")


# TEXT ENTRY
text_entry = ctk.CTkEntry(
    input_frame,
    height=45,
    font=("Segoe UI", 13),
    placeholder_text="Message Jarvis..."
)
text_entry.pack(side="left", fill="x", expand=True, padx=(10, 5), pady=10)
text_entry.bind("<Return>", on_enter)


# VOICE BUTTON
voice_button = ctk.CTkButton(
    input_frame,
    text="🎤",
    width=45,
    height=45,
    fg_color="#00c67c",
    text_color="white",
    font=ctk.CTkFont(size=16, weight="bold"),
    corner_radius=12,
    command=start_voice_thread
)
voice_button.pack(side="left", padx=5, pady=10)


# SEND BUTTON
text_button = ctk.CTkButton(
    input_frame,
    text="➤",
    width=45,
    height=45,
    fg_color="#0a84ff",
    text_color="white",
    font=ctk.CTkFont(size=16, weight="bold"),
    corner_radius=12,
    command=run_text_command
)
text_button.pack(side="left", padx=(5, 10), pady=10)


# START APP
log_output("Jarvis initialized. Ready to assist.")
start_wake_listener(process_command, log_output)

app.mainloop()
