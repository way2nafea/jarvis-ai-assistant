🤖 JARVIC – Modular AI Voice Assistant
JARVIC is a futuristic, modular AI assistant inspired by sci-fi HUD systems.
It supports voice and text interaction, a plugin-based skill architecture, and uses the Groq API for fast, high-quality natural language understanding.
Designed for experimentation, extensibility, and learning — JARVIC allows developers to easily add new capabilities without touching the core engine.
✨ Features
🖥️ Futuristic HUD Interface
Sci-Fi inspired GUI built using PyQt6
Real-time visual feedback
Interactive controls for pause/resume and shutdown
🎙️ Dual Interaction Modes
Voice Mode
Hands-free interaction using speech recognition and text-to-speech
Text Mode
Command-line interaction for debugging or silent environments
🧩 Modular Skill System
Plugin-style architecture
Each capability lives in its own skill module
Easy to add, remove, or extend features
Available skills include:
🌦️ Weather Information
🖥️ System Operations
📧 Email Handling
🌐 Web Operations
📁 File & Text Operations
🧠 Persistent Memory
➕ More can be added easily
🗣️ Wake Word Detection
Responds to “Jarvis”
Also supports direct command phrases
🛠️ Tech Stack
Component
Technology
Language
Python 3
GUI
PyQt6
LLM Engine
Groq API
Speech Input
SpeechRecognition
Speech Output
pyttsx3
Audio
PyAudio
Environment
Python Virtual Environment
📦 Installation
1️⃣ Clone the Repository
Copy code
Bash
git clone https://github.com/your-username/Project_JARVIS.git
cd Project_JARVIS
2️⃣ Create & Activate Virtual Environment
Copy code
Bash
python3 -m venv venv
source venv/bin/activate
Windows
Copy code
Bash
venv\Scripts\activate
3️⃣ Install Dependencies
Copy code
Bash
pip install -r requirements.txt
4️⃣ Environment Configuration
This project requires API keys via environment variables.
Create a .env file:
Copy code
Bash
cp .env.template .env
Edit .env and add:
Copy code
Env
GROQ_API_KEY=your_groq_api_key_here
Optional (depending on enabled skills):
Weather API keys
Email credentials
⚠️ Do NOT commit .env to GitHub
▶️ Usage
Run Voice-Activated GUI Mode
Copy code
Bash
python main.py
Run Text-Only Mode
Copy code
Bash
python main.py --text
🎮 Controls
Voice Commands
Say “Jarvis” followed by your command
Example:
"Jarvis, what's the weather?"
GUI Controls
Click the central HUD element → Pause / Resume listening
Close the window → Gracefully shuts down JARVIC
Direct Commands
Commands like:
Open
Search
Create
Send
Exit
🗂️ Project Structure
Copy code
Text
Project_JARVIS/
│
├── main.py            # Application entry point
├── requirements.txt   # Dependencies
├── .env.template      # Environment variable template
│
├── core/              # Core engine & skill registry
│   ├── engine.py
│   ├── voice.py
│   └── memory.py
│
├── gui/               # PyQt6 HUD interface
│   └── app.py
│
├── skills/            # Modular skill plugins
│   ├── weather/
│   ├── system_ops/
│   ├── email/
│   ├── web_ops/
│   └── file_ops/
│
├── assets/             # UI assets & resources
└── venv/               # Virtual environment (ignored)
🚧 Platform Support
⚠️ Big Update
Currently, JARVIC works only on macOS.
👉 A Windows-compatible version will be released after the YouTube channel reaches 100 subscribers.
🧠 Design Philosophy
Separation of Concerns
Core logic, UI, and skills are fully decoupled
Extensibility First
New skills can be added without modifying the core
Developer Friendly
Clear structure, readable code, and easy debugging
📜 License
This project is licensed under the MIT License.
Feel free to use, modify, and distribute.
