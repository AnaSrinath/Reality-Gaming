#!/usr/bin/env python
# coding: utf-8

# In[ ]:


from tkinter import *
import cv2
import numpy as np
from collections import deque
import time
import pyautogui


pts = deque(maxlen = 16)
cam = cv2.VideoCapture(0)
time.sleep(0)


def image_processing(frame,x):  
    frame = cv2.resize(frame, (int(frame.shape[1]/1), int(frame.shape[0]/1)))    
    if x == 0:
        greyImg = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        return greyImg
    
    elif x == 1:
        blurred_frame = cv2.GaussianBlur(frame, (5,5), 0)
        hsv_converted_frame = cv2.cvtColor(blurred_frame, cv2.COLOR_BGR2HSV)
        return hsv_converted_frame
        

def obj_det():
    Lower = (61,94,76)      
    Upper = (162,211,253)
    (dX,dY) = (0,0)
    
    while True:
        _,frame = cam.read() 
        frame = cv2.flip(frame,1) 
        
        mask = cv2.inRange(image_processing(frame,1), Lower, Upper)
        mask = cv2.erode(mask, None, iterations = 2)
        mask = cv2.dilate(mask, None, iterations = 2)
        
        cnts = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)[-2]
        center = None
        
        if(len(cnts)) > 0:
            c = max(cnts, key = cv2.contourArea)
            ((x,y), radius) = cv2.minEnclosingCircle(c)            
            center = (int(x), int(y))
            
            if radius > 10:
                cv2.circle(frame, (int(x), int(y)), int(radius), (0,255,255), 2)
                cv2.circle(frame, center, 5, (0,255,255), -1)
            pts.appendleft(center)    
            
            for i in range(1, len(pts)):
                if pts[i-1] is None or pts[i] is None:
                    continue
                
                if i > 10 and pts[10] is not None:
                    dX = pts[10][0] - pts[i][0]
                    dY = pts[10][1] - pts[i][1]
                    
                if np.abs(dX) > 20:
                    if np.sign(dX) == 1:
                        cv2.putText(frame,'RIGHT',(10,20),cv2.FONT_HERSHEY_SIMPLEX,0.5,(0,0,255),2) 
                        pyautogui.press('right',presses=1)
                        pyautogui.PAUSE = 0
                        
                    else:
                        cv2.putText(frame,'LEFT',(10,20),cv2.FONT_HERSHEY_SIMPLEX,0.5,(0,0,255),2) 
                        pyautogui.press('left',presses=1)
                        pyautogui.PAUSE = 0
                        
                if np.abs(dY) > 20:
                    if np.sign(dY) == 1:
                        cv2.putText(frame,'ROLL',(10,20),cv2.FONT_HERSHEY_SIMPLEX,0.5,(0,0,255),2) 
                        pyautogui.press('down',presses=1)
                        pyautogui.PAUSE = 0
                    
                    else:
                        cv2.putText(frame,'JUMP',(10,20),cv2.FONT_HERSHEY_SIMPLEX,0.5,(0,0,255),2) 
                        pyautogui.press('up',presses=1)
                        pyautogui.PAUSE = 0
        
        cv2.imshow('Frame', frame)
        key = cv2.waitKey(1) & 0xFF
        
        if(key == ord('q')):
            break
        
    cam.release()
    cv2.destroyAllWindows()

    
    
def face_det():
    haar_cascade = cv2.CascadeClassifier(r'C:\Users\hp\anaconda3\Lib\site-packages\cv2\data\haarcascade_frontalface_default.xml') 
    (dX,dY) = (0,0)
    
    while True:
        _,frame = cam.read()
        frame = cv2.flip(frame,1) 
        frame1 = image_processing(frame,0)
        
        face = haar_cascade.detectMultiScale(frame1,1.3,4)  
    
        cv2.rectangle(frame,(0,0),(639,150),(255,0,0),1) 
        cv2.rectangle(frame,(0,310),(639,480),(255,0,0),1)
        y1 = 160
        h1 = 0
        
        for (x,y,w,h) in face:
            cv2.rectangle(frame,(x,y),(x+w,y+h),(0,255,0),2) 
            sp = (x,y)
            y1,h1 = y,h
            pts.appendleft(sp)  
        
        for i in range(1, len(pts)):
            if pts[i-1] is None or pts[i] is None:
                continue
                
            if i > 10 and pts[10] is not None:
                dX = pts[10][0] - pts[i][0]
                dY = pts[10][1] - pts[i][1]
                
            if np.abs(dX) > 50:
                if np.sign(dX) == 1:
                    cv2.putText(frame,"RIGHT",(10,20),cv2.FONT_HERSHEY_SIMPLEX,0.5,(0,0,255),2) 
                    pyautogui.press('right', presses=1)
                    pyautogui.PAUSE = 0
                
                else:
                    cv2.putText(frame,"LEFT",(10,20),cv2.FONT_HERSHEY_SIMPLEX,0.5,(0,0,255),2)
                    pyautogui.press('left', presses=1)
                    pyautogui.PAUSE = 0
                                        
            if y1+h1 > 320:
                cv2.putText(frame,"ROLL",(10,20),cv2.FONT_HERSHEY_SIMPLEX,0.5,(0,0,255),2)   
                pyautogui.press('down', presses=1)
                pyautogui.PAUSE = 0
                
            elif y1 < 140:
                cv2.putText(frame,"JUMP",(10,20),cv2.FONT_HERSHEY_SIMPLEX,0.5,(0,0,255),2) 
                pyautogui.press('up', presses=1)
                pyautogui.PAUSE = 0
                
        cv2.imshow("CameraFeed",frame)
        key = cv2.waitKey(1) & 0xFF
        
        #If q is pressed, close the window
        if(key == ord('q')):
            break
        
    cam.release()
    cv2.destroyAllWindows()       
            


root = Tk()
root.title("Console")
root.geometry('900x400')
root.config(bg = "black")
name = Label(root,text="WELCOME TO THE REALITY GAMING CONSOLE",bg = 'black',fg = 'seagreen2',font = ('Fixedsys',24)).place(x = 78,y = 50)

img = PhotoImage(file = r'C:\Users\hp\Desktop\face.png')
button1 = Button(image=img,command = face_det)
button1.place(x = 330, y = 150)

img1 = PhotoImage(file = r'C:\Users\hp\Desktop\obj.png')
button4 = Button(image=img1,command = obj_det)
button4.place(x = 330,y = 210)

exit = Button(text = "EXIT",font = ('System',14),command = root.destroy).place(x = 430,y= 300)

root.mainloop()

