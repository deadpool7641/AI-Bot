# 🧠 Jarvis AI Voice & Text Assistant

Jarvis is a powerful desktop AI assistant built with Python that supports:
- Voice commands
- Text conversation
- AI responses (Groq)
- Image generation
- News updates
- Music playback
- Multi-language speech
- Cyberpunk UI

---

## ✨ Features

🎤 Voice Recognition  
⌨️ Text Conversation  
🧠 AI Chat (Groq LLM)  
🌍 Multi-language support  
🗞️ News fetching  
🎶 Music playback  
🖼️ AI Image generation  
🖥️ Cyberpunk UI interface  
🔊 Natural Jarvis voice (Edge TTS)

---

## 🚀 Installation

### 1) Clone project


git clone <your-repo-url>
cd Jarvis


### 2) Create virtual environment


python -m venv jarvis_env
jarvis_env\Scripts\activate


### 3) Install dependencies


pip install -r requirements.txt


### 4) Add API keys

Create a `.env` file:


NEWS_API_KEY=your_news_api
REPLICATE_API_TOKEN=your_replicate_token
GROQ_API_KEY=your_groq_key


### 5) Run Jarvis


python main.py


---

## 🧠 Commands Jarvis understands

### Web
- open youtube
- open instagram
- open gmail
- open linkedin

### AI
- what is AI
- explain python
- help me write code

### Media
- play <song>

### News
- news

### Image
- generate image of <prompt>

---

## 🗂️ Project Structure


Jarvis/
│
├── main.py
├── requirements.txt
├── README.md
├── .env
│
├── modules/
│ ├── command_handler.py
│ ├── web_actions.py
│ ├── system_actions.py
│ ├── memory.py
│ ├── translator.py
│ ├── news.py
│ ├── image_generator.py
│
├── ui/
│ ├── app.py
│ ├── components.py
│
├── data/
│ ├── memory.json
│
├── assets/
│ ├── sounds/
│ ├── images/


---

## 🛠️ Troubleshooting

### PyAudio install error


pip install pipwin
pipwin install pyaudio


### Pygame install error


pip install pygame --pre


### Mic not detected

Check Windows microphone permissions.

---

## 🧬 Future Roadmap

- Wake word detection ("Hey Jarvis")
- WhatsApp automation
- Email automation
- Smart memory learning
- Avatar hologram UI
- Offline LLM

---

## 📜 License

MIT License

---

## 🤝 Contributing

Pull requests welcome.

---

## 💡 Author

Built as an advanced AI desktop assistant using:
- Python
- Groq LLM
- Replicate
- Edge TTS
- CustomTkinter
✅ After creating these two files

Run:

pip install -r requirements.txt
python main.py