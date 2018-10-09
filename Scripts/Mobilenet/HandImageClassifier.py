import cv2
import keras
import os
import time
import numpy as np

from keras.utils.generic_utils import CustomObjectScope
from keras.models import load_model
from keras.applications.mobilenet import preprocess_input

keras_dict = {
    'relu6': keras.applications.mobilenet.relu6,
    'DepthwiseConv2D': keras.applications.mobilenet.DepthwiseConv2D
}

with CustomObjectScope(keras_dict):
    model = load_model('TrainedModels/Hand-mobilenet-v2.model')

IMG_SIZE = 224
CATEGORIES = ['C', 'O']


def get_label(img):
    # img = cv2.flip(img,1)
    img = cv2.resize(img, (IMG_SIZE, IMG_SIZE))
    img = img[..., ::-1]
    img = img.astype('float32')
    img = np.expand_dims(img, axis=0)
    img = preprocess_input(img)
    prediction = model.predict(img)
    return prediction[0], str(np.argmax(prediction[0]))


def main():
    cap = cv2.VideoCapture(0)

    while True:
        _, frame = cap.read()
        cv2.rectangle(frame, (20, 20), (320, 320), (255, 0, 0), 2)

        tic = time.time()
        predictions, label = get_label(frame[20:320, 20:320])
        toc = time.time()

        cv2.putText(frame, label, (20, 390), cv2.FONT_HERSHEY_COMPLEX,
                    3.0, (0, 0, 255))

        os.system('clear')
        print('Detected Class: ' + label)
        print('Confidence: ', max(predictions))
        print('Time Taken: ', toc - tic)

        cv2.imshow('frame', frame)
        cv2.imshow('img', frame[20:320, 20:320])
        cv2.moveWindow('frame', 1000, 500)
        cv2.moveWindow('img', 1000, 100)

        if cv2.waitKey(5) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()


if __name__ == '__main__':
    main()
