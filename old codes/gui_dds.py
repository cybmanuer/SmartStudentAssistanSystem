# import streamlit as st
# from scipy.spatial import distance as dist
# import imutils
# import dlib
# import cv2
# import pyttsx3
# from imutils import face_utils

# # Set up Streamlit page configuration
# st.set_page_config(page_title="Drowsiness Detection System", layout="wide")

# # Initialize text-to-speech engine
# engine = pyttsx3.init()

# # Load the face landmark predictor
# shapePredictor = "shape_predictor_68_face_landmarks.dat"

# # Eye aspect ratio (EAR) calculation
# def eyeAspectRatio(eye):
#     A = dist.euclidean(eye[1], eye[5])
#     B = dist.euclidean(eye[2], eye[4])
#     C = dist.euclidean(eye[0], eye[3])
#     ear = (A + B) / (2.0 * C)
#     return ear

# # Initialize webcam and face detector
# cam = cv2.VideoCapture(0)
# detector = dlib.get_frontal_face_detector()
# predictor = dlib.shape_predictor(shapePredictor)

# # Get the coordinates of left & right eye
# (lStart, lEnd) = face_utils.FACIAL_LANDMARKS_IDXS["left_eye"]
# (rStart, rEnd) = face_utils.FACIAL_LANDMARKS_IDXS["right_eye"]

# # Streamlit UI elements
# st.title("Drowsiness Detection System")
# image_placeholder = st.empty()
# alert_placeholder = st.empty()

# # Initialize variables
# count = 0
# earThresh = 0.3
# earFrames = 80
# total_frames = 0
# drowsy_frames = 0
# drowsiness_detected = False
# face_detected = False
# no_face_counter = 0
# no_face_threshold = 280
# sitting_time = 0
# break_threshold = 900
# break_prompted = False

# # Create a unique stop button
# stop_button = st.button("Stop", key="stop_button_unique")

# # Start capturing frames
# running = True
# while running:
#     # Read the frame from the camera
#     ret, frame = cam.read()
    
#     # Check if frame is captured successfully
#     if frame is None or not ret:
#         st.error("Failed to capture image from the camera. Please check the camera.")
#         break  # Exit the loop if frame capture fails

#     frame = imutils.resize(frame, width=640)  # Adjusted width for a medium-sized video
#     gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
#     rects = detector(gray, 0)

#     # Check for faces
#     if len(rects) > 0:
#         face_detected = True
#         no_face_counter = 0
#         sitting_time += 1

#         # Check if sitting time exceeds break threshold
#         if sitting_time >= break_threshold and not break_prompted:
#             engine.say("You've been studying for a while. It's time to take a break!")
#             engine.runAndWait()
#             break_prompted = True
#     else:
#         face_detected = False
#         no_face_counter += 1
#         sitting_time = 0

#         if break_prompted:
#             break_prompted = False

#     # Check if no face has been detected for more than 3 minutes
#     if no_face_counter >= no_face_threshold:
#         if not drowsiness_detected:
#             engine.say("ARE YOU THERE? I can't find you.")
#             engine.runAndWait()
#             no_face_counter = 0

#     for rect in rects:
#         shape = predictor(gray, rect)
#         shape = face_utils.shape_to_np(shape)

#         leftEye = shape[lStart:lEnd]
#         rightEye = shape[rStart:rEnd]
#         leftEAR = eyeAspectRatio(leftEye)
#         rightEAR = eyeAspectRatio(rightEye)

#         ear = (leftEAR + rightEAR) / 2.0

#         if ear < earThresh:
#             count += 1

#             if count >= earFrames and not drowsiness_detected:
#                 cv2.putText(frame, "DROWSINESS DETECTED", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
#                 engine.say("Please awake. Don't sleep.")
#                 engine.runAndWait()
#                 drowsy_frames += 1
#                 drowsiness_detected = True
#         else:
#             count = 0
#             drowsiness_detected = False

#     total_frames += 1
#     accuracy = (1 - drowsy_frames / total_frames) * 100

#     cv2.putText(frame, f"Accuracy: {accuracy:.2f}%", (10, 60), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)

#     # Update the Streamlit UI
#     image_placeholder.image(frame, channels="BGR", use_column_width=True)
#     alert_text = "DROWSINESS DETECTED" if drowsiness_detected else "All Good!"
#     alert_placeholder.text(alert_text)

#     # Check if the stop button was pressed
#     if stop_button:
#         running = False

# # Clean up
# cam.release()
# cv2.destroyAllWindows()






# -----------v2------------------

# import streamlit as st
# from scipy.spatial import distance as dist
# import imutils
# import dlib
# import cv2
# import pyttsx3
# from imutils import face_utils

# # Set up Streamlit page configuration
# st.set_page_config(page_title="Drowsiness Detection System", layout="wide")

# # Initialize text-to-speech engine
# engine = pyttsx3.init()

# # Load the face landmark predictor
# shapePredictor = "shape_predictor_68_face_landmarks.dat"

# # Eye aspect ratio (EAR) calculation
# def eyeAspectRatio(eye):
#     A = dist.euclidean(eye[1], eye[5])
#     B = dist.euclidean(eye[2], eye[4])
#     C = dist.euclidean(eye[0], eye[3])
#     return (A + B) / (2.0 * C)

# # Function to initialize webcam with error handling
# def initialize_camera():
#     cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)  # Try DSHOW backend first
#     if not cap.isOpened():
#         st.error("Failed to open the camera with DSHOW. Trying MSMF...")
#         cap.release()
#         cap = cv2.VideoCapture(0, cv2.CAP_MSMF)  # Try MSMF if DSHOW fails
        
#         if not cap.isOpened():
#             st.error("Failed to open the camera with both DSHOW and MSMF.")
#             return None
#     return cap

# # Initialize webcam and face detector
# cam = initialize_camera()
# if cam is None:
#     st.stop()  # Stop execution if camera initialization failed

# detector = dlib.get_frontal_face_detector()
# predictor = dlib.shape_predictor(shapePredictor)

# # Get the coordinates of left & right eye
# (lStart, lEnd) = face_utils.FACIAL_LANDMARKS_IDXS["left_eye"]
# (rStart, rEnd) = face_utils.FACIAL_LANDMARKS_IDXS["right_eye"]

# # Streamlit UI elements
# st.title("Drowsiness Detection System")
# image_placeholder = st.empty()
# alert_placeholder = st.empty()

# # Initialize variables
# count = 0
# earThresh = 0.3
# earFrames = 80
# total_frames = 0
# drowsy_frames = 0
# drowsiness_detected = False

# # Create a unique stop button
# stop_button = st.button("Stop", key="stop_button_unique")

# # Start capturing frames
# running = True
# while running:
#     try:
#         # Read the frame from the camera
#         ret, frame = cam.read()
        
#         # Check if frame is captured successfully
#         if not ret or frame is None:
#             st.error("Failed to capture image from the camera. Please check the camera.")
#             break  # Exit the loop if frame capture fails

#         frame = imutils.resize(frame, width=640)
#         gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
#         rects = detector(gray, 0)

#         if len(rects) > 0:
#             for rect in rects:
#                 shape = predictor(gray, rect)
#                 shape_np = face_utils.shape_to_np(shape)

#                 leftEye = shape_np[lStart:lEnd]
#                 rightEye = shape_np[rStart:rEnd]
#                 leftEAR = eyeAspectRatio(leftEye)
#                 rightEAR = eyeAspectRatio(rightEye)

#                 ear = (leftEAR + rightEAR) / 2.0

#                 if ear < earThresh:
#                     count += 1

#                     if count >= earFrames and not drowsiness_detected:
#                         cv2.putText(frame, "DROWSINESS DETECTED", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
#                         engine.say("Please awake. Don't sleep.")
#                         engine.runAndWait()
#                         drowsy_frames += 1
#                         drowsiness_detected = True
#                 else:
#                     count = 0
#                     drowsiness_detected = False

#         total_frames += 1
#         accuracy = (1 - drowsy_frames / total_frames) * 100

#         # cv2.putText(frame, f"Accuracy: {accuracy:.2f}%", (10, 60), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)

#         # Update the Streamlit UI with specified width for the image frame.
#         image_placeholder.image(frame, channels="BGR", width=540)
        
#         alert_text = "DROWSINESS DETECTED" if drowsiness_detected else "All Good!"
#         alert_placeholder.text(alert_text)

#         # Check if the stop button was pressed
#         if stop_button:
#             running = False

#     except Exception as e:
#         st.error(f"An unexpected error occurred: {str(e)}")
#         break

# # Clean up resources after stopping the loop.
# cam.release()
# cv2.destroyAllWindows()

# //////////  v3 //////// with timer and date

import streamlit as st
from scipy.spatial import distance as dist
import imutils
import dlib
import cv2
import pyttsx3
from imutils import face_utils
from datetime import datetime, timedelta
# st.set_page_config(page_title="Drowsiness Detection System", layout="wide")
st.header(" Student Monitroing System")

# Set up Streamlit page configuration
time = datetime.now().strftime("%H:%M:%S")
date = datetime.now().strftime("%Y-%m-%d")  
st.markdown(f"<div class='timedate'>Current Time: {time} <span> | </span> Current Date:  {date}</div>", unsafe_allow_html=True)



# Initialize text-to-speech engine
engine = pyttsx3.init()

# Load the face landmark predictor
shapePredictor = "shape_predictor_68_face_landmarks.dat"

# Eye aspect ratio (EAR) calculation
def eyeAspectRatio(eye):
    A = dist.euclidean(eye[1], eye[5])
    B = dist.euclidean(eye[2], eye[4])
    C = dist.euclidean(eye[0], eye[3])
    return (A + B) / (2.0 * C)

# Function to initialize webcam with error handling
def initialize_camera():
    cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)  # Try DSHOW backend first
    if not cap.isOpened():
        st.error("Failed to open the camera with DSHOW. Trying MSMF...")
        cap.release()
        cap = cv2.VideoCapture(0, cv2.CAP_MSMF)  # Try MSMF if DSHOW fails
        
        if not cap.isOpened():
            st.error("Failed to open the camera with both DSHOW and MSMF.")
            return None
    return cap

# Initialize webcam and face detector
cam = initialize_camera()
if cam is None:
    st.stop()  # Stop execution if camera initialization failed

detector = dlib.get_frontal_face_detector()
predictor = dlib.shape_predictor(shapePredictor)

# Get the coordinates of left & right eye
(lStart, lEnd) = face_utils.FACIAL_LANDMARKS_IDXS["left_eye"]
(rStart, rEnd) = face_utils.FACIAL_LANDMARKS_IDXS["right_eye"]

# Streamlit UI elements
# st.title("Drowsiness Detection System")
image_placeholder = st.empty()
alert_placeholder = st.empty()

# Initialize variables
count = 0
earThresh = 0.3
earFrames = 80
total_frames = 0
drowsy_frames = 0
drowsiness_detected = False

# Timer variables
start_time = datetime.now()

# Placeholders for current time, date, and elapsed time display
time_placeholder = st.empty()
date_placeholder = st.empty()
elapsed_time_placeholder = st.empty()

# Session state to control running state of the loop
if 'running' not in st.session_state:
    st.session_state.running = True

# Stop button outside of the loop
if st.button("Stop"):
    st.session_state.running = False

# Start capturing frames
while st.session_state.running:
    try:
        # Read the frame from the camera
        ret, frame = cam.read()
        
        # Check if frame is captured successfully
        if not ret or frame is None:
            st.error("Failed to capture image from the camera. Please check the camera.")
            break  # Exit the loop if frame capture fails

        frame = imutils.resize(frame, width=640)
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        rects = detector(gray, 0)

        if len(rects) > 0:
            for rect in rects:
                shape = predictor(gray, rect)
                shape_np = face_utils.shape_to_np(shape)

                leftEye = shape_np[lStart:lEnd]
                rightEye = shape_np[rStart:rEnd]
                leftEAR = eyeAspectRatio(leftEye)
                rightEAR = eyeAspectRatio(rightEye)

                ear = (leftEAR + rightEAR) / 2.0

                if ear < earThresh:
                    count += 1

                    if count >= earFrames and not drowsiness_detected:
                        cv2.putText(frame, "DROWSINESS DETECTED", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
                        engine.say("Please awake. Don't sleep.")        
                        engine.runAndWait()
                        drowsy_frames += 1
                        drowsiness_detected = True
                else:
                    count = 0
                    drowsiness_detected = False

        total_frames += 1
        
        # Calculate elapsed time for timer display.
        elapsed_time_str = str(timedelta(seconds=(datetime.now() - start_time).seconds))
        
        # Update the Streamlit UI with specified width for the image frame.
        # image_placeholder.image(frame, channels="BGR", width=640)

        # Display the frame in the styled container
        image_placeholder.image(frame, channels="BGR", width=540)

     
           


        alert_text = "DROWSINESS DETECTED" if drowsiness_detected else "All Good!"
        alert_placeholder.text(alert_text)

       
        # Update elapsed time display.
        elapsed_time_placeholder.markdown(f"**Elapsed Time:** {elapsed_time_str}")

        # choice = st.selectbox("Choose an option", ["Option 1", "Option 2", "Option 3"])
        # st.write("You selected:", choice)

    except Exception as e:
        st.error(f"An unexpected error occurred: {str(e)}")
        break

# Clean up resources after stopping the loop.
cam.release()
cv2.destroyAllWindows()

time_placeholder.markdown("""
    <style>
    
    .timedate{
        margin-left: 10%;  
        # color:red;   
        font-size:20px;             
    }
    .timedate span{
        padding:30px;
        color: red;
        margin-right:10px;                                                        
    }

                          
  
    </style>
    """, unsafe_allow_html=True)


its gui based face recognition system