from zipfile import ZipFile
from PIL import Image
import PIL
import pytesseract #cannot download or use in this PC
import cv2 as cv
import numpy as np


def open_zip_image(file):
    '''Provided a zip file, it returns a list of each image file as PIL object'''
    with ZipFile(file) as picfaces:
        listpics = picfaces.infolist()
        openpics = []
        for pic in listpics:
            extract_pic = picfaces.extract(pic)
            image = Image.open(extract_pic)
            openpics.append(image)
        return openpics

def make_sheet_display(cropped_list):
    '''Provided the list of cropped thumbnails 100x100 returns and displays them on the 5x2 contact sheet'''
    first_image = cropped_list[0]
    if len(cropped_list) <= 5:
        contact_sheet = PIL.Image.new(first_image.mode, (100*5, 100))
    elif len(cropped_list) > 5:
        contact_sheet = PIL.Image.new(first_image.mode, (100*5, 100*2))
    x = 0
    y = 0
    for face in cropped_list:
        contact_sheet.paste(face, (x, y))
        if x + 100 == contact_sheet.width:
            x = 0
            y = y + 100
        else:
            x = x + 100
    display(contact_sheet)


word = input('What word do you want to get faces for? ')
face_cascade = cv.CascadeClassifier('readonly/haarcascade_frontalface_default.xml') # loading the face detection classifier

for image in open_zip_image('readonly/images.zip'):
    name = image.filename

    l_image = image.convert('L')
    text = pytesseract.image_to_string(l_image)

    if word in text:
        print('\nResults found in file ' + name)

        cv_image = cv.imread(name)
        gray = cv.cvtColor(cv_image, cv.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray, scaleFactor = 1.35, minNeighbors = 7)
        try:
            faces_list = faces.tolist()
            cropped_list = []
            for face in faces_list:
                crop_face = image.crop((face[0], face[1], face[0]+face[2], face[1]+face[3]))
                crop_face.thumbnail((100,100))
                cropped_list.append(crop_face)
            make_sheet_display(cropped_list)
        except:
            print('But there were no faces in that file')
