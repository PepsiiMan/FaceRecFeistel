from tkinter import Event
import PySimpleGUI as sg
import cv2
import numpy as np
import face_recognition
import base64
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.fernet import Fernet, InvalidToken
from numpy.core.fromnumeric import ptp
from helpers import known_faces
from encryptely import get_key, encrypt, decrypt

def loggedin(username,password):
    known_face_encodings, known_face_names = known_faces()

    layout = [
        [sg.Text("Welcome "+username+"!", size=(60, 1), justification="center")],
        [sg.Image(filename="", key="-IMAGE-")],
        [sg.Text("Enter the name of the file you wish to encrypt:"), sg.InputText()], 
        [sg.Button("Encrypt")],
        [sg.Text("Enter the name of the file you wish to decrypt:"), sg.InputText()], 
        [sg.Button("Decrypt")],
        [sg.Button("Exit", size=(10, 1))]
        ]
    window = sg.Window("Encreptely", layout)
    cap = cv2.VideoCapture(0)
    while True:
        event, values = window.read(timeout=20)

        ret, frame = cap.read()
        imgbytes = cv2.imencode(".png", frame)[1].tobytes()
        window["-IMAGE-"].update(data=imgbytes)

        rgb_frame = frame[:, :, ::-1]
        face_locations = face_recognition.face_locations(rgb_frame)
        face_encodings = face_recognition.face_encodings(rgb_frame, face_locations)
        for (top, right, bottom, left), face_encoding in zip(face_locations, face_encodings):
            matches = face_recognition.compare_faces(known_face_encodings, face_encoding)

            name = "Unknown"
            face_distances = face_recognition.face_distance(known_face_encodings, face_encoding)
            best_match_index = np.argmin(face_distances)
            if matches[best_match_index]:
                name = known_face_names[best_match_index]
        if event == "Exit" or event == sg.WIN_CLOSED:
            break
        if event == "Encrypt" and name == username:
            key = get_key(password)
            encrypt(values[0], key)
            success("Successfully encrypted: ", values[0])
        if event == "Decrypt" and name == username:
            key = get_key(password)
            decrypt(values[1], key)
            success("Successfully decrypted: ", values[1])


    window.close()


def success(msg, file):
    layout = [[sg.Text(msg + file)]]
    window = sg.Window("Success!", layout)
    while True:
        event, values = window.read()
        if event == sg.WIN_CLOSED:
            break
    
    window.close()