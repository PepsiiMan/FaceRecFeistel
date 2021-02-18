import os
import csv
import cv2
import face_recognition


def check_login(user, password):
    if user == '' or password == '':
        return False
    flag = False
    with open(os.path.join('users.csv')) as file:
        reader = csv.reader(file, delimiter=',')
        for row in reader:
            i = 0
            for column in row:
                if i == 0:
                    if column==user:
                        i+=1
                if i == 1:
                    if column==password:
                        flag = True
        if flag:
            return True
        else:
            return False

def add_user(username,password):
    if username == '' or password == '':
        return os.error
    row = [username,password]
    with open(os.path.join('users.csv'), 'a+', newline='') as write_obj:
        writer = csv.writer(write_obj)
        writer.writerow(row)

def known_faces():
    known_face_encodings = []
    known_face_names = []
    for file in os.listdir(os.fsencode('Pictures')):
        filename = os.fsdecode(file)
        name = filename.split('.')[0]
        filename = os.path.join('Pictures', filename)
        image = face_recognition.load_image_file(filename)
        encoding = face_recognition.face_encodings(image)[0]
        known_face_encodings.append(encoding)
        known_face_names.append(name)
    return known_face_encodings, known_face_names

def save_img(image, username):
    cv2.imwrite((os.path.join('Pictures', username)+'.jpg'), image)
