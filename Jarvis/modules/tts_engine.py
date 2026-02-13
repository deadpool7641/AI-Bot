import pyttsx3
from gtts import gTTS
import pygame
import uuid
import os
from threading import Lock

engine = pyttsx3.init()
speak_lock = Lock()


def speak(text, lang="en"):
    with speak_lock:
        try:
            if lang == "ur":
                filename = f"output_{uuid.uuid4()}.mp3"
                tts = gTTS(text=text, lang="ur")
                tts.save(filename)

                pygame.mixer.init()
                pygame.mixer.music.load(filename)
                pygame.mixer.music.play()

                while pygame.mixer.music.get_busy():
                    pygame.time.Clock().tick(10)

                pygame.mixer.quit()
                os.remove(filename)

            else:
                engine = pyttsx3.init()
                voices = engine.getProperty("voices")
                for voice in voices:
                    if "male" in voice.name.lower():
                        engine.setProperty("voice", voice.id)
                        break
                engine.setProperty("rate", 160)
                engine.say(text)
                engine.runAndWait()

        except Exception as e:
            print("TTS error:", e)
