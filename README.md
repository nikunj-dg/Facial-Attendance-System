# Face Recognition System 

A desktop-based Facial Recognition System built using Python, OpenCV, Tkinter, and face_recognition, which can be used as an attendance system.

This application allows users to:

- Register using facial recognition
- Login using webcam face detection
- Logout with face verification
- Automatically log attendance records with timestamps

## Features

- Live webcam feed
- Face recognition using deep learning embeddings
- Register new users with face encoding storage
- Login / Logout system
- Local database using .pickle files
- Automatic attendance logging (log.txt)
- Tkinter-based GUI interface

## Tech Stack

Python 3.8+

Tkinter – GUI

OpenCV (cv2) – Webcam handling

face_recognition – Face encoding & matching

Pillow (PIL) – Image processing

Pickle – Local face embeddings storage 

## Usage 

- Install dependencies
    - pip install opencv-python
    - pip install pillow
    - pip install face_recognition
- Run the app
    - py

 ## Limitations

- Single-face detection only
- Local file storage only
- Requires good lighting for accuracy

## Future Improvements 

- Cloud data storage
- Implement the attendance system
- Generate attendance report 



