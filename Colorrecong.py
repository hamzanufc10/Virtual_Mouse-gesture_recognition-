import cv2
import numpy as np

cam=cv2.VideoCapture(0)
kernelOpen=np.ones((5,5))
kernelClose=np.ones((20,20))

fontface = cv2.FONT_HERSHEY_SIMPLEX
fontscale = 2
fontcolor = (5000 ,0 ,0)



lowerBound=np.array([33,80,40])
upperBound=np.array([102,255,255])
while True:
    ret,img=cam.read()
    img = cv2.resize(img, (340, 220))

    # convert BGR to HSV
    imgHSV = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    # create the Mask
    mask = cv2.inRange(imgHSV, lowerBound, upperBound)
    #morpholoygy

    maskOpen = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernelOpen)
    maskClose = cv2.morphologyEx(maskOpen, cv2.MORPH_CLOSE, kernelClose)

    maskFinal = maskClose
    #################
    conts, h = cv2.findContours(maskFinal.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)

    #to draw contour
    cv2.drawContours(img, conts, -1, (255, 0, 0), 3)

    #to place a rectangle over contour
    for i in range(len(conts)):
        x, y, w, h = cv2.boundingRect(conts[i])
        cv2.rectangle(img, (x, y), (x + w, y + h), (0, 0, 255), 2)
        #cv2.cv.PutText(cv2.cv.fromarray(img), str(i + 1), (x, y + h), font, (0, 255, 255))
        cv2.putText((img), str(i + 1), (x, y + h), fontface, fontscale, fontcolor)
    cv2.imshow('maskOpen', maskOpen)
    cv2.imshow('maskClose', maskClose)
    cv2.imshow('mask',mask)
    cv2.imshow('org',img)
    cv2.waitKey(10)
