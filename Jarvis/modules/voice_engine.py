import speech_recognition as sr
import threading

WAKE_WORD = "hey jarvis"
LISTENING = False


def detect_wake_word(log_output=None):
    recognizer = sr.Recognizer()

    with sr.Microphone() as source:
        recognizer.adjust_for_ambient_noise(source, duration=1)

        while True:
            try:
                recognizer.energy_threshold = 300
                recognizer.dynamic_energy_threshold = True
                audio = recognizer.listen(source, timeout=15, phrase_time_limit=10)
                text = recognizer.recognize_google(audio).lower()

                if WAKE_WORD in text:
                    if log_output:
                        log_output("Wake word detected.")
                    return True

            except:
                continue


def listen_for_command(log_output=None):
    recognizer = sr.Recognizer()

    with sr.Microphone() as source:
        if log_output:
            log_output("Listening for command...")

        recognizer.adjust_for_ambient_noise(source, duration=1)

        try:
            audio = recognizer.listen(source, timeout=6, phrase_time_limit=8)
            command = recognizer.recognize_google(audio)

            if log_output:
                log_output("You: " + command)

            return command

        except:
            if log_output:
                log_output("Couldn't understand command.")
            return None


def start_wake_listener(process_command, log_output):
    def wake_loop():
        while True:
            detected = detect_wake_word(log_output)
            if detected:
                command = listen_for_command(log_output)
                if command:
                    process_command(command, log_output)

    thread = threading.Thread(target=wake_loop, daemon=True)
    thread.start()
