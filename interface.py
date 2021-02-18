import PySimpleGUI as sg
import os
import csv
from PySimpleGUI.PySimpleGUI import Window
import numpy as np
import cv2
from mainpage import loggedin
from helpers import check_login, add_user, save_img

def main():
    layout = [
    [sg.Text("Welcome to Encryptely")], 
    [sg.Button("Login")], 
    [sg.Button("Register")]
    ]
    window = sg.Window("Encryptely", layout)
    while True:
        event, values = window.read()
        if event == "Register":
            break
        elif event == "Login":
            break
        elif event == sg.WIN_CLOSED:
            break

    window.close()
    if event == "Register":
        register()
    elif event == "Login":
        login()

def register():
    layout = [
    [sg.Text("Please enter a username and password to Register. Please make sure your face is visible and in adequate lighting conditions before pressing the Register button.")],
    [sg.Image(filename="", key="-IMAGE-")], 
    [sg.Text("Username"), sg.InputText(key='Username')], 
    [sg.Text("Password"), sg.InputText(key="Password",password_char="*")],
    [sg.Button("Register")]
    ]
    window = sg.Window("Register", layout)
    cap = cv2.VideoCapture(0)
    while True:
        event, values = window.read(timeout=20)
        ret, frame = cap.read()
        imgbytes = cv2.imencode(".png", frame)[1].tobytes()
        window["-IMAGE-"].update(data=imgbytes)
        if event == "Register":
            break
        if event == sg.WIN_CLOSED:
            break

    window.close()
    if event == "Register":
        add_user(values['Username'], values['Password'])
        save_img(frame,values['Password'])
        main()

def login():
    layout = [
    [sg.Text("Please enter your username and password")], 
    [sg.Text("Username"), sg.InputText(key='Username')], 
    [sg.Text("Password"), sg.InputText(key="Password",password_char="*")],
    [sg.Button("Login")]
    ]
    window = sg.Window("Login", layout)
    while True:
        event, values = window.read()
         # End program if user closes window or
        # presses the OK button
        if event == "Login":
            if check_login(values['Username'],values['Password']):
                break
        if event == sg.WIN_CLOSED:
            break
    
    window.close()
    if check_login(values["Username"],values["Password"]):
        loggedin(values["Username"], values["Password"])

if __name__ == '__main__':
    main()



