import google.generativeai as genai
import speech_recognition as sr
import pyttsx3
import os
import webbrowser
import datetime
import pywhatkit
import requests
import smtplib
import time
import calendar
import pytz
import random

# Set up Gemini API Key
API_KEY = "GEMINI_API_KEY"
genai.configure(api_key=API_KEY)

# Initialize Text-to-Speech Engine
engine = pyttsx3.init()
engine.setProperty("rate", 200)

# Set voice - try Daniel, else fallback to first available voice
voices = engine.getProperty("voices")
selected_voice = None
for voice in voices:
    if "Daniel" in voice.name:
        selected_voice = voice
        break
if not selected_voice:
    selected_voice = voices[0]  # fallback
engine.setProperty("voice", selected_voice.id)

# Memory Storage
memory = []

# Function to make AI speak
def say(text):
    global engine
    print(f"Jarvis speaking: {text}")  # Debug print
    engine.say(text)
    engine.runAndWait()

# Function to take voice command
def take_command():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        r.adjust_for_ambient_noise(source)
        audio = r.listen(source)
        try:
            print("Recognizing...")
            query = r.recognize_google(audio, language="en-in")
            print(f"User: {query}")
            if "stop" in query.lower():
                engine.stop()
                return "stop"
            return query.lower()
        except sr.UnknownValueError:
            print("Speech not understood")
            return "Sorry, I didn't catch that."
        except sr.RequestError:
            print("Speech recognition service unavailable")
            return "Speech recognition service is unavailable."

# Function to process AI response
def ask_ai(query):
    global memory
    try:
        model = genai.GenerativeModel("models/gemini-2.5-flash")
        full_context = "\n".join(memory[-10:])
        prompt = f"Previous conversation:\n{full_context}\n\nUser: {query}\nAI:"
        response = model.generate_content(prompt)
        response_text = response.text
        print(f"Jarvis: {response_text}")
        say(response_text)
        memory.append(f"User: {query}")
        memory.append(f"AI: {response_text}")
        return response_text
    except Exception as e:
        print("Error:", e)
        say("Sorry, I couldn't process that.")
        return "Sorry, I couldn't process that."

# Function to get weather updates
def get_weather(city):
    api_key = "WEATHER_API_KEY"  
    base_url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"
    try:
        response = requests.get(base_url)
        data = response.json()
        if data["cod"] != "404":
            temp = data["main"]["temp"]
            description = data["weather"][0]["description"]
            say(f"The current temperature in {city} is {temp}°C with {description}.")
        else:
            say("Sorry, I couldn't find the weather for that location.")
    except Exception as e:
        print("Error:", e)
        say("I couldn't fetch the weather details.")

# Function to send WhatsApp message
def send_whatsapp_message(number, message):
    try:
        say(f"Sending WhatsApp message to {number}")
        pywhatkit.sendwhatmsg_instantly(number, message)
        say("Message sent successfully!")
    except Exception as e:
        print("Error:", e)
        say("I couldn't send the message.")

# Function to send an email
def send_email(to, subject, message):
    sender_email = "your_email@gmail.com"
    sender_password = "your_password"  # Use App Passwords if needed
    try:
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.starttls()
        server.login(sender_email, sender_password)
        msg = f"Subject: {subject}\n\n{message}"
        server.sendmail(sender_email, to, msg)
        server.quit()
        say("Email sent successfully!")
    except Exception as e:
        print("Error:", e)
        say("I couldn't send the email.")

# Function to set alarms
def set_alarm(hours, minutes):
    now = datetime.datetime.now().strftime("%H:%M")
    say(f"Alarm set for {hours}:{minutes}.")
    while True:
        current_time = datetime.datetime.now().strftime("%H:%M")
        if current_time == f"{hours}:{minutes}":
            say("Wake up! It's time.")
            break
        time.sleep(30)

# Function to fetch Wikipedia summaries
def search_wikipedia(topic):
    try:
        import wikipedia
        summary = wikipedia.summary(topic, sentences=2)
        say(summary)
    except Exception as e:
        print("Error:", e)
        say("I couldn't find anything on Wikipedia.")

# Function to tell jokes
def tell_joke():
    jokes = [
        "Why don't programmers like nature? Because it has too many bugs.",
        "Why do Java developers wear glasses? Because they can't C#.",
        "How does a computer catch a fish? With its internet!"
    ]
    joke = random.choice(jokes)
    say(joke)

# Function to play YouTube videos
def play_on_youtube(query):
    search_query = query.replace("play", "").replace("on youtube", "").strip()
    say(f"Playing {search_query} on YouTube")
    pywhatkit.playonyt(search_query)

# Main loop
def main_loop():
    while True:
        query = take_command()

        if query == "stop" or query == "exit":
            say("Goodbye! I will listen for hotword again.")
            break

        elif "open youtube" in query:
            say("Opening YouTube")
            webbrowser.open("https://www.youtube.com")

        elif "open google" in query:
            say("Opening Google")
            webbrowser.open("https://www.google.com")

        elif "play" in query and "on youtube" in query:
            play_on_youtube(query)

        elif "what's the weather in" in query:
            city = query.replace("what's the weather in", "").strip()
            get_weather(city)

        elif "send whatsapp" in query:
            say("Who should I send the message to?")
            number = take_command()
            say("What should I say?")
            message = take_command()
            send_whatsapp_message(number, message)

        elif "send email" in query:
            say("Who should I send it to?")
            recipient = take_command()
            say("What's the subject?")
            subject = take_command()
            say("What's the message?")
            message = take_command()
            send_email(recipient, subject, message)

        elif "set an alarm for" in query:
            time_parts = query.replace("set an alarm for", "").strip().split(":")
            if len(time_parts) == 2:
                set_alarm(time_parts[0], time_parts[1])
            else:
                say("Please specify time as hours and minutes.")

        elif "joke" in query:
            tell_joke()

        elif "search wikipedia for" in query:
            topic = query.replace("search wikipedia for", "").strip()
            search_wikipedia(topic)

        else:
            ask_ai(query)

# Hotword activation loop
def hotword_activation():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        r.adjust_for_ambient_noise(source)
        while True:
            try:
                print("Listening for 'Hey Jarvis'...")
                audio = r.listen(source)
                command = r.recognize_google(audio, language="en-in").lower()
                print(f"Hotword listener heard: {command}")
                if "hey jarvis" in command:
                    say("Yes, how can I assist you?")
                    main_loop()  # After main loop ends, resumes hotword listening
            except sr.UnknownValueError:
                continue
            except sr.RequestError:
                say("Speech recognition service is unavailable.")

# Start hotword activation
hotword_activation()
