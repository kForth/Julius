import numpy as np
import cv2
import time

def blockScreen(screenWidth, screenHeight):
    img = np.zeros((screenHeight, screenWidth), np.uint8) #Create black empty box

    cv2.rectangle(img, (0, 0), (screenWidth, screenHeight), (50, 50, 50), -1)

    drawCenteredText(img, "Julius", cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 60);

    drawCenteredText(img, "Possible Seizure Avoided", cv2.FONT_HERSHEY_SIMPLEX, 2, (255, 255, 255), screenHeight / 2)

    cv2.imshow("Julius", img) #Show the screen
    cv2.moveWindow("Julius", 0, 0) #Move the window to the top left corner
    cv2.waitKey(3000) #Close the window after 30 seconds

def drawCenteredText(img, text, font, scale, color, yPos):
    size = cv2.getTextSize(text, font, scale, 1)
    textWidth = size[0][0]
    textHeight = size[0][1]
    width = img.shape[1]

    cv2.putText(img, text, ((width - textWidth) / 2, yPos), font, scale, color, 1, cv2.CV_AA)


time.sleep(60)

blockScreen(1440, 900)
