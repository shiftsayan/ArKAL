import face_recognition
import cv2

import time
import requests

from os import listdir

CAM = "0"

# Get a reference to webcam #0 (the default one)
video_capture = cv2.VideoCapture(0)

# Create arrays of known face encodings and their names
known_face_encodings = []
known_face_names = []

# Load all students from /students
for student in listdir("students"):
    # Ignore hidden files
    if student[0] == '.': continue

    # Load a sample picture and learn how to recognize it.
    student_image = face_recognition.load_image_file("students/" + str(student))
    student_face_encoding = face_recognition.face_encodings(student_image)[0]

    known_face_names.append(student[:-4])
    known_face_encodings.append(student_face_encoding)

while True:
    # Grab a single frame of video
    ret, frame = video_capture.read()

    # Convert the image from BGR color (which OpenCV uses) to RGB color (which face_recognition uses)
    rgb_frame = frame[:, :, ::-1]

    # Find all the faces and face enqcodings in the frame of video
    face_locations = face_recognition.face_locations(rgb_frame)
    face_encodings = face_recognition.face_encodings(rgb_frame, face_locations)

    # Loop through each face in this frame of video
    for (top, right, bottom, left), face_encoding in zip(face_locations, face_encodings):
        # See if the face is a match for the known face(s)
        matches = face_recognition.compare_faces(known_face_encodings, face_encoding)

        # If a match was found in known_face_encodings, just use the first one.
        if True in matches:
            first_match_index = matches.index(True)
            name = known_face_names[first_match_index]
            print("Posted " + name)
            requests.post('http://hackcmu.pillai.io:5000/post', data={'name': name, 'code': CAM})
        else:
            print("No match found")

        # Draw a box around the face
        cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)

        # Draw a label with a name below the face
        cv2.rectangle(frame, (left, bottom - 35), (right, bottom), (0, 0, 255), cv2.FILLED)
        font = cv2.FONT_HERSHEY_DUPLEX
        cv2.putText(frame, name + " OUT", (left + 6, bottom - 6), font, 1.0, (255, 255, 255), 1)

    # Display the resulting image
    cv2.imshow('Video', cv2.resize(frame, (0,0), fx=0.75, fy=0.75))

    # time.sleep(0.5)

    # Hit 'q' on the keyboard to quit!
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release handle to the webcam
video_capture.release()
cv2.destroyAllWindows()
