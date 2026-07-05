import queue
import time
import threading
import datetime
import requests
import pyttsx3
import speech_recognition as sr

# ===============================
# Put your API keys here (replace placeholders)
# ===============================
GEMINI_API_KEY = "GEMINI_API_KEY"
WEATHER_API_KEY = "WEATHER_API_KEY"

# ===============================
# TTS setup
# ===============================
engine = pyttsx3.init()
engine.setProperty('rate', 170)
engine.setProperty('volume', 1.0)
voices = engine.getProperty('voices')
# choose an index that exists on your system (0,1,...)
engine.setProperty('voice', voices[1].id)

def speak(text):
    """Speak from the main thread only. Stop engine first to clear queue."""
    text = str(text).strip()
    if not text:
        return
    engine.stop()
    print("Jarvis:", text)
    engine.say(text)
    engine.runAndWait()
    time.sleep(0.15)  # small pause so audio device can settle

# ===============================
# Gemini (HTTP) helper
# ===============================
def query_gemini(prompt):
    MODEL = "models/gemini-2.5-flash"
    url = f"https://generativelanguage.googleapis.com/v1beta/{MODEL}:generateContent"
    headers = {"Content-Type": "application/json"}
    payload = {"contents": [{"parts": [{"text": prompt}]}]}
    try:
        resp = requests.post(f"{url}?key={GEMINI_API_KEY}", headers=headers, json=payload, timeout=20)
        if resp.status_code != 200:
            return f"Gemini API error {resp.status_code}: {resp.text}"
        j = resp.json()
        return j["candidates"][0]["content"]["parts"][0]["text"].strip()
    except Exception as e:
        return f"Gemini API error: {e}"

# ===============================
# Weather helper (weatherapi.com)
# ===============================
def get_weather(city):
    try:
        url = f"http://api.weatherapi.com/v1/current.json?key={WEATHER_API_KEY}&q={city}&aqi=no"
        resp = requests.get(url, timeout=10)
        if resp.status_code != 200:
            return f"Weather API error {resp.status_code}: {resp.text}"
        data = resp.json()
        if "current" not in data:
            return "Couldn't fetch weather."
        temp = data["current"]["temp_c"]
        cond = data["current"]["condition"]["text"]
        return f"The current temperature in {city} is {temp}°C and {cond}."
    except Exception as e:
        return f"Weather API error: {e}"

# ===============================
# Speech recognition (background)
# ===============================
recognizer = sr.Recognizer()
mic = sr.Microphone()
q = queue.Queue()

def callback(recognizer, audio):
    """This runs in background thread — put recognized phrases into queue."""
    try:
        text = recognizer.recognize_google(audio, language="en-in")
        text = text.strip().lower()
        if text:
            print("Recognized (bg):", text)
            q.put(text)
    except sr.UnknownValueError:
        # ignore unrecognized chunks
        pass
    except sr.RequestError as e:
        print("Speech recognition request error:", e)

def start_listening():
    """Start background listening and return stop function."""
    return recognizer.listen_in_background(mic, callback, phrase_time_limit=8)

# ===============================
# Main program
# ===============================
def main():
    # calibrate ambient noise once
    with mic:
        print("Calibrating microphone for ambient noise (1s)...")
        recognizer.adjust_for_ambient_noise(mic, duration=1)

    stop_listening = start_listening()
    speak("Hello! I am Jarvis. I am online. Speak now.")

    try:
        while True:
            # block until a phrase arrives from callback
            command = q.get()  # blocks
            if not command:
                continue

            # stop listening so our TTS doesn't get recorded
            stop_listening(wait_for_stop=True)

            # handle commands
            if "exit" in command or "quit" in command:
                speak("Goodbye!")
                break

            elif "weather" in command:
                # user might say "weather in mumbai" or just "weather"
                if "in" in command:
                    city = command.split("in", 1)[-1].strip()
                else:
                    speak("Which city?")
                    # temporarily listen once for city
                    with mic:
                        recognizer.adjust_for_ambient_noise(mic, duration=0.3)
                        audio = recognizer.listen(mic, timeout=5, phrase_time_limit=6)
                    try:
                        city = recognizer.recognize_google(audio, language="en-in")
                    except Exception:
                        city = ""
                if not city:
                    speak("I didn't get the city name.")
                else:
                    speak("Checking weather...")
                    weather_info = get_weather(city)
                    speak(weather_info)

            elif "time" in command:
                now = datetime.datetime.now().strftime("%I:%M %p")
                speak(f"The time is {now}")

            else:
                speak("Let me ask Gemini...")
                response = query_gemini(command)
                speak(response)

            # small pause then restart background listening
            time.sleep(0.25)
            stop_listening = start_listening()

    finally:
        # ensure microphone thread is stopped
        try:
            stop_listening(wait_for_stop=True)
        except Exception:
            pass

if __name__ == "__main__":
    main()
