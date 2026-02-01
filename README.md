# 🤖 JARVIC – Modular AI Voice Assistant

**JARVIC** is a futuristic, modular AI assistant inspired by **sci-fi HUD systems**.  
It supports **voice and text interaction**, uses a **plugin-based skill architecture**, and is powered by the **Groq API** for fast, high-quality natural language understanding.

Designed for **experimentation, extensibility, and learning**, JARVIC allows developers to add new capabilities **without touching the core engine**.

---

## ✨ Features

### 🖥️ Futuristic HUD Interface
- Sci-Fi inspired **PyQt6 GUI**
- Real-time visual feedback
- Interactive controls for **pause / resume**
- Clean, minimal AI-style design

### 🎙️ Dual Interaction Modes
- **Voice Mode**  
  Hands-free interaction using SpeechRecognition + Text-to-Speech
- **Text Mode**  
  Command-line interaction for debugging or silent environments

### 🧩 Modular Skill System
Plugin-style architecture where **each capability lives in its own skill module**.

Available skills include:
- 🌦️ Weather Information
- 🖥️ System Operations
- 📂 File & Text Operations
- 🌐 Web Operations
- 🧠 Memory (extensible)
- ➕ Easily add more skills

### 🧠 Intelligent Command Handling
- Wake-word detection: **“Jarvis”**
- Supports direct commands like:
  - `Open`
  - `Search`
  - `Create`
  - `Send`
  - `Exit`

---

## 🧪 Tech Stack

| Component | Technology |
|---------|-----------|
| Language | Python 3 |
| GUI | PyQt6 |
| LLM Engine | Groq API |
| Voice Input | SpeechRecognition |
| Voice Output | pyttsx3 |
| Audio | PyAudio |
| Environment | Python Virtual Environment |

---

## 📦 Installation

### 1️⃣ Clone the Repository
```bash
git clone https://github.com/way2nfea/jarvis-ai-assistant.git
cd jarvis-ai-assistant
```

2️⃣ Create & Activate Virtual Environment
```Windows
python -m venv venv
venv\Scripts\activate
```
