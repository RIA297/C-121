import cv2
import time
import numpy as np
fourcc= cv2.VideoWriter_fourcc(*"XVID")
output_file=cv2.VideoWriter("output.avi",fourcc,20.0,(640,480))
# starting the webcam
cap=cv2.VideoCapture(0)
# allowing the webcam to start by making the code sleep for 2 secs
time.sleep(2)
bg=0
for i in range (60):
    ret,img=cap.read()
    if not ret:
        break
    #flipping the img for consistency
    img=np.flip(img,axis=1)
    #converting the color from bgr to hsv
    hsv = cv2.cvtColor(img,cv2.COLOR_BGR2HSV)
    #generating mask to detect red color 
    #values can also be changed as per color
    lower_red = np.array([0,120,50])
    upper_red =np.array([10,255,255])
    mask_1 = cv2.inRange(hsv,lower_red,upper_red)
    lower_red=np.array([170,120,70])
    upper_red=np.array([180,255,255])
    mask_2 =cv2.inRange(hsv,lower_red,upper_red)
    mask_1 = mask_1 + mask_2
    # Open and expand the img where there is mask_1
    mask_1=cv2.morphologyEx(mask_1,cv2.MORPH_OPEN,np.ones((3,3),np.uint8))
    mask_1=cv2.morphologyEx(mask_1,cv2.MORPH_DILATE,np.ones((3,3),np.uint8))
    # Selecting only the part that does not have mask_1 and saving in mask_2
    mask_2 = cv2.bitwise_not(mask_1)
    # Keeping only the part of imgs without the red color
    res_1 = cv2.bitwise_and(img,img,mask=mask_2)
    # Keeping only the part of images with the red color
    res_2=cv2.bitwise_and(bg,bg,mask=mask_1)
    # generating the final output by merging res1 and res2
    final_output=cv2.addWeighted(res_1,1,res_2,1,0)
    output_file.write(final_output)
    #displaying the output to the user 
    cv2.imshow("magic",final_output)
    cv2.waitKey(1)
cap.release()
cv2.destroyAllWindows()
