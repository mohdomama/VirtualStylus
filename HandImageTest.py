import cv2
import tensorflow as tf
import os
import time

IMG_SIZE = 100
model = tf.keras.models.load_model('TrainedModels/Hand-CNN-v2-CO.model')
CATEGORIES = ['C', 'O']
DATADIR = 'static/Test/'

def get_label(img):
    # img = cv2.flip(img,1)
    img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    img = cv2.resize(img, (IMG_SIZE, IMG_SIZE))
    img = img.reshape(-1, IMG_SIZE, IMG_SIZE, 1)

    prediction = model.predict([img])
    return CATEGORIES[int(prediction[0][0])]


def test(expect):
    count  = 0
    
    print('Expecting: ' + expect)
    num = len(os.listdir(DATADIR + expect))
    
    for name in (os.listdir(DATADIR + expect)):
        img = cv2.imread(DATADIR + expect + '/' + name)
        label = get_label(img)

        #print(name + ' ' + label)
        
        if label == expect:
            count += 1
    
    print('Percentage: ' , count/num * 100)


def main():

    '''
    count = 0
    print('Testing for C:')
    for i in range(4, 36):
        img = cv2.imread(DATADIR + '/{}.jpg'.format(i))
        label = get_label(img)
        if label == 'C':
            count += 1

        print('Label for image {} : '.format(i-3) + label)
    print('Percentage: {}'.format(count/32 * 100))


    count = 0
    print('Testing for C:')
    for i in range(4, 54):
        img = cv2.imread(DATADIR + '/{}.jpg'.format(i))
        label = get_label(img)
        if label == 'O':
            count += 1
        print('Label for image {}'.format(i-3) + label)
    print('Percentage: {}'.format(count/50 * 100))
    '''

    test('C')
    test('O')

if __name__ == '__main__':
    main()

