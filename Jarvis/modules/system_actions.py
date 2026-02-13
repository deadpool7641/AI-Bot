import os
import platform
import subprocess
import webbrowser
from shutil import which

OS_NAME = platform.system().lower()


# -----------------------------------
# SOCIAL MEDIA + WEB APPS
# -----------------------------------

WEB_APPS = {
    "facebook": "https://facebook.com",
    "instagram": "https://instagram.com",
    "whatsapp": "https://web.whatsapp.com",
    "telegram": "https://web.telegram.org",
    "twitter": "https://twitter.com",
    "x": "https://twitter.com",
    "linkedin": "https://linkedin.com",
    "gmail": "https://mail.google.com",
    "youtube": "https://youtube.com",
    "reddit": "https://reddit.com",
    "chatgpt": "https://chat.openai.com"
}


# -----------------------------------
# SAFE COMMAND EXECUTOR
# -----------------------------------

def run_command(command):
    try:
        subprocess.Popen(command, shell=True)
        return True
    except Exception:
        return False


# -----------------------------------
# OPEN APPLICATIONS (ROBUST)
# -----------------------------------

def open_app(app_name):
    app_name = app_name.lower()

    # 1️⃣ Always allow browser fallback first
    if app_name in WEB_APPS:
        webbrowser.open(WEB_APPS[app_name])
        return f"Opening {app_name}"

    try:

        # WINDOWS
        if OS_NAME == "windows":
            apps = {
                "chrome": "start chrome",
                "vscode": "code",
                "notepad": "notepad",
                "calculator": "calc",
                "explorer": "explorer",
                "cmd": "start cmd"
            }

            if app_name in apps:
                run_command(apps[app_name])
                return f"Opening {app_name}"

        # MAC
        elif OS_NAME == "darwin":
            apps = {
                "chrome": "open -a 'Google Chrome'",
                "vscode": "open -a 'Visual Studio Code'",
                "finder": "open ."
            }

            if app_name in apps:
                run_command(apps[app_name])
                return f"Opening {app_name}"

        # LINUX
        elif OS_NAME == "linux":
            apps = {
                "chrome": "google-chrome",
                "vscode": "code",
                "files": "xdg-open ."
            }

            if app_name in apps and which(apps[app_name]):
                subprocess.Popen([apps[app_name]])
                return f"Opening {app_name}"

        # 2️⃣ fallback to search open in browser
        webbrowser.open(f"https://www.google.com/search?q={app_name}")
        return f"Searching for {app_name}"

    except Exception as e:
        return f"Error opening app: {e}"


# -----------------------------------
# CREATE FILE
# -----------------------------------

def create_file(filename):
    try:
        with open(filename, "w") as f:
            f.write("")
        return f"{filename} created successfully."
    except Exception as e:
        return f"File creation error: {e}"


# -----------------------------------
# OPEN FOLDER
# -----------------------------------

def open_folder(path):
    try:
        if OS_NAME == "windows":
            os.startfile(path)

        elif OS_NAME == "darwin":
            subprocess.Popen(["open", path])

        elif OS_NAME == "linux":
            subprocess.Popen(["xdg-open", path])

        return f"Opening folder: {path}"

    except Exception as e:
        return f"Folder open error: {e}"


# -----------------------------------
# SYSTEM CONTROL
# -----------------------------------

def shutdown_pc():
    try:
        if OS_NAME == "windows":
            os.system("shutdown /s /t 5")

        elif OS_NAME == "darwin":
            os.system("shutdown -h now")

        elif OS_NAME == "linux":
            os.system("shutdown now")

        return "Shutting down system..."
    except Exception as e:
        return f"Shutdown error: {e}"


def restart_pc():
    try:
        if OS_NAME == "windows":
            os.system("shutdown /r /t 5")

        elif OS_NAME == "darwin":
            os.system("shutdown -r now")

        elif OS_NAME == "linux":
            os.system("reboot")

        return "Restarting system..."
    except Exception as e:
        return f"Restart error: {e}"