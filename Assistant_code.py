import pyttsx3
import speech_recognition as sr
import datetime
import wikipedia
import webbrowser as wb
import pywhatkit as pw
import os
import random
import subprocess

# Initialize the text-to-speech engine
speech_engine = pyttsx3.init('sapi5')
speech_engine.setProperty('rate', 200)
speech_engine.setProperty('volume', 1)

# Setting voice to first one
voices = speech_engine.getProperty('voices')
speech_engine.setProperty('voice', voices[0].id)

def speak(audio):
    """Convert text to speech."""
    speech_engine.say(audio)
    speech_engine.runAndWait()

def takeCommands():
    rcg = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        audio = rcg.listen(source)
    try:
        print("Recognizing...")
        text = rcg.recognize_google(audio)
        print("User said:",text)
        return text.lower()

    except Exception as e:
        print("Please repeat again...")
        return None

def greetMe():
    """Greet the user based on the time of day."""
    hour = int(datetime.datetime.now().hour)
    if hour >= 0 and hour < 12:
        speak("Good Morning!")
    elif hour >= 12 and hour < 18:
        speak("Good Afternoon!")
    else:
        speak("Good Evening!")
    speak("Ready to comply. What can I do for you?")

def searchWikipedia(query, num_sentences=3):
    """Search Wikipedia and return a summary."""
    speak("Searching Wikipedia...")
    result = wikipedia.summary(query, sentences=num_sentences)
    speak("According to Wikipedia")
    print(result)
    speak(result)

def openGoogle(search_query=None):
    """Open Google and optionally search for a query."""
    if search_query:
        wb.open(f"https://www.google.com/search?q={search_query}")
    else:
        wb.open('https://www.google.com')

def playYouTube(video_query):
    """Play a YouTube video based on a search query."""
    speak("Playing on YouTube")
    pw.playonyt(video_query)

def openNotepad():
    """Open Notepad."""
    path = r"C:\Windows\notepad.exe"
    os.startfile(path)

def closeNotepad():
    """Close Notepad."""
    os.system("taskkill /f /im Notepad.exe")

def playMusic():
    """Play a random song from the music directory."""
    music_path = r"C:\Users\lhema\Music"
    songs = os.listdir(music_path)
    os.startfile(os.path.join(music_path, random.choice(songs)))
    #os.system("tasklist")

def stopMusic():
    """Stop the music player."""
    os.system("taskkill /f /im Microsoft.Media.Player.exe")

def getCurrentTime():
    """Get and speak the current time."""
    strTime = datetime.datetime.now().strftime("%H:%M:%S")
    print(strTime)
    speak(f"The current time is {strTime}")

def shutDownSystem():
    """Shut down the system."""
    os.system("shutdown /s /t 5")

def restartSystem():
    """Restart the system."""
    os.system("shutdown /r /t 5")

def executeCommand(command):
    """Execute the command based on user input."""
    if 'assistant' in command:
        speak('Yes, I am here.')
    
    elif 'what is' in command or 'who is' in command:
        search_query = command.replace("what is", "").replace("who is", "")
        searchWikipedia(search_query)

    elif 'just open google' in command:
        openGoogle()

    elif 'open google' in command:
        speak("What should I search?")
        search_query = takeCommands()
        openGoogle(search_query)

    elif 'just open youtube' in command:
        wb.open('youtube.com')

    elif 'open youtube' in command:
        speak("What would you like to watch?")
        video_query = takeCommands()
        playYouTube(video_query)

    elif 'close browser' in command:
        os.system("taskkill /f /im msedge.exe")

    elif 'open notepad' in command:
        openNotepad()

    elif 'close notepad' in command:
        closeNotepad()

    elif 'play music' in command:
        playMusic()

    elif 'stop music' in command:
        stopMusic()

    elif 'current time please' in command:
        getCurrentTime()

    elif 'shut down the system' in command:
        shutDownSystem()

    elif 'restart the system' in command:
        restartSystem()

    elif 'exit' in command or 'stop' in command:
        speak("Shutting down. Goodbye!")
        return False  # Signal to exit the loop
    return True  # Continue the loop

if __name__ == "__main__":
    greetMe()
    while True:
        command = takeCommands()
        if command:
            if not executeCommand(command):
                break  # Exit the loop if the command signals to stop
