#to import opencv
import cv2
import numpy as np

#controller for controling the mouse
#button - for left and right click
from pynput.mouse import Button,Controller

#to get the screen size of our system
import wx


mouse=Controller()
app=wx.App(False)

#to get the display size of the monitor(for large screen)
(sx,sy)=wx.GetDisplaySize()
#to set the camera resolution and capture the image(fro small screen)
(camx,camy)=(320,240)

lowerBound=np.array([33,80,40])
upperBound=np.array([102,255,255])


cam=cv2.VideoCapture(0)

cam.set(3,camx)
cam.set(4,camy)
kernelOpen=np.ones((5,5))
kernelClose=np.ones((20,20))
#because we cannot divide list or substract list
mLocOld=np.array([0,0])
mouseLoc=np.array([0,0])
DamingFactor=2
pinchFlag=0
openx, openy, openw, openh=(0,0,0,0)


#mouseLoc=mLocOld+(targetLoc-mLocOld)/DamingFactor
while True:
    ret,img=cam.read()
    #img = cv2.resize(img, (340, 220))

    # convert BGR to HSV
    imgHSV = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    # create the Mask
    mask = cv2.inRange(imgHSV, lowerBound, upperBound)
    #morpholoygy

    maskOpen = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernelOpen)
    maskClose = cv2.morphologyEx(maskOpen, cv2.MORPH_CLOSE, kernelClose)

    maskFinal = maskClose
    conts, h = cv2.findContours(maskFinal.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    if (len(conts) == 2):
        #if there are 2 green object
        if(pinchFlag==1):
            pinchFlag=0
            #if we will do a open gesture then it will release the mouse
            mouse.release(Button.left)
         #h,w of first object
        x1, y1, w1, h1 = cv2.boundingRect(conts[0])
        #h,w of 2nd object
        x2, y2, w2, h2 = cv2.boundingRect(conts[1])

        #lets create a rectangle over the first object
        cv2.rectangle(img, (x1, y1), (x1 + w1, y1 + h1), (255, 0, 0), 2)
        # lets create a rectangle over the second  object
        cv2.rectangle(img, (x2, y2), (x2 + w2, y2 + h2), (255, 0, 0), 2)
        #center point of the first rectangle
        cx1 = x1 + w1 // 2
        cy1 = y1 + h1 // 2
        #center pont of the second rectangle
        cx2 = x2 + w2 // 2
        cy2 = y2 + h2 // 2
        cx = (cx1 + cx2) // 2
        cy = (cy1 + cy2) // 2
        cv2.line(img, (cx1, cy1), (cx2, cy2), (255, 0, 0), 2)
        cv2.circle(img, (cx, cy), 2, (0, 0, 255), 2)


        mouseLoc = mLocOld + ((cx,cy) - mLocOld) / DamingFactor
        mouse.position=(sx-(mouseLoc[0]*sx//camx),mouseLoc[1]*sy//camy)
        while mouse.position!=(sx-(mouseLoc[0]*sx//camx),mouseLoc[1]*sy//camy):
            pass
        mLocOld=mouseLoc


    elif (len(conts) == 1):
        x, y, w, h = cv2.boundingRect(conts[0])
        #if there is one object
        if (pinchFlag == 0):
            #if(abs((w*h-openw*openh)*100/(w*h))<20):

                pinchFlag = 1
            #if we will perform a close gesture it will do a left click
                mouse.press(Button.left)
                openx, openy, openw, openh=(0,0,0,0)
            #h,w of 2 object
        x, y, w, h = cv2.boundingRect(conts[0])
        #we will create a rectangle over that object
        cv2.rectangle(img, (x, y), (x + w, y + h), (255, 0, 0), 2)
        cx = x + w // 2
        cy = y + h // 2
        #get the center of the rectangle and create a circle
        cv2.circle(img, (cx, cy), (w + h) // 4, (0, 0, 255), 2)



        mouseLoc = mLocOld + ((cx, cy) - mLocOld) / DamingFactor



        #change mouse position from small screen to big screen
        mouse.position = (sx - (mouseLoc[0] * sx // camx), mouseLoc[1] * sy // camy)
        while mouse.position != (sx - (mouseLoc[0] * sx // camx), mouseLoc[1] * sy // camy):
            pass
        mLocOld = mouseLoc


        cv2.drawContours(img, conts, -1, (255, 0, 0), 3)
        #cv2.imshow('maskOpen', maskOpen)
        #cv2.imshow('maskClose', maskClose)
        #cv2.imshow('mask',mask)

    cv2.imshow('org',img)
    cv2.waitKey(10)
