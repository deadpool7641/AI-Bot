import json
import os
from datetime import datetime

MEMORY_FILE = "Jarvis/data/memory.json"

def load_memory():
    if not os.path.exists(MEMORY_FILE):
        return {}

    with open(MEMORY_FILE, "r") as f:
        return json.load(f)


def save_memory(data):
    with open(MEMORY_FILE, "w") as f:
        json.dump(data, f, indent=4)


def remember(key, value):
    memory = load_memory()
    memory[key] = value
    memory["last_updated"] = str(datetime.now())
    save_memory(memory)


def recall(key):
    memory = load_memory()
    return memory.get(key)


def learn_habit(command):
    memory = load_memory()
    habits = memory.get("habits", {})
    habits[command] = habits.get(command, 0) + 1
    memory["habits"] = habits
    save_memory(memory)