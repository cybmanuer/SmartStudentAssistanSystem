
from scipy.spatial import distance as dist
from imutils import face_utils
import imutils
import dlib
import cv2
import os
import matplotlib.pyplot as plt
import keyboard
import pyttsx3  # Import the text-to-speech library

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


# from scipy.spatial import distance as dist
# from imutils import face_utils
# import imutils
# import dlib
# import cv2
# import os
# import matplotlib.pyplot as plt
# import keyboard
# import pyttsx3  # Import the text-to-speech library
# import time  # Import time for tracking duration

# frame_save_path = "frames"

# def eyeAspectRatio(eye):
#     A = dist.euclidean(eye[1], eye[5])
#     B = dist.euclidean(eye[2], eye[4])
#     C = dist.euclidean(eye[0], eye[3])
#     ear = (A + B) / (2.0 * C)
#     return ear

# count = 0
# earThresh = 0.3  # distance between vertical eye coordinate Threshold
# earFrames = 80  # consecutive frames for eye closure
# shapePredictor = "shape_predictor_68_face_landmarks.dat"

# # Initialize the text-to-speech engine
# engine = pyttsx3.init()

# cam = cv2.VideoCapture(0)
# detector = dlib.get_frontal_face_detector()
# predictor = dlib.shape_predictor(shapePredictor)

# # get the coord of left & right eye
# (lStart, lEnd) = face_utils.FACIAL_LANDMARKS_IDXS["left_eye"]
# (rStart, rEnd) = face_utils.FACIAL_LANDMARKS_IDXS["right_eye"]

# total_frames = 0
# drowsy_frames = 0
# drowsiness_detected = False  # Flag to track if drowsiness has been detected

# # Initialize variables to track face detection
# face_detected = False
# no_face_counter = 0
# no_face_threshold = 180  # 3 minutes in seconds

# # Initialize a flag to control the loop
# running = True

# while running:
#     _, frame = cam.read()
#     frame = imutils.resize(frame, width=450)
#     gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

#     rects = detector(gray, 0)

#     if len(rects) > 0:
#         face_detected = True  # Face detected
#         no_face_counter = 0  # Reset counter
#     else:
#         face_detected = False  # No face detected
#         no_face_counter += 1  # Increment counter

#     # Check if no face has been detected for more than 3 minutes
#     if no_face_counter >= no_face_threshold:
#         # Speak "ARE YOU THERE" only once
#         if not drowsiness_detected:  # Ensure it only speaks once
#             engine.say("  ARE YOU THERE. I cant found You ")
#             engine.runAndWait()
#             no_face_counter = 0  # Reset the counter after speaking

#     for rect in rects:
#         shape = predictor(gray, rect)
#         shape = face_utils.shape_to_np(shape)

#         leftEye = shape[lStart:lEnd]
#         rightEye = shape[rStart:rEnd]
#         leftEAR = eyeAspectRatio(leftEye)
#         rightEAR = eyeAspectRatio(rightEye)

#         ear = (leftEAR + rightEAR) / 2.0

#         leftEyeHull = cv2.convexHull(leftEye)
#         rightEyeHull = cv2.convexHull(rightEye)
#         cv2.drawContours(frame, [leftEyeHull], -1, (0, 0, 255), 1)
#         cv2.drawContours(frame, [rightEyeHull], -1, (0, 0, 255), 1)

#         if ear < earThresh:
#             count += 1

#             if count >= earFrames and not drowsiness_detected:
#                 cv2.putText(frame, "DROWSINESS DETECTED", (10, 30),
#                             cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
                
#                 # Speak the drowsiness warning only if it hasn't been detected before
#                 engine.say("Please awake. Dont Sleep.")
#                 engine.runAndWait()  # Wait until the speech is finished
                
#                 drowsy_frames += 1
#                 drowsiness_detected = True  # Set the flag to indicate drowsiness has been detected
#         else:
#             count = 0
#             drowsiness_detected = False  # Reset the flag when eyes are open

#     total_frames += 1
#     accuracy = (1 - drowsy_frames / total_frames) * 100

#     cv2.putText(frame, f"Accuracy: {accuracy:.2f}%", (10, 60),
#                 cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
    
#     frame_filename = f"frame_{total_frames:04d}.jpg"
#     cv2.imwrite(os.path.join(frame_save_path, frame_filename), frame)

#     # Display the frame using OpenCV's imshow function
#     cv2.imshow("Frame", frame)

#     # Check if user wants to stop the loop
#     if cv2.waitKey(1) & 0xFF == ord('q'):
#         break

# cam.release()
# cv2.destroyAllWindows()


# from scipy.spatial import distance as dist
# from imutils import face_utils
# import imutils
# import dlib
# import cv2
# import os
# import pyttsx3  # Import the text-to-speech library

# frame_save_path = "frames"

# def eyeAspectRatio(eye):
#     A = dist.euclidean(eye[1], eye[5])
#     B = dist.euclidean(eye[2], eye[4])
#     C = dist.euclidean(eye[0], eye[3])
#     ear = (A + B) / (2.0 * C)
#     return ear

# count = 0
# earThresh = 0.3  # Threshold for eye aspect ratio
# earFrames = 80  # Number of frames for 4 seconds (30 FPS * 4 seconds)
# shapePredictor = "shape_predictor_68_face_landmarks.dat"

# # Initialize the text-to-speech engine
# engine = pyttsx3.init()

# cam = cv2.VideoCapture(0)
# detector = dlib.get_frontal_face_detector()
# predictor = dlib.shape_predictor(shapePredictor)

# # Get the coordinates of left & right eye
# (lStart, lEnd) = face_utils.FACIAL_LANDMARKS_IDXS["left_eye"]
# (rStart, rEnd) = face_utils.FACIAL_LANDMARKS_IDXS["right_eye"]

# total_frames = 0
# drowsy_frames = 0
# drowsiness_detected = False  # Flag to track if drowsiness has been detected

# # Initialize variables to track face detection
# face_detected = False
# no_face_counter = 0
# no_face_threshold = 280  # 3 minutes in seconds

# # Initialize variables for study breaks
# sitting_time = 0  # Time spent sitting in seconds
# break_threshold = 900  # 15 minutes in seconds
# break_prompted = False  # Flag to track if break has been prompted

# # Initialize a flag to control the loop
# running = True

# while running:
#     _, frame = cam.read()
#     frame = imutils.resize(frame, width=450)
#     gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

#     rects = detector(gray, 0)

#     if len(rects) > 0:
#         face_detected = True  # Face detected
#         no_face_counter = 0  # Reset counter

#         # Increment sitting time since the face is detected
#         sitting_time += 1  # Increment by 1 frame (~33ms)

#         # Check if sitting time exceeds break threshold
#         if sitting_time >= break_threshold and not break_prompted:
#             engine.say("You've been studying for a while. It's time to take a break!")
#             engine.runAndWait()
#             break_prompted = True  # Set the flag to indicate break has been prompted
#     else:
#         face_detected = False  # No face detected
#         no_face_counter += 1  # Increment counter
#         sitting_time = 0  # Reset sitting time if no face is detected

#         # Reset break prompt flag if no face is detected
#         if break_prompted:
#             break_prompted = False

#     # Check if no face has been detected for more than 3 minutes
#     if no_face_counter >= no_face_threshold:
#         # Speak "ARE YOU THERE" only once
#         if not drowsiness_detected:  # Ensure it only speaks once
#             engine.say("ARE YOU THERE? I can't find you.")
#             engine.runAndWait()
#             no_face_counter = 0  # Reset the counter after speaking

#     for rect in rects:
#         shape = predictor(gray, rect)
#         shape = face_utils.shape_to_np(shape)

#         leftEye = shape[lStart:lEnd]
#         rightEye = shape[rStart:rEnd]
#         leftEAR = eyeAspectRatio(leftEye)
#         rightEAR = eyeAspectRatio(rightEye)

#         ear = (leftEAR + rightEAR) / 2.0

#         leftEyeHull = cv2.convexHull(leftEye)
#         rightEyeHull = cv2.convexHull(rightEye)
#         cv2.drawContours(frame, [leftEyeHull], -1, (0, 0, 255), 1)
#         cv2.drawContours(frame, [rightEyeHull], -1, (0, 0, 255), 1)

#         if ear < earThresh:
#             count += 1

#             if count >= earFrames and not drowsiness_detected:
#                 cv2.putText(frame, "DROWSINESS DETECTED", (10, 30),
#                             cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)

#                 # Speak the drowsiness warning only if it hasn't been detected before
#                 engine.say("Please awake. Don't sleep.")
#                 engine.runAndWait()  # Wait until the speech is finished

#                 drowsy_frames += 1
#                 drowsiness_detected = True  # Set the flag to indicate drowsiness has been detected
#         else:
#             count = 0
#             drowsiness_detected = False  # Reset the flag when eyes are open

#     total_frames += 1
#     accuracy = (1 - drowsy_frames / total_frames) * 100

#     cv2.putText(frame, f"Accuracy: {accuracy:.2f}%", (10, 60),
#                 cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)

#     frame_filename = f"frame_{total_frames:04d}.jpg"
#     cv2.imwrite(os.path.join(frame_save_path, frame_filename), frame)

#     # Display the frame using OpenCV's imshow function
#     cv2.imshow("Frame", frame)

#     # Check if user wants to stop the loop
#     if cv2.waitKey(1) & 0xFF == ord('q'):
#         break

# cam.release()
# cv2.destroyAllWindows()






import streamlit as st
import mediapipe as mp
import cv2
import numpy as np
from scipy.spatial import distance as dist
from datetime import datetime, timedelta
import pyttsx3

# Initialize Streamlit page
st.set_page_config(page_title="Drowsiness Detection System", layout="wide")

# Initialize Mediapipe modules
mp_face_detection = mp.solutions.face_detection
mp_face_mesh = mp.solutions.face_mesh
face_mesh = mp_face_mesh.FaceMesh(refine_landmarks=True)

# Initialize text-to-speech
engine = pyttsx3.init()

# Eye aspect ratio (EAR) calculation
def eye_aspect_ratio(eye_landmarks):
    A = dist.euclidean(eye_landmarks[1], eye_landmarks[5])
    B = dist.euclidean(eye_landmarks[2], eye_landmarks[4])
    C = dist.euclidean(eye_landmarks[0], eye_landmarks[3])
    return (A + B) / (2.0 * C)

# Function to initialize the webcam
def initialize_camera():
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        st.error("Failed to open the camera.")
        return None
    return cap

# Start Streamlit
st.title("Drowsiness Detection System")
image_placeholder = st.empty()
alert_placeholder = st.empty()

# Variables for drowsiness detection
EAR_THRESHOLD = 0.25
CONSEC_FRAMES = 20
frame_count = 0
drowsiness_detected = False

# Timer variables
start_time = datetime.now()
sitting_time = 0
break_threshold = 900  # 15 minutes
no_face_counter = 0
no_face_threshold = 180

# Streamlit placeholders for time
time_placeholder = st.empty()
date_placeholder = st.empty()
elapsed_time_placeholder = st.empty()

# Initialize the webcam
cap = initialize_camera()
if not cap:
    st.stop()

# Stop button
if 'running' not in st.session_state:
    st.session_state.running = True

if st.button("Stop"):
    st.session_state.running = False

# Process frames
while st.session_state.running:
    ret, frame = cap.read()
    if not ret or frame is None:
        st.error("Failed to capture frame from camera. Please check the device.")
        break

    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = face_mesh.process(frame_rgb)

    drowsiness_detected = False
    if results.multi_face_landmarks:
        no_face_counter = 0
        sitting_time += 1
        for face_landmarks in results.multi_face_landmarks:
            # Extract eye landmarks
            left_eye = [np.array([face_landmarks.landmark[i].x, face_landmarks.landmark[i].y]) for i in [362, 385, 387, 263, 373, 380]]
            right_eye = [np.array([face_landmarks.landmark[i].x, face_landmarks.landmark[i].y]) for i in [33, 160, 158, 133, 153, 144]]

            # Convert to pixel coordinates
            h, w, _ = frame.shape
            left_eye = np.array([(int(p[0] * w), int(p[1] * h)) for p in left_eye])
            right_eye = np.array([(int(p[0] * w), int(p[1] * h)) for p in right_eye])

            # Calculate EAR for both eyes
            left_ear = eye_aspect_ratio(left_eye)
            right_ear = eye_aspect_ratio(right_eye)
            ear = (left_ear + right_ear) / 2.0

            # Draw eye landmarks
            for (x, y) in np.vstack([left_eye, right_eye]):
                cv2.circle(frame, (x, y), 2, (0, 255, 0), -1)

            # Check for drowsiness
            if ear < EAR_THRESHOLD:
                frame_count += 1
                if frame_count >= CONSEC_FRAMES:
                    cv2.putText(frame, "DROWSINESS DETECTED", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
                    engine.say("Please wake up. Don't sleep!")
                    engine.runAndWait()
                    drowsiness_detected = True
            else:
                frame_count = 0

    else:
        no_face_counter += 1
        if no_face_counter >= no_face_threshold:
            engine.say("Are you there? I can't find you!")
            engine.runAndWait()
            no_face_counter = 0

    # Calculate elapsed time
    elapsed_time = str(timedelta(seconds=(datetime.now() - start_time).seconds))
    image_placeholder.image(frame, channels="BGR", width=640)

    # Update Streamlit UI
    alert_text = "DROWSINESS DETECTED" if drowsiness_detected else "All Good!"
    alert_placeholder.text(alert_text)
    current_time_str = datetime.now().strftime("%H:%M:%S")
    current_date_str = datetime.now().strftime("%Y-%m-%d")
    time_placeholder.markdown(f"*Current Time:* {current_time_str}")
    date_placeholder.markdown(f"*Current Date:* {current_date_str}")
    elapsed_time_placeholder.markdown(f"*Elapsed Time:* {elapsed_time}")

cap.release()
cv2.destroyAllWindows()
