import cv2
import numpy as np
from util import BackProjection as bp
from math import sqrt, acos, degrees

def contours(hist_mask_image):
    gray_hist_mask_image = cv2.cvtColor(hist_mask_image, cv2.COLOR_BGR2GRAY)
    ret, thresh = cv2.threshold(gray_hist_mask_image, 0, 255, 0)
    _, cont, hierarchy = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    return cont

def max_contour(contours_list):
    max_area = 0
    for i in range(len(contours_list)):
        c = contours_list[i]
        if cv2.contourArea(c) > max_area:
            max_area = cv2.contourArea(c)
            max_index = i
            bound_rec = c

    return max_index, bound_rec

def roi_extract(frame):
    roi_defined = False
    roi = None

    x1, y1 = 100, 100
    x2, y2 = 200, 260

    cv2.rectangle(frame, (x1,y1), (x2, y2), (255, 0, 0))
    cv2.imshow('Display', frame)

    if cv2.waitKey(5) & 0xFF == ord('c'):
        roi = frame[y1:y2, x1:x2]
        roi_defined = True

    return roi_defined, roi

def cal_ang(start, end, far):
    A = cal_des(far, start)
    B = cal_des(far, end)
    C = cal_des(start, end)

    return degrees(acos((A * A + B * B - C * C)/(2.0 * A * B)))


def cal_des(p1, p2):
    return sqrt( 
        (p1[0] - p2[0])**2 + 
        (p1[1] - p2[1])**2 
        )




def main():
    roi_defined = False

    cap = cv2.VideoCapture(0)

    while True:
        _, frame = cap.read()

        if roi_defined == False:
            roi_defined, roi = roi_extract(frame)


        else:

            mask = bp.calculate(roi, frame)


            contours_list = contours(mask)


            #find the biggest area
            max_cont ,rec = max_contour(contours_list)

            hull = cv2.convexHull(rec, returnPoints = False)

            defects = cv2.convexityDefects(rec,hull)

            for i in range(defects.shape[0]):
                s,e,f,d = defects[i,0]
                start = tuple(rec[s][0])
                end = tuple(rec[e][0])
                far = tuple(rec[f][0])

                angle = cal_ang(start, end, far)

                mid = (
                    (start[0] + end[0])/2,
                    (start[1] + end[1])/2,
                    )
                des = cal_des(mid, far)

                cv2.line(frame,start,end,[0,255,0],2)

                if des > 70 and angle < 55:
                    cv2.circle(frame,far,5,[0,0,255],-1)


            x,y,w,h = cv2.boundingRect(rec)
            # draw the book contour (in green)
            cv2.rectangle(frame,(x,y),(x+w,y+h),(0,0,255),2)
            #cv2.drawContours(frame, [hull], 0, (0,255,0), 3)


            cv2.imshow('Display', mask)
            cv2.imshow('Display2', frame)

        if cv2.waitKey(5) & 0xFF == ord('q'):
            break
     
    cv2.destroyAllWindows()

if __name__ == '__main__':
    main()