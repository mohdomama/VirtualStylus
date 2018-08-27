import cv2
import numpy as np

def call_back(x):
    pass

def create(name):
    image = cv2.namedWindow(name)
    cv2.moveWindow(name, 1000,0)
    cv2.createTrackbar('H_high', name, 255, 255, call_back)
    cv2.createTrackbar('H_low', name, 0, 255, call_back)
    cv2.createTrackbar('S_high', name, 255, 255, call_back)
    cv2.createTrackbar('S_low', name, 0, 255, call_back)
    cv2.createTrackbar('V_high', name, 255, 255, call_back)
    cv2.createTrackbar('V_low', name, 0, 255, call_back)

def extract(name):
    H_high = cv2.getTrackbarPos('H_high', name) 
    H_low = cv2.getTrackbarPos('H_low', name)
    S_high = cv2.getTrackbarPos('S_high', name) 
    S_low = cv2.getTrackbarPos('S_low', name)
    V_high = cv2.getTrackbarPos('V_high', name) 
    V_low = cv2.getTrackbarPos('V_low', name)

    return (
        (H_low, S_low, V_low),
        (H_high, S_high, V_high) )
