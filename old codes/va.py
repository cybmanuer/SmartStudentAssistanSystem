# import streamlit as st
# import pyttsx3
# import speech_recognition as sr
# import datetime
# import wikipedia
# import webbrowser
# import os
# import requests
# import pyjokes
# import json
# import pywhatkit
# import time
# import subprocess
# import pyautogui
# from googletrans import Translator
# from bs4 import BeautifulSoup

# # Initialize text-to-speech engine
# engine = pyttsx3.init('sapi5')
# voices = engine.getProperty('voices')
# engine.setProperty('voice', voices[0].id)

# def speak(text):
#     engine.say(text)
#     engine.runAndWait()

# def textcreate(message):
#     st.write(message)

# def wishMe():
#     hour = datetime.datetime.now().hour
#     if 0 <= hour < 12:
#         speak("Good morning Master")
#         textcreate("Good morning Master")
#     elif 12 <= hour < 18:
#         speak("Good afternoon Master")
#         textcreate("Good afternoon Master")
#     else:
#         speak("Good evening Master")
#         textcreate("Good evening Master")
#     speak('I am your Virtual Assistant. How Can I Help You Today')
#     textcreate('I am your Virtual Assistant. How Can I Help You Today')

# def takeCommand():
#     r = sr.Recognizer()
#     with sr.Microphone() as source:
#         st.write("Listening...")
#         audio = r.listen(source)
    
#     try:
#         query = r.recognize_google(audio, language='en-in')
#         message = f"YOU said: {query}"
#         textcreate(message)
#     except sr.UnknownValueError:
#         message = 'NO AUDIO HEARD......'
#         textcreate(message)
#         query = takeCommand()
    
#     return query

# def get_current_date():
#     current_date = datetime.datetime.now().strftime("%B %d, %Y")
#     message = current_date
#     textcreate(message)
#     speak(f"Master, Today's date is {current_date}")

# def searchGoogle(query, num_sentences=5):
#     url = f"https://www.google.com/search?q={query}"
#     response = requests.get(url)
#     soup = BeautifulSoup(response.text, "html.parser")
#     search_result = soup.find("div", class_="BNeawe s3v9rd AP7Wnd").get_text()
#     sentences = search_result.split(".")
#     result = ". ".join(sentences[:num_sentences])
#     return result

# def tellJoke():
#     joke = pyjokes.get_joke()
#     message = "ME: " + joke
#     textcreate(message)    
#     speak("Here's a joke for you:")
#     speak(joke)

# def getLatestNews():
#     url = "https://news.google.com/rss"
#     response = requests.get(url)
#     soup = BeautifulSoup(response.text, "lxml")
#     news_list = soup.find_all("item")
#     latest_news = []
    
#     for i, news in enumerate(news_list[:10]):
#         title = news.title.text
#         latest_news.append(title)
    
#     return latest_news

# def getWeatherReport(city):
#     api_key = "YOUR_API_KEY"  # Replace with your OpenWeather API key
#     url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}"
    
#     response = requests.get(url)
#     data = json.loads(response.text)

#     main_weather = data['weather'][0]['main']
#     description = data['weather'][0]['description']
#     temperature = data['main']['temp']
    
#     report = f"The weather in {city} is {main_weather} with a temperature of {temperature}K."
    
#     return report

# def take_screenshot():
#     if not os.path.exists("screenshots"):
#         os.makedirs("screenshots")
    
#     current_time = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
#     screenshot_path = os.path.join("screenshots", f"screenshot_{current_time}.png")
    
#     pyautogui.screenshot(screenshot_path)
    
# def open_application(application_name):
#     application_name = application_name.lower()
    
#     application_paths = {
#         "notepad": r"C:\\Windows\\System32\\notepad.exe",
#         "calculator": r"C:\\Windows\\System32\\calc.exe",
#         "explorer": r"C:\\Windows\\explorer.exe",
#         "chrome": r"C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe",
#         "control panel": r"C:\\Windows\\System32\\control.exe",
#         "task manager": r"C:\\Windows\\System32\\taskmgr.exe"
#     }

#     application_path = application_paths.get(application_name)
    
#     if application_path:
#         subprocess.Popen(application_path)
#         speak(f"Opening {application_name} application")
        
# def showOperations():
#     operations =[ 
#         "1. Get the current time",
#         "2. Get the current date",
#         "3. Tell a joke",
#         "4. Take a screenshot",
#         "5. Start a countdown",
#         "6. Get the latest news",
#         "7. Get the weather report",
#         "8. Open applications"
#      ]
     
#     for operation in operations:
#          textcreate(operation)

# # Streamlit UI setup
# st.title("Virtual Assistant")

# def start_virtual_assistant():
#     speak("STARTING...")
#     textcreate("Starting virtual assistant...")
#     wishMe()
#     while True:
#          query = takeCommand()

#          if 'shutdown' in query.lower() or 'exit' in query.lower() or 'stop' in query.lower():
#              speak("Okay Master.. I am leaving!")
#              break

#          elif 'time' in query.lower() or 'what is the time' in query.lower():
#              strTime = datetime.datetime.now().strftime("%H:%M:%S")
#              speak(f"Master the time is {strTime}")

#          elif 'date' in query.lower() or 'what is the date' in query.lower():
#              get_current_date()

#          elif 'joke' in query.lower():
#              tellJoke()

#          elif 'latest news' in query.lower():
#              news = getLatestNews()
#              for headline in news:
#                  textcreate(headline)

#          elif 'weather' in query.lower():
#              city_name = takeCommand()
#              weather_report = getWeatherReport(city_name)
#              textcreate(weather_report)

#          elif 'open application' in query.lower():
#              app_name = takeCommand()
#              open_application(app_name)

#          # Add more commands as needed...

#          elif 'weather' in query.lower() or 'weather report' in query.lower():
#              speak("Please provide the city name for the weather report.")
#              city_name = takeCommand()
#              weather_report = getWeatherReport(city_name)
#              textcreate(weather_report)

#          elif 'screenshot' in query.lower() or 'take a screenshot' in query.lower():
#              speak("Taking a screenshot...")
#              take_screenshot() 

#          elif 'countdown' in query.lower() or 'start countdown' in query.lower():
#              speak("How many seconds for the countdown?")
#              countdown_seconds = int(takeCommand())
#              speak(f"Starting countdown for {countdown_seconds} seconds...")
#              countdown(countdown_seconds) 

#          elif 'play video on youtube' in query.lower() or 'search youtube' in query.lower():
#              video_query = query.replace('play video on youtube', '').strip()
#              speak(f"Playing {video_query} on YouTube...")
#              pywhatkit.playonyt(video_query) 

#          elif 'search information on wikipedia' in query.lower():
#              speak("What do you want to search on Wikipedia?")
#              wiki_query = takeCommand()
#              speak('Searching Wikipedia...')
#              try:
#                  results = wikipedia.summary(wiki_query, sentences=2)
#                  textcreate(results)
#                  speak(results)
#              except wikipedia.exceptions.PageError:
#                  speak("Sorry, I couldn't find any information on that topic.")
#              except wikipedia.exceptions.DisambiguationError:
#                  speak("There are multiple results for that query. Please be more specific.") 

#          elif 'open mail' in query.lower() or 'open gmail' in query.lower():
#              speak("Opening Gmail...")
#              webbrowser.open("https://mail.google.com") 

#          elif 'play music' in query.lower() or 'play song' in query.lower():
#              speak("Playing music...")
#              songs_dir = "C:\\Users\\manu\\Music\\MUSIC"
#              songs = os.listdir(songs_dir)
#              os.startfile(os.path.join(songs_dir, songs[0])) 

#          elif 'hello' in query.lower() or 'hi' in query.lower():
#              textcreate("Hello...")
#              speak('Hello! How can I assist you today?') 
             
#          elif 'stop' in query.lower() or 'exit' in query.lower():
#              speak("Okay Master, I am shutting down now.")
#              break

# # Streamlit UI execution
# if __name__ == "__main__":
#     st.button('Start Assistant', on_click=start_virtual_assistant)
#     # if st.button('Start Assistant'):
#     #     start_virtual_assistant()




# // good interface

# import streamlit as st
# import pyttsx3
# import speech_recognition as sr
# import datetime
# import wikipedia
# import requests
# import pyjokes
# import os
# import json
# import pywhatkit
# import pyautogui
# from bs4 import BeautifulSoup
# from googletrans import Translator

# # Initialize text-to-speech engine
# engine = pyttsx3.init('sapi5')
# voices = engine.getProperty('voices')
# engine.setProperty('voice', voices[0].id)

# def speak(text):
#     """Speak the provided text."""
#     engine.say(text)
#     engine.runAndWait()

# def wish_me():
#     """Wish the user based on the current time."""
#     hour = datetime.datetime.now().hour
#     if 0 <= hour < 12:
#         speak("Good morning!")
#     elif 12 <= hour < 18:
#         speak("Good afternoon!")
#     else:
#         speak("Good evening!")
#     speak("I am your Virtual Assistant. How can I help you today?")

# def get_current_date():
#     """Fetch and display the current date."""
#     current_date = datetime.datetime.now().strftime("%B %d, %Y")
#     speak(f"Today's date is {current_date}.")
#     return f"Today's date is {current_date}."

# def tell_joke():
#     """Fetch and return a random joke."""
#     return pyjokes.get_joke()

# def get_weather_report(city):
#     """Fetch the weather report for a given city."""
#     api_key = "your_openweather_api_key"
#     url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"
#     response = requests.get(url)
#     data = response.json()

#     if response.status_code == 200:
#         weather = data["weather"][0]["description"].capitalize()
#         temp = data["main"]["temp"]
#         humidity = data["main"]["humidity"]
#         return f"The weather in {city} is {weather} with a temperature of {temp}°C and humidity of {humidity}%."
#     else:
#         return "Sorry, I couldn't fetch the weather details."

# def take_screenshot():
#     """Take a screenshot and save it to the screenshots folder."""
#     if not os.path.exists("screenshots"):
#         os.makedirs("screenshots")
#     current_time = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
#     screenshot_path = os.path.join("screenshots", f"screenshot_{current_time}.png")
#     pyautogui.screenshot(screenshot_path)
#     return f"Screenshot saved to {screenshot_path}."

# def search_wikipedia(query):
#     """Search Wikipedia and return the summary."""
#     try:
#         results = wikipedia.summary(query, sentences=2)
#         return results
#     except wikipedia.exceptions.PageError:
#         return "Sorry, I couldn't find any information on that topic."
#     except wikipedia.exceptions.DisambiguationError:
#         return "There are multiple results for that query. Please be more specific."

# # Streamlit UI
# st.title("Virtual Assistant")
# st.sidebar.header("Assistant Commands")

# # Sidebar menu
# menu = st.sidebar.selectbox(
#     "Choose an operation",
#     ["Greet", "Get Date", "Tell a Joke", "Weather Report", "Take Screenshot", "Wikipedia Search"]
# )

# # Display output based on selected operation
# if menu == "Greet":
#     st.subheader("Greeting")
#     wish_me()

# elif menu == "Get Date":
#     st.subheader("Today's Date")
#     st.write(get_current_date())

# elif menu == "Tell a Joke":
#     st.subheader("Joke")
#     st.write(tell_joke())

# elif menu == "Weather Report":
#     st.subheader("Weather Report")
#     city = st.text_input("Enter city name:")
#     if st.button("Get Weather"):
#         report = get_weather_report(city)
#         st.write(report)

# elif menu == "Take Screenshot":
#     st.subheader("Take Screenshot")
#     if st.button("Capture"):
#         result = take_screenshot()
#         st.write(result)

# elif menu == "Wikipedia Search":
#     st.subheader("Wikipedia Search")
#     query = st.text_input("Enter search query:")
#     if st.button("Search"):
#         result = search_wikipedia(query)
#         st.write(result)

# # Footer
# st.write("Powered by Streamlit")



import streamlit as st
import pyttsx3
import speech_recognition as sr
import datetime
import wikipedia
import requests
import pyjokes
import os
import pyautogui
import time

# Initialize text-to-speech engine
engine = pyttsx3.init('sapi5')
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[0].id)

def speak(text):
    """Speak the provided text."""
    engine.say(text)
    engine.runAndWait()

def wish_me():
    """Wish the user based on the current time."""
    hour = datetime.datetime.now().hour
    if 0 <= hour < 12:
        speak("Good morning!")
    elif 12 <= hour < 18:
        speak("Good afternoon!")
    else:
        speak("Good evening!")
    speak("I am your Virtual Assistant. How can I help you?")

def take_command():
    """Listen to the user's voice and return the text command."""
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        st.write("Listening...")
        try:
            recognizer.adjust_for_ambient_noise(source)
            audio = recognizer.listen(source, timeout=5)
            st.write("Recognizing...")
            command = recognizer.recognize_google(audio, language='en-in')
            st.write(f"Command: {command}")
            return command.lower()
        except sr.UnknownValueError:
            return "Sorry, I could not understand that."
        except sr.RequestError:
            return "Request failed; check your internet connection."

def process_command(command):
    """Process the command and return a response."""
    if 'time' in command:
        current_time = datetime.datetime.now().strftime("%I:%M %p")
        return f"The time is {current_time}."
    elif 'date' in command:
        current_date = datetime.datetime.now().strftime("%B %d, %Y")
        return f"Today's date is {current_date}."
    elif 'joke' in command:
        return pyjokes.get_joke()
    elif 'weather' in command:
        city = command.replace("weather in", "").strip()
        return get_weather_report(city)
    elif 'screenshot' in command:
        return take_screenshot()
    elif 'search' in command:
        query = command.replace("search", "").strip()
        return search_wikipedia(query)
    elif 'thank you' in command:
        return "You're welcome!"
    elif 'exit' in command or 'stop' in command:
        st.session_state.listening = False
        return "Stopping assistant. Goodbye!"
    else:
        return "Sorry, I didn't understand that. Please try again."

def get_weather_report(city):
    """Fetch the weather report for a given city."""
    api_key = "your_openweather_api_key"  # Replace with your OpenWeatherMap API key
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"
    response = requests.get(url)
    data = response.json()
    if response.status_code == 200:
        weather = data["weather"][0]["description"].capitalize()
        temp = data["main"]["temp"]
        humidity = data["main"]["humidity"]
        return f"The weather in {city} is {weather} with a temperature of {temp}°C and humidity of {humidity}%."
    else:
        return "Sorry, I couldn't fetch the weather details."

def take_screenshot():
    """Take a screenshot and save it to the screenshots folder."""
    if not os.path.exists("screenshots"):
        os.makedirs("screenshots")
    current_time = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    screenshot_path = os.path.join("screenshots", f"screenshot_{current_time}.png")
    pyautogui.screenshot(screenshot_path)
    return f"Screenshot saved to {screenshot_path}."

def search_wikipedia(query):
    """Search Wikipedia and return the summary."""
    try:
        results = wikipedia.summary(query, sentences=2)
        return results
    except wikipedia.exceptions.PageError:
        return "Sorry, I couldn't find any information on that topic."
    except wikipedia.exceptions.DisambiguationError:
        return "There are multiple results for that query. Please be more specific."

# Streamlit Interface
st.title("Continuous Voice-Controlled Virtual Assistant")

# Initialize session state
if "listening" not in st.session_state:
    st.session_state.listening = False

# Buttons for controlling the assistant
if st.button("Start Listening"):
    st.session_state.listening = True
    wish_me()

if st.button("Stop Listening"):
    st.session_state.listening = False

# Container for displaying responses
response_container = st.empty()

# Continuous listening loop
while st.session_state.listening:
    command = take_command()
    if command:
        response = process_command(command)
        response_container.markdown(f"**Assistant:** {response}")  # Update the container
        speak(response)
    time.sleep(1)


chatgpt converstion

    //https://chatgpt.com/share/678026d1-5bac-8000-ae94-04cbafdb5400

    