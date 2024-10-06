import pyttsx3 as p
import speech_recognition as sr
import webbrowser
import wikipedia
import pyjokes
import time
import threading
from datetime import datetime, timedelta

# Initialize the text-to-speech engine
engine = p.init()

# Set the speech rate
rate = engine.getProperty('rate')
engine.setProperty('rate', 180)

# Set the voice
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[0].id)

# Define a function to speak text
def speak(text):
    engine.say(text)
    engine.runAndWait()

# Initialize the speech recognition engine
r = sr.Recognizer()

# Reminder list
reminders = []

# Function to check reminders continuously
def check_reminders():
    while True:
        current_time = datetime.now()
        for reminder in reminders[:]:
            if current_time >= reminder[1]:
                speak(f"Reminder: {reminder[0]}")
                reminders.remove(reminder)
        time.sleep(10)  # Check every 10 seconds

# Start the reminder checker in a separate thread
reminder_thread = threading.Thread(target=check_reminders, daemon=True)
reminder_thread.start()

# Introduce the voice assistant
speak("Hello! I am LEO, your voice assistant. I'm here to help you with anything you need. Just ask!")

asleep = False  # Initially, the assistant is awake

while True:
    # Listen for user input
    with sr.Microphone() as source:
        r.adjust_for_ambient_noise(source, duration=1.2)  # Adjust ambient noise
        print("Listening...")

        try:
            audio = r.listen(source, timeout=5)
            text = r.recognize_google(audio, language='en-IN')  # Specify Indian English
            print(text)

            # If the assistant is asleep, listen for the wake-up call
            if asleep:
                if "hello leo" in text.lower():
                    asleep = False
                    speak("Hello! How can I assist you?")  # Respond upon waking
                continue

            # Process the user's request if awake
            if "hello" in text.lower():
                speak("Hello! How can I assist you today?")
            elif "what is your name" in text.lower():
                speak("My name is LEO, and I'm your voice assistant. How can I help you today?")
            elif "ok bye" in text.lower():
                speak("Goodbye! It was nice chatting with you.")
                break
            
            # Random joke from the pyjokes library
            elif "tell me a joke" in text.lower():
                joke = pyjokes.get_joke()
                speak(joke)
            
            # YouTube
            elif "open youtube" in text.lower():
                webbrowser.open("https://www.youtube.com")
                speak("YouTube is now open.")
                
            # Google
            elif "open google" in text.lower():
                webbrowser.open("https://www.google.com")
                speak("Google is now open.")
                
            # Weather
            elif "what's the weather like" in text.lower():
                webbrowser.open("https://www.accuweather.com/en/in/india-weather")
                speak("Weather is now open.")
                
            # News
            elif "tell me about today's news" in text.lower():
                webbrowser.open("https://news.google.com/")
                speak("Google News is now open.")
                
            # ChatGPT
            elif "open chat gpt" in text.lower():
                webbrowser.open("https://chat.openai.com")
                speak("ChatGPT is now open.")
                
            # Gemini
            elif "open gemini" in text.lower():
                webbrowser.open("https://gemini.com")
                speak("Gemini is now open.")
                
            # Time
            elif "what's the time" in text.lower() or "tell me the time" in text.lower():
                current_time = datetime.now().strftime("%I:%M %p")  # Format the time
                speak(f"The current time is {current_time}.")
                
            # Play a song
            elif "play a song" in text.lower() or "play music" in text.lower():
                webbrowser.open("https://www.youtube.com/results?search_query=music")
                speak("Playing music for you.")
            
            # Wikipedia
            elif "tell me about" in text.lower() or "about" in text.lower():
                if "tell me about" in text.lower():
                    topic = text.lower().replace("tell me about", "").strip()
                elif "about" in text.lower():
                    topic = text.lower().replace("about", "").strip()

                try:
                    summary = wikipedia.summary(topic, sentences=2)  
                    speak(summary)
                except wikipedia.exceptions.DisambiguationError:
                    speak("There are multiple topics related to that. Please be more specific.")
                except wikipedia.exceptions.PageError:
                    speak("I couldn't find any information on that topic.")
                except Exception as e:
                    print(f"An error occurred while fetching Wikipedia info: {e}")
                    speak("Sorry, I couldn't fetch the information.")
            
            # Set a reminder
            elif "set reminder" in text.lower():
                speak("What should I remind you about?")
                with sr.Microphone() as source:
                    reminder_audio = r.listen(source, timeout=5)
                    reminder_text = r.recognize_google(reminder_audio, language='en-IN')  # Specify Indian English
                    print(f"Reminder: {reminder_text}")

                speak("In how many seconds or minutes should I remind you?")
                with sr.Microphone() as source:
                    time_audio = r.listen(source, timeout=5)
                    reminder_time_str = r.recognize_google(time_audio, language='en-IN')  # Specify Indian English
                    print(f"Reminder time: {reminder_time_str}")

                try:
                    reminder_time = 0
                    parts = reminder_time_str.split()
                    
                    for part in parts:
                        if part.isdigit():
                            index = parts.index(part)  
                            if index + 1 < len(parts):
                                if "second" in parts[index + 1] or "seconds" in parts[index + 1]:
                                    reminder_time += int(part)  # Add seconds
                                elif "minute" in parts[index + 1] or "minutes" in parts[index + 1]:
                                    reminder_time += int(part) * 60  # Convert minutes to seconds

                    reminder_datetime = datetime.now() + timedelta(seconds=reminder_time)
                    reminders.append((reminder_text, reminder_datetime))

                    # singular/plural handling
                    if reminder_time == 1:
                        time_unit = "minute" if "minute" in reminder_time_str else "second"
                    elif reminder_time % 60 == 0 and reminder_time // 60 == 1:
                        time_unit = "minute"
                    elif reminder_time % 60 == 0:
                        time_unit = "minutes"
                    else:
                        time_unit = "seconds"

                    speak(f"Reminder set for {reminder_text} in {reminder_time} {time_unit}.")
                except ValueError:
                    speak("Sorry, I couldn't understand the reminder time. Please try again.")
            
            else:
                speak("I didn't understand that. Can you please rephrase?")

            # After handling a request, go to sleep
            asleep = True

        except sr.UnknownValueError:
            if not asleep:
                speak("Sorry, I didn't catch that. Can you please repeat?")
        except sr.RequestError:
            speak("Sorry, there was an error processing your request. Please try again.")
        except Exception as e:
            print(f"An error occurred: {e}")  # Print error to console for debugging
