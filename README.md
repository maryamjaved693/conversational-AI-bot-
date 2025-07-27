# 🎙️ Terminal-Based Voice Assistant (Deepgram + Groq + gTTS)

This is a Python voice assistant that lets you have a conversation through the terminal using your voice. It records your voice input, transcribes it with Deepgram’s speech-to-text API, generates an AI response using Groq's LLaMA-3 model, and converts the response back to speech using gTTS with playback through pygame.

---

## 🧠 How It Works

1. **🎤 Record**: Records 5 seconds of audio using your microphone.
2. **📝 Transcribe**: Sends the audio to Deepgram for real-time transcription.
3. **🤖 AI Response**: Sends the transcribed text to Groq's LLaMA-3 model to get a reply.
4. **🔊 Text-to-Speech**: Uses gTTS to convert the reply to audio and plays it.

---

## 🛠️ Requirements

- Python 3.10 or newer
- A working microphone
- Deepgram API Key
- Groq API Key

---

## 📦 Installation

1. **Clone this repository**
   ```bash
   git clone https://github.com/yourusername/voice-assistant-terminal.git
   cd voice-assistant-terminal
