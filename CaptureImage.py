import os
import cv2

def main() :

	gestureClass = input("Enter the type of gesture")

	cap = cv2.VideoCapture(0)

	rootName = 'HandGestures/' + gestureClass

	try:
		if(not os.path.exists(rootName)):
			os.makedirs(rootName)
	except OSError:
		print('Cannot create the directory')

	currentFrame = 0

	while(True):

		if(not cap.isOpened()):
			cap.open()

		ret, frame = cap.read()

		frame = cv2.resize(frame, (128, 128)) 

		cv2.imshow('frame', frame)

		path = "./"+rootName

		print(path)

		cv2.imwrite(path+"/{}.jpg".format(currentFrame), frame)

		if(cv2.waitKey(0) & 0xFF == ord('q')):
			break

		currentFrame+=1

	cap.release()
	cv2.destroyAllWindows()

if __name__ == '__main__':
	main()

