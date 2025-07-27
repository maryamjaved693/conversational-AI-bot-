import wave
import pyaudio
import requests
import json
from deepgram import Deepgram
from gtts import gTTS
import simpleaudio as sa
import os

# Set your API keys here
DEEPGRAM_API_KEY = 'your'
GROQ_API_KEY = 'your key'

# Step 1: Record audio from mic
def record_audio(filename="input.wav", duration=5):
    chunk = 1024
    sample_format = pyaudio.paInt16
    channels = 1
    fs = 44100

    print("🎤 Recording...")
    p = pyaudio.PyAudio()
    stream = p.open(format=sample_format,
                    channels=channels,
                    rate=fs,
                    frames_per_buffer=chunk,
                    input=True)

    frames = []
    for _ in range(0, int(fs / chunk * duration)):
        data = stream.read(chunk)
        frames.append(data)

    stream.stop_stream()
    stream.close()
    p.terminate()

    wf = wave.open(filename, 'wb')
    wf.setnchannels(channels)
    wf.setsampwidth(p.get_sample_size(sample_format))
    wf.setframerate(fs)
    wf.writeframes(b''.join(frames))
    wf.close()
    print("✅ Recording finished")

# Step 2: Transcribe audio with Deepgram
def transcribe_audio(filename="input.wav"):
    print("📝 Transcribing...")
    dg_client = Deepgram(DEEPGRAM_API_KEY)

    with open(filename, 'rb') as audio:
        source = {'buffer': audio, 'mimetype': 'audio/wav'}
        options = {'punctuate': True, 'language': 'en'}

        response = dg_client.transcription.sync_prerecorded(source, options)

    transcript = response['results']['channels'][0]['alternatives'][0]['transcript']
    print("🧠 Transcribed Text:", transcript)
    return transcript


def generate_response(prompt):
    print("🤖 Generating response...")
    url = "https://api.groq.com/openai/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json"
    }
    payload = {
         "model": "llama3-8b-8192",
        "messages": [{"role": "user", "content": prompt}],
        "temperature": 0.7
    }

    try:
        response = requests.post(url, headers=headers, json=payload)
        result = response.json()
        print("🔍 Full API Response:", result)
        reply = result["choices"][0]["message"]["content"]
        print("💬 Assistant:", reply)
        return reply
    except Exception as e:
        print("❌ Error in response:", e)
        print("📦 Full response content:", response.text)
        return "Sorry, I couldn’t generate a response."

# Step 4: Convert response to speech using gTTS
import pygame

def speak_text(text):
    print("🔊 Speaking...")
    tts = gTTS(text=text, lang='en')
    tts.save("output.mp3")

    pygame.mixer.init()
    pygame.mixer.music.load("output.mp3")
    pygame.mixer.music.play()
    while pygame.mixer.music.get_busy():
        continue

    os.remove("output.mp3")



# Step 5: Main function
def main():
    record_audio()
    user_input = transcribe_audio()
    if user_input.strip() == "":
        print("⚠️ No speech detected.")
        return
    response = generate_response(user_input)
    speak_text(response)

if __name__ == "__main__":
    main()
