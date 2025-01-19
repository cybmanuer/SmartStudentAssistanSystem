import cv2
import speech_recognition as sr
import pyttsx3
import threading
import datetime
import requests
import json
import pyjokes
import webbrowser

from scipy.spatial import distance as dist
from imutils import face_utils
import imutils
import dlib
import matplotlib.pyplot as plt
import pyttsx3


# ----------  VA
import datetime
import wikipedia
import webbrowser
import os
import pywhatkit
import time
import subprocess
import pyautogui
from googletrans import Translator
from bs4 import BeautifulSoup
from ecapture import ecapture as ec




# ------------

# Initialize the speech engine
engine = pyttsx3.init()

def speak(text):
    engine.say(text)
    engine.runAndWait()


#  ---------------------------  COMMAND DEFNATION -------------------------------------


def wishMe():
    hour = datetime.datetime.now().hour
    if 0 <= hour < 12:
        speak("Good morning Master")
    elif 12 <= hour < 18:
        speak("Good afternoon Master")
    else:
        speak("Good evening Master")
    speak(' I am your Virtual Assistant. How Can I Help You Today')



def textcreate(message):
    print(message)
#
# to take voice input and recognise the text
def takeCommand():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        message = "Listening..." #to output the msg to Screen
        textcreate(message)  #the function that outputs the msg to GUI      
        audio = r.listen(source) # to leaston the audio/input

    try: #to analyse or recognise the input 
        message = "Recognizing..." 
        textcreate(message)
        query = r.recognize_google(audio, language='en-in') # perform speech recognition using the Google Web Speech API.
        message = f" YOU said: {query}\n"
        textcreate(message)

        # if no voice/audio heard 
    except sr.UnknownValueError:
        message = 'NO AUDIO HEARD......'
        textcreate(message)
        query = takeCommand()

    return query

# TO FETCH THE DATE
def get_current_date():
    current_date = datetime.datetime.now().strftime("%B %d, %Y")
    message = current_date
    textcreate(message)
    speak(f" Master Today's date is {current_date}")


# for google search
def searchGoogle(query, num_sentences=5):
    url = f"https://www.google.com/search?q={query}"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")
    search_result = soup.find("div", class_="BNeawe s3v9rd AP7Wnd").get_text()
    sentences = search_result.split(".")
    result = ". ".join(sentences[:num_sentences])
    return result

# CODE TO TELL JOKE 
def tellJoke():
    joke = pyjokes.get_joke()
    message = "ME:" + joke
    textcreate(message)    
    speak("Here's a joke for you:")
    speak(joke)

# CODE TO FETCH LATEST  NEWS
def getLatestNews():
    url = "https://news.google.com/rss"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "lxml")
    news_list = soup.find_all("item")
    latest_news = []
    for i, news in enumerate(news_list[:10]):
        title = news.title.text
        latest_news.append(title)
        if i == 9:
            break
    return latest_news

# WETHER REPORT
def getWeatherReport(city):
    api_key = "bd5e378503939ddaee76f12ad7a97608"      # THE CODE IS IMPORTANT ,IT IS THE OPENWETHER USER API KEY THAT ALLOW ACCES TO FETCH THE DETAILS
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}"
    response = requests.get(url)     # Send a GET request to the API and retrieve the response
    data = json.loads(response.text)      # Parse the JSON response

    # Extract the relevant weather information
    main_weather = data['weather'][0]['main']
    description = data['weather'][0]['description']
    temperature = data['main']['temp']
    humidity = data['main']['humidity']
    wind_speed = data['wind']['speed']

    # Create the weather report string
    report = f"The weather in {city} is {main_weather}  " \
             f"The humidity is {humidity}% and the wind speed is {wind_speed} meter/second. "
    return report

# to take screen shot
def take_screenshot():
    # Create the screenshots folder if it doesn't exist
    if not os.path.exists("screenshots"):
        os.makedirs("screenshots")
    current_time = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    screenshot_path = os.path.join("screenshots", f"screenshot_{current_time}.png")
    pyautogui.screenshot(screenshot_path)
    speak("Screenshot taken and saved in Screenshot folder.")


# TIME COUNTER
def countdown(seconds):
    try :
        for i in range(seconds, 0, -1):
            message = f"Countdown: {i} seconds"
            textcreate(message)
            time.sleep(1)
            message = f"Countdown: {i} seconds"
            textcreate(message)
        speak("Countdown complete!")

    except ValueError:
        speak("Invalid input. Please enter a valid number of seconds.")
        textcreate("Invalid input. Please enter a valid number of seconds.")
        takeCommand()


# CODE TO OPEN ANY WEBSITE
def open_website(website):
    speak(f"Opening {website}")
    url = f"https://www.{website}.com"
    webbrowser.open(url)



# Open a local application
def open_application(application_name):
    application_name = application_name.lower()
    application_path = None
    
    # Define the paths for your applications
    application_paths = {
        "notepad": r"C:\\Windows\\System32\\notepad.exe",
        "calculator": r"C:\\Windows\\System32\\calc.exe",
        # "paint": r"C:\\Windows\\System32\\mspaint.exe",
        "explorer": r"C:\\Windows\\explorer.exe",
        "chrome": r"C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe",
        "control pannel": r"C:\\Windows\\System32\\control.exe",
        "task manager": r"C:\\Windows\\System32\\taskmgr.exe",
        "pictures" :r"C:\Users\manu\Pictures",
        "Documents":r"C:\Users\manu\Documents"
        # Add more applications and their paths here
    }

    # Find the path of the requested application
    if application_name in application_paths:
        application_path = application_paths[application_name]

    # Open the application if the path is found
    if application_path:
        subprocess.Popen(application_path)
        speak(f"Opening {application_name} application")
    else:
        speak(f"Sorry, I couldn't find the {application_name} application")


    # Find the path of the requested application
    if application_name in application_paths:
        application_path = application_paths[application_name]

    # Open the application if the path is found
    if application_path:
        subprocess.Popen(application_path)
        speak(f"Opening {application_name} application")
    else:
        speak(f"Sorry, I couldn't find the {application_name} application")

# Show the list of operations
def showOperations():
    speak("Here are some of the operations I can perform:")
    operations =[
        "1. Get the current time",
        "2. Get the current date",
        "3. Tell a joke",
        "4. Take a screenshot",
        "5. Start a countdown",
        "6. Play videos on YouTube",
        "7. Get the latest news",
        "8. Get the weather report",
        "9. Open The websites",
        "10. Open Mail ",
        "11. play music"
        "13. Search information on Wikipedia",
        "14. Search on Google"
        "15. open application"
    ]
    for operation in operations:
        speak(operation)
        # message = operation
        textcreate(operation)
        # return operation


# Function to stop the virtual assistant
def stop_virtual_assistant():
    textcreate("Stopping virtual assistant...")
    speak("Stopping virtual assistant...")





# -----------------------------

def recognize_voice():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening for commands...")
        while True:
            audio = recognizer.listen(source)
            try:
                command = recognizer.recognize_google(audio).lower()
                print(f"You said: {command}")
                process_command(command)
            except sr.UnknownValueError:
                print("Could not understand audio")
            except sr.RequestError as e:
                print(f"Could not request results; {e}")

def process_command(command):

            if 'shutdown' in query.lower() or 'exit' in query.lower() or 'stop' in query.lower():
                speak(" ok  Master.. I am Living... !")
                stop_virtual_assistant()

            elif 'time' in query.lower() or 'what is the time' in query.lower():
                strTime = datetime.datetime.now().strftime("%H:%M:%S")
                speak(f"Master the time is {strTime}")

            elif 'date' in query.lower() or 'what is the date' in query.lower():
                 get_current_date()
                 
         
            elif 'wikipedia' in query.lower() or 'search wikipedia' in query.lower() or 'in wikipedia' in query.lower() :
                speak('Searching Wikipedia...')
                query = query.replace("wikipedia", "")
                try:
                    results = wikipedia.summary(query, sentences=2)
                    textcreate(results)
                    speak(results)
                    # this line also search on wikipidia
                    # pywhatkit.info(query)
                except wikipedia.exceptions.PageError:
                    speak("Sorry, I couldn't find any information on that topic.")
                except wikipedia.exceptions.DisambiguationError:
                    speak("There are multiple results for that query. Please be more specific.")


            elif 'screenshot' in query.lower() or 'take a screenshot' in query.lower():
                    speak(" Taking a screenshot...")
                    take_screenshot()

            elif 'countdown' in query.lower() or ' start countdown' in query.lower():
                    speak("How many seconds for the countdown?")
                    countdown_seconds = int(takeCommand())
                    speak(f"Starting countdown for {countdown_seconds} seconds...")
                    countdown(countdown_seconds)

            elif 'another joke' in query.lower() or 'tell me a joke' in query.lower() or  'a joke' in query.lower()  :
                    tellJoke()

            elif 'who are you' in query.lower() or 'what is your name' in query.lower() or  'about you' in query.lower()  :
                    speak("I AM virtual  ASSISTANT created by Finall year students")

            elif 'operations' in query.lower() or 'what can you do' in query.lower() or 'what do you do' in query.lower():
                    showOperations()

            # elif 'open youtube' in query.lower():
            #     speak("opening Youtube")
            #     url = "https://www.youtube.com"
            #     webbrowser.open(url)

            # elif 'open google' in query.lower():
            #     speak("OPENING GOOGLE...")
            #     url = "https://www.google.com"
            #     webbrowser.open(url)


            elif 'open mail' in query.lower() or 'open g mail' in query.lower() or 'mail' in query.lower():
                    speak("OPENING mail")
                    url = "https://mail.google.com/mail/"
                    webbrowser.open(url)

            elif 'play music' in query.lower() or 'play song' in query.lower():
                    speak("Playing Music..")
                    songs_dir = "C:\\Users\\manu\\Music\\MUSIC"
                    songs = os.listdir(songs_dir)
                # print(songs)
                    os.startfile(os.path.join(songs_dir, songs[0]))

            elif 'in youtube' in query.lower() or 'play in youtube' in query.lower() or  'search youtube' in query.lower():
                    yot=query.replace('playing on youtube',"")
                    speak(yot)
                    pywhatkit.playonyt(yot)


            elif 'hello' in query.lower() or 'hii' in query.lower() :
                    textcreate("Hello...")
                    speak('Hello....')

            elif 'sing a song' in query.lower() or 'sing me a song' in query.lower() or 'can you sing a song' in query.lower() :
                    textcreate('sorry... i\'m not so good at it.. if you want i can play some good music for you... do you want me to do that')
                    speak('sorry... i\'m not so good at it.. if you want i can play some good music for you... do you want me to do that')
                    r=takeCommand()
                    if 'yes' in r:
                        speak("Playing Music..")
                        songs_dir = "C:\\Users\\manu\\Music\\MUSIC"
                        songs = os.listdir(songs_dir)
                        os.startfile(os.path.join(songs_dir, songs[0]))
                         
                    elif 'no' in r:
                        speak("ok master")

            elif ' Robert can you dance' in query.lower() or 'can you dance with me' in query.lower():
                    textcreate('sorry... i skipped those classes...')
                    speak('sorry... i skipped those classes...')

            # elif ' Do you have any hidden talents ' in query or ' hidden talents ':
            #         textcreate("Oh, I have plenty of hidden talents. Unfortunately, they're all hidden from me too.")
            #         speak("Oh, I have plenty of hidden talents. Unfortunately, they're all hidden from me too.")

            elif 'open website' in query.lower() or 'website' in query.lower():
                    speak("Sure, what website would you like to open?")
                    website_name = takeCommand().lower()
                    open_website(website_name)

            elif 'open application' in query.lower() or 'open app' in query.lower():
                    speak("Sure, what application would you like to open?")
                    app_name = takeCommand().lower()
                    open_application(app_name)

            

            elif 'latest news' in query.lower() or 'news' in query.lower():
                    speak("Fetching the latest news...")
                    news = getLatestNews()
                    # this code print 10 headlines but reads onlu 2 NEWS....
                    if news:
                        speak("Here are the top 10 latest news headlines. I will read two of them for you. please check remainingin the console.:")
                        for i, headline in enumerate(news[:2]):  # Limiting to the top two headlines
                            textcreate(f"{i + 1}. {headline}")
                            # print(f"{i + 1}. {headline}")
                            speak(f"{i + 1}. {headline}")
                        if len(news) > 2:
                            speak("You can check the remaining headlines in the console.")
                            for i, headline in enumerate(news[2:]):  # Printing the remaining headlines
                             print(f"{i + 3}. {headline}")

                    # THIS READS ALL THE 10 NEWS
                    # if news:
                    #     speak("Here are the 10 latest news headlines , i can read two of them for you :")
                    #     for i, headline in enumerate(news):
                    #         print(f"{i + 1}. {headline}")
                    # else:
                    #     speak("Sorry, I couldn't fetch the latest news at the moment.")


            elif 'weather' in query.lower() or 'weather report' in query.lower():
                    speak("Please tell me the city name.")
                    city_name = takeCommand()
                    report = getWeatherReport(city_name)
                    textcreate(report)
                    speak(report)

           

            elif 'who is ' in query.lower():
                person = query.split('for')[-1]
                info = wikipedia.summary(person, sentences = 5)
                speak(info)
                textcreate(info)

            

            # elif 'google' in query.lower() or ' search in google' in query.lower() :
            else:
                speak("Searching on Internet...")
                result = searchGoogle(query, num_sentences=3)
                # below code opens and serches in google..***
                # pywhatkit.search(query)
                if result:
                    # speak("Here are the top search results:")
                    textcreate(result)
                    speak(result)
                else:
                    speak("No results found on Google.")


voice_thread = threading.Thread(target=recognize_voice)
voice_thread.daemon = True
voice_thread.start()


# -----------vedio monitroing ---------------
# Initialize the webcam
cap = cv2.VideoCapture(0)


frame_save_path = "frames"

def eyeAspectRatio(eye):
    A = dist.euclidean(eye[1], eye[5])
    B = dist.euclidean(eye[2], eye[4])
    C = dist.euclidean(eye[0], eye[3])
    ear = (A + B) / (2.0 * C)
    return ear

count = 0
earThresh = 0.3  # distance between vertical eye coordinate Threshold
earFrames = 30  # consecutive frames for eye closure
shapePredictor = "shape_predictor_68_face_landmarks.dat"

# Initialize the text-to-speech engine
engine = pyttsx3.init()

cam = cv2.VideoCapture(0)
detector = dlib.get_frontal_face_detector()
predictor = dlib.shape_predictor(shapePredictor)

# get the coord of left & right eye
(lStart, lEnd) = face_utils.FACIAL_LANDMARKS_IDXS["left_eye"]
(rStart, rEnd) = face_utils.FACIAL_LANDMARKS_IDXS["right_eye"]

total_frames = 0
drowsy_frames = 0
drowsiness_detected = False  # Flag to track if drowsiness has been detected

# Initialize a flag to control the loop
running = True

while running:
    _, frame = cam.read()
    frame = imutils.resize(frame, width=450)
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    rects = detector(gray, 0)

    for rect in rects:
        shape = predictor(gray, rect)
        shape = face_utils.shape_to_np(shape)

        leftEye = shape[lStart:lEnd]
        rightEye = shape[rStart:rEnd]
        leftEAR = eyeAspectRatio(leftEye)
        rightEAR = eyeAspectRatio(rightEye)

        ear = (leftEAR + rightEAR) / 2.0

        leftEyeHull = cv2.convexHull(leftEye)
        rightEyeHull = cv2.convexHull(rightEye)
        cv2.drawContours(frame, [leftEyeHull], -1, (0, 0, 255), 1)
        cv2.drawContours(frame, [rightEyeHull], -1, (0, 0, 255), 1)

        if ear < earThresh:
            count += 1

            if count >= earFrames and not drowsiness_detected:
                cv2.putText(frame, "DROWSINESS DETECTED", (10, 30),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
                
                # Speak the drowsiness warning only if it hasn't been detected before
                engine.say("Drowsiness detected")
                engine.runAndWait()  # Wait until the speech is finished
                
                drowsy_frames += 1
                drowsiness_detected = True  # Set the flag to indicate drowsiness has been detected
        else:
            count = 0
            drowsiness_detected = False  # Reset the flag when eyes are open

    total_frames += 1
    accuracy = (1 - drowsy_frames / total_frames) * 100

    cv2.putText(frame, f"Accuracy: {accuracy:.2f}%", (10, 60),
                cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
    
    frame_filename = f"frame_{total_frames:04d}.jpg"
    cv2.imwrite(os.path.join(frame_save_path, frame_filename), frame)

    # Display the frame using OpenCV's imshow function
    cv2.imshow("Frame", frame)

    # Check if user wants to stop the loop
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cam.release()
cv2.destroyAllWindows()






# previous version
# while True:
#     ret, frame = cap.read()
#     if not ret:
#         print("Failed to capture image")
#         break
    
#     cv2.imshow('Webcam Feed', frame)

#     # Break the loop when 'q' is pressed
#     if cv2.waitKey(1) & 0xFF == ord('q'):
#         break

# # Release the webcam and close windows
# cap.release()
# cv2.destroyAllWindows()
