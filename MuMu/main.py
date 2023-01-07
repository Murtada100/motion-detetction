import cv2
import matplotlib.pyplot as plt
import matplotlib.animation as animation

#Initialising background used from video
background = cv2.imread("background2.jpg")
background = cv2.cvtColor(background,cv2.COLOR_BGR2GRAY)
background = cv2.GaussianBlur(background, (21, 21), 0)

#Initialising the video file
video = cv2.VideoCapture("test.mp4")

#Made a function to extract frames
def extract_frames(frames):
    frames=[]
    i=0
    while(1):
        ret,frame=video.read()
        if ret:
            frame=cv2.resize(frame,dsize=(600,400))
            frame=cv2.cvtColor(frame,cv2.COLOR_BGR2RGB)
            frames.append(frame)
   

while True:
    status, frame = video.read()
    gray = cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
    gray = cv2.GaussianBlur(gray,(21,21), 0)

    diff = cv2.absdiff(background, gray)

    thresh = cv2.threshold(diff, 30, 255, cv2.THRESH_BINARY)[1]
    thresh = cv2.dilate(thresh, None, iterations = 2)
    
    #Setting up contours to appear when movement is detected
    cnts, res = cv2.findContours(thresh.copy(),
        cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    
    #Initialising contour sensitivity and specifics
    for contour in cnts:
        if cv2.contourArea(contour) < 10000:
            continue
        (x, y, w, h) = cv2.boundingRect(contour)
        cv2.rectangle(frame, (x,y), (x+w, y+h), (0, 255, 0), 3)
        
        #This extract frames function now removes all frames of the video that contains the contours.
        #If you comment the function below out you can see the full video
        extract_frames(frame)
        #How do I use the extracted frames and append them into a clip?
  
    cv2.imshow("All Countours", frame)

    #cv2.imshow("Threshold Video", thresh)

    #cv2.imshow("Diff Video", diff)
    #cv2.imshow("Gray Video", gray)
    key = cv2.waitKey(1)
    if key == ord('q'):
        break

video.release()
cv2.destroyWindows()   