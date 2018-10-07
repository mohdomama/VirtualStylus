import os
import sys
import cv2


def main() :

	gestureClass = input("Enter the type of gesture")
	imageName = input("Enter the image name")

	cap = cv2.VideoCapture(0)
	rootName = 'HandGestures/' + gestureClass

	try:
		if(not os.path.exists(rootName)):
			os.makedirs(rootName)
	except OSError:
		print('Directory Exists')
		sys.exit(0)

	currentFrame = 0

	while(True):

		if(not cap.isOpened()):
			cap.open()

		ret, frame = cap.read()
		frame = cv2.resize(frame, (128, 128))
		cv2.imshow('frame', frame)

		path = os.path.join("./", rootName)
		print(path)

		cv2.imwrite(path+"/{}{}.jpg".format(imageName, currentFrame), frame)

		if(cv2.waitKey(0) & 0xFF == ord('q')):
			break
		currentFrame+=1

	cap.release()
	cv2.destroyAllWindows()


if __name__ == '__main__':
	main()

