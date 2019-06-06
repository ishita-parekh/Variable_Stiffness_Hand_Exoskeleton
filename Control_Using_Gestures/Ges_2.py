#Import python libraries
import cv2
import numpy as np
import math

import wx
import time
from Dynamixel import dynamixel

ID = 1
ID_1 = 6
ID_2 = 8
ID_3= 11
ID_4 = 14
ID_5 = 15
SPEED_REG = 32
POS_REG = 30

#import pyautogui

#Capturing the video from web camera
cap = cv2.VideoCapture(0)
     
while(cap.isOpened()):
        
          
        ret, frame = cap.read()
        frame=cv2.flip(frame,1)
        kernel = np.ones((3,3),np.uint8)
        
        #Define the region of interest
        roi=frame[100:300, 100:300]
        
        #Draw a rectangle and convert BGR to HSV color space in specified region of interest
        cv2.rectangle(frame,(100,100),(300,300),(0,255,0),0)    
        hsv = cv2.cvtColor(roi, cv2.COLOR_BGR2HSV)
            
        #Define range of skin color in HSV
        lower_range = np.array([0,20,70], dtype=np.uint8)
        upper_range = np.array([20,255,255], dtype=np.uint8)
        
        #Threshold the HSV image to get only skin colour 
        mask = cv2.inRange(hsv, lower_range, upper_range)
        
        #Dilate to fill the broken parts of hand 
        mask = cv2.dilate(mask,kernel,iterations = 4)
        
        #Smoothen the image to reduce noise
        mask = cv2.GaussianBlur(mask,(5,5),100) 
            
        #Find contours in the masked frame
        _,contours,hierarchy= cv2.findContours(mask,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
    
        try:
            #Find contour of max area (hand)
            cnt = max(contours, key = lambda x: cv2.contourArea(x))
        
            #Approximate the hand contour
            epsilon = 0.0005*cv2.arcLength(cnt,True)
            approx= cv2.approxPolyDP(cnt,epsilon,True)
        
            #Make convex hull around hand
            hull = cv2.convexHull(cnt)
        
            #Define area of the convex hull and area of the hand contour
            area_hull = cv2.contourArea(hull)
            area_cnt = cv2.contourArea(cnt)
      
            #Find the percentage of area not covered by hand contour in convex hull
            area_ratio=((area_hull-area_cnt)/area_cnt)*100
    
            #Find the defects in convex hull with respect to hand
            hull = cv2.convexHull(approx, returnPoints=False)
            defects = cv2.convexityDefects(approx, hull)
        except:
            pass
      
        try:
            no_of_defects=0
        
            #Finding number of defects between fingers

            #Storing start, end, far points of defects
            for i in range(defects.shape[0]):
                s,e,f,d = defects[i,0]
                start = tuple(approx[s][0])
                end = tuple(approx[e][0])
                far = tuple(approx[f][0])
                pt= (100,180)
            
            
                # Finding length of all sides of triangle created due to each defect
                a = math.sqrt((end[0] - start[0])**2 + (end[1] - start[1])**2)
                b = math.sqrt((far[0] - start[0])**2 + (far[1] - start[1])**2)
                c = math.sqrt((end[0] - far[0])**2 + (end[1] - far[1])**2)
                s = (a+b+c)/2
                ar = math.sqrt(s*(s-a)*(s-b)*(s-c))
            
                #Finding distance between farthest point of defect and convex hull
                d=(2*ar)/a
            
                #Finding angle of each defect using cosine rule
                angle = math.acos((b**2 + c**2 - a**2)/(2*b*c)) * 57
            
        
                #Discard angles greater than 90 degrees and points very close to convex hull (they are generally due to noise)
                if angle <= 90 and d>30:
                    no_of_defects += 1
                    cv2.circle(roi, far, 3, [255,0,0], -1)
            
                #Drawing lines around hand making a convex hull
                cv2.line(roi,start, end, [0,255,0], 2)
        except:
            pass
        
        try:
            no_of_defects+=1
        
            #Displaying what gestures are recognized in region of interest
            font = cv2.FONT_HERSHEY_SCRIPT_SIMPLEX
            if no_of_defects==1:

                if area_cnt<2000:
                    cv2.putText(frame,'Place your hand',(0,50), font, 2, (255,0,0), 3, cv2.LINE_AA)
                    

                else:
                    if area_ratio<12:
                        cv2.putText(frame,'Closed fist',(0,50), font, 2, (255,0,0), 3, cv2.LINE_AA)
                        speed = 190
                        speed_2 = 1390
                        
                        self.ax12 = dynamixel()
                        self.ax12.set_ax_reg(ID, SPEED_REG, ([(speed%256),(speed>>8)]))
                        self.ax12.set_ax_reg(ID_3, SPEED_REG, ([(speed%256),(speed>>8)]))
                        self.ax12.set_ax_reg(ID_4, SPEED_REG, ([(speed%256),(speed>>8)]))
                        self.ax12.set_ax_reg(ID_1, SPEED_REG, ([(speed_2%256),(speed_2>>8)]))
                        self.ax12.set_ax_reg(ID_2, SPEED_REG, ([(speed_2%256),(speed_2>>8)]))
                        self.ax12.set_ax_reg(ID_5, SPEED_REG, ([(speed_2%256),(speed_2>>8)]))
                        

                        time.sleep(4)

                        speed = 0
                        speed_2=0

                        
                        self.ax12 = dynamixel()
                        self.ax12.set_ax_reg(ID, SPEED_REG, ([(speed%256),(speed>>8)]))
                        self.ax12.set_ax_reg(ID_1, SPEED_REG, ([(speed_2%256),(speed_2>>8)]))
                        self.ax12.set_ax_reg(ID_2, SPEED_REG, ([(speed_2%256),(speed_2>>8)]))
                        self.ax12.set_ax_reg(ID_3, SPEED_REG, ([(speed%256),(speed>>8)]))
                        self.ax12.set_ax_reg(ID_4, SPEED_REG, ([(speed%256),(speed>>8)]))
                        self.ax12.set_ax_reg(ID_5, SPEED_REG, ([(speed_2%256),(speed_2>>8)]))

                    elif (area_ratio>12 and area_ratio<17.5):
                        cv2.putText(frame,'Best of luck',(0,50), font, 2, (255,0,0), 3, cv2.LINE_AA)
                   
                    else:
                        cv2.putText(frame,'1',(0,50), font, 2, (255,0,0), 3, cv2.LINE_AA)
                        
                    
            elif no_of_defects==2:
                cv2.putText(frame,'2',(0,50), font, 2, (255,0,0), 3, cv2.LINE_AA)
                
            
            elif no_of_defects==3:
         
                  if area_ratio<27:
                        cv2.putText(frame,'3',(0,50), font, 2, (255,0,0), 3, cv2.LINE_AA)
                   
                  else:
                        cv2.putText(frame,'Ok',(0,50), font, 2, (255,0,0), 3, cv2.LINE_AA)
                    
            elif no_of_defects==4:
                cv2.putText(frame,'4',(0,50), font, 2, (255,0,0), 3, cv2.LINE_AA)
                
            
            elif no_of_defects==5:
                cv2.putText(frame,'5',(0,50), font, 2, (255,0,0), 3, cv2.LINE_AA)
                
            
            elif no_of_defects==6:
                cv2.putText(frame,'Reposition',(0,50), font, 2, (255,0,0), 3, cv2.LINE_AA)
            
            else :
                cv2.putText(frame,'Reposition',(10,50), font, 2, (255,0,0), 3, cv2.LINE_AA)
        except:
            pass
            
        #Showing mask and video frame window on output
        cv2.imshow('mask',mask)
        cv2.imshow('frame',frame)
        
    
        k = cv2.waitKey(5) & 0xFF
        if k == 27:
            break
     
  
