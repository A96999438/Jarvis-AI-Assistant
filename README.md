# 🤖 Jarvis - AI Voice Assistant

Jarvis is an **AI-powered Voice Assistant** built using **Python**, **Google Gemini AI**, **Natural Language Processing (NLP)**, **Speech Recognition**, and **Voice Synthesis**. It automates daily tasks, answers user queries using Generative AI, performs voice-controlled operations, and can be extended for **IoT device control** and **smart automation**.

The project includes **two executable versions** of Jarvis:
- **jarvis.py** – Full-featured AI assistant with task automation.
- **code01.py** – Lightweight version with continuous voice recognition and Gemini integration.

You can run **either file** based on your requirements.

---

# 🚀 Features

- 🎤 Voice Command Recognition
- 🤖 Google Gemini AI Integration
- 🗣️ Text-to-Speech Responses
- 🧠 Natural Language Processing (NLP)
- 🌦️ Weather Information
- ⏰ Time Queries
- 📺 Open YouTube & Google
- ▶️ Play YouTube Videos
- 💬 Send WhatsApp Messages
- 📧 Send Emails
- ⏰ Alarm Management
- 📚 Wikipedia Search
- 😂 Tell Jokes
- 🧠 Conversation Memory
- 🔊 Hotword Activation ("Hey Jarvis")
- 🏠 Extendable for IoT & Home Automation

---

# 🛠️ Technologies Used

- Python 3.x
- Google Gemini AI API
- SpeechRecognition
- pyttsx3
- Vosk Offline Speech Model
- Requests
- PyWhatKit
- Wikipedia
- SMTP (Email)
- Natural Language Processing (NLP)

---

# 📁 Project Structure

```
Jarvis/
│
├── model/                  # Vosk Offline Speech Recognition Model
│
├── jarvis.py               # Full AI Assistant
├── code01.py               # Lightweight AI Assistant
│
├── requirements.txt        # Python Dependencies (Optional)
├── README.md
└── .gitignore
```

---

# ⚙️ Installation

## Clone the Repository

```bash
git clone https://github.com/A96999438/Jarvis.git

cd Jarvis
```

---

## Install Dependencies

```bash
pip install -r requirements.txt
```

If you don't have a `requirements.txt`, install the required packages manually:

```bash
pip install google-generativeai
pip install SpeechRecognition
pip install pyttsx3
pip install requests
pip install pywhatkit
pip install wikipedia
pip install pyaudio
pip install vosk
```

---

## Configure API Keys

Create a `.env` file or directly replace the placeholders inside the Python files.

```
GEMINI_API_KEY=YOUR_GEMINI_API_KEY

WEATHER_API_KEY=YOUR_WEATHER_API_KEY
```

---

# ▶️ Run the Project

Run **either** of the following files:

### Full AI Assistant

```bash
python jarvis.py
```

### Lightweight AI Assistant

```bash
python code01.py
```

---

# 🧠 How It Works

1. Starts the voice assistant.
2. Listens for user voice commands.
3. Converts speech into text.
4. Processes the command using NLP.
5. If required, sends the query to Google Gemini AI.
6. Performs the requested task.
7. Converts the response back into speech.

---

# 📌 Example Commands

- "Hey Jarvis"
- "What is Artificial Intelligence?"
- "What's the weather in Mumbai?"
- "Open Google"
- "Open YouTube"
- "Play Believer on YouTube"
- "Tell me a joke"
- "Search Wikipedia for Machine Learning"
- "What time is it?"

---

# 📈 Future Enhancements

- Smart Home / IoT Device Control
- Calendar & Schedule Management
- Face Recognition Login
- Offline AI Mode
- Multi-language Support
- Desktop GUI
- Home Automation Dashboard
- Reminder & Notes Management
- Voice Authentication

---

# 👨‍💻 Developer

**Aman Aslam Patel**

Artificial Intelligence & Data Science Student

🔗 GitHub  
https://github.com/A96999438

🔗 LinkedIn  
https://www.linkedin.com/in/a-92-p/

---

# ⭐ Support

If you like this project, don't forget to ⭐ **Star** the repository.

Contributions, suggestions, and feedback are always welcome.