import cv2
import sys
import json
import time
import numpy as np
from keras.models import model_from_json
import matplotlib.pyplot as plt
import matplotlib.image as mpimg

def predict_emotion(face_image_gray, model): # a single cropped face
    resized_img = cv2.resize(face_image_gray, (48,48), interpolation = cv2.INTER_AREA)
    # cv2.imwrite(str(index)+'.png', resized_img)
    image = resized_img.reshape(1, 1, 48, 48)
    list_of_list = model.predict(image, batch_size=1, verbose=1)
    angry, fear, happy, sad, surprise, neutral = [prob for lst in list_of_list for prob in lst]
    return [angry, fear, happy, sad, surprise, neutral]

def still_image(path):
    emotion_labels = ['angry', 'fear', 'happy', 'sad', 'surprise', 'neutral']
    cascPath = 'haarcascade_frontalface_default.xml'

    faceCascade = cv2.CascadeClassifier(cascPath)

    # load json and create model arch
    json_file = open('model.json','r')
    loaded_model_json = json_file.read()
    json_file.close()
    model = model_from_json(loaded_model_json)

    # load weights into new model
    model.load_weights('model.h5')
    # Capture frame-by-frame
    frame = cv2.imread(path)
    cv2.imshow('Image1',frame)
    img_gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY,1)


    faces = faceCascade.detectMultiScale(
        img_gray,
        scaleFactor=1.1,
        minNeighbors=5,
        minSize=(30, 30),
        flags=cv2.cv.CV_HAAR_SCALE_IMAGE
    )

    emotions = []
    # Draw a rectangle around the faces
    for (x, y, w, h) in faces:
        # fig, ax = plt.subplots()
        face_image_gray = img_gray[y:y+h, x:x+w]

        cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
        plt.imshow(frame)
        plt.show()

        angry, fear, happy, sad, surprise, neutral = predict_emotion(face_image_gray, model)
        with open('emotion.txt', 'a') as f:
            f.write('{},{},{},{},{},{},{}\n'.format(time.time(), angry, fear, happy, sad, surprise, neutral))
        # ('{},{},{},{},{},{},{}\n'.format(time.time(), angry, fear, happy, sad, surprise, neutral))
        s = 'angry {}, fear {}, happy {}, sad {}, surprise {}, neutral {}\n'.format(angry, fear, happy, sad, surprise, neutral)
        a = plt.bar(emotion_labels, [angry, fear, happy, sad, surprise, neutral],align = 'center',color = ['r','#800080','y','b','#ffa500','#9acd32'])
        plt.show()

    # Display the resulting frame

    cv2.imshow('Image', frame)

if __name__ == '__main__':
    still_image('sample.jpg')