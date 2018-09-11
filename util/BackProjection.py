import numpy as np
import cv2



def calculate_hist_2D(hsvr, dim):
	# Bilateral Filtering
	# calculating object histogram
	roi_hist = cv2.calcHist([hsvr],dim, None, [256, 256], [0, 256, 0, 256] )

	# normalize histogram and apply backprojection
	cv2.normalize(roi_hist,roi_hist,0,255,cv2.NORM_MINMAX)

	return roi_hist

def back_proj_2D(hsvt, roi_hist, dim, target):
	

	dst = cv2.calcBackProject([hsvt],dim,roi_hist,[0,256,0,256],1)

	# Now convolute with circular disc. Play with it
	disc = cv2.getStructuringElement(cv2.MORPH_ERODE,(15,15))

	cv2.filter2D(dst,-1,disc,dst)

	# threshold and binary AND
	ret,thresh = cv2.threshold(dst,175,255,cv2.THRESH_BINARY+cv2.THRESH_OTSU)
	thresh = cv2.merge((thresh,thresh,thresh))
	#thresh = cv2.GaussianBlur(thresh, (35, 35), 0)

	return thresh

def back_proj_1D(hsvr, hsvt, dim, target):
	# calculating object histogram
	roi_hist = cv2.calcHist([hsvr],[dim], None, [256], [0, 256] )

	# normalize histogram and apply backprojection
	cv2.normalize(roi_hist,roi_hist,0,255,cv2.NORM_MINMAX)

	dst = cv2.calcBackProject([hsvt],[dim],roi_hist,[0,256],1)

	# Now convolute with circular disc
	disc = cv2.getStructuringElement(cv2.MORPH_ELLIPSE,(13,13))

	cv2.filter2D(dst,-1,disc,dst)

	# threshold and binary AND
	ret,thresh = cv2.threshold(dst,50,255,0)
	thresh = cv2.merge((thresh,thresh,thresh))
	res = cv2.bitwise_and(target,thresh)
	res = cv2.resize(res, (800, 500)) 
	return res


def calculate(roi, target):
	

	hsvr = cv2.cvtColor(roi,cv2.COLOR_BGR2HSV)
	hsvt = cv2.cvtColor(target,cv2.COLOR_BGR2HSV)

	roi_hist_0 = calculate_hist_2D(hsvr, [0,1])
	roi_hist_1 = calculate_hist_2D(hsvr, [1, 2])
	roi_hist_2 = calculate_hist_2D(hsvr, [2, 0])


	res2D_0 = back_proj_2D(hsvt, roi_hist_0,[0, 1], target)
	res2D_1 = back_proj_2D(hsvt, roi_hist_1, [1, 2], target)
	res2D_2 = back_proj_2D(hsvt, roi_hist_2, [2, 0], target)

	res = cv2.bitwise_and(res2D_0, res2D_1)
	res = cv2.bitwise_and(res, res2D_2)



	return res



