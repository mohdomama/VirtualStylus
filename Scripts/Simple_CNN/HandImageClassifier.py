import cv2
import tensorflow as tf
import os
import time

IMG_SIZE = 100
model = tf.keras.models.load_model('TrainedModels/Hand-CNN-v2-CO.model')
CATEGORIES = ['C', 'O']


def get_label(img):
    # img = cv2.flip(img,1)
    img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    img = cv2.resize(img, (IMG_SIZE, IMG_SIZE))
    img = img.reshape(-1, IMG_SIZE, IMG_SIZE, 1)

    prediction = model.predict([img])
    return CATEGORIES[int(prediction[0][0])]


def main():
    cap = cv2.VideoCapture(0)

    while True:
        _, frame = cap.read()
        cv2.rectangle(frame, (20, 20), (320, 320), (255, 0, 0), 2)
        cv2.imshow("img", frame[20:320, 20:320])

        tic = time.time()
        label = get_label(frame[20:320, 20:320])
        toc = time.time()
        cv2.putText(frame, label, (20, 380), cv2.FONT_HERSHEY_COMPLEX,
                    3.0, (255, 255, 255))

        os.system('clear')
        print('Detected Gesture: ' + label)
        print('Time Taken: ', toc - tic)
        cv2.imshow("frame", frame)

        if cv2.waitKey(5) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()


if __name__ == '__main__':
    main()
