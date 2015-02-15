import numpy as np
import cv2
import cv
import datetime
import math
import time
import ScreenBlocker as sb
import os

cap = cv2.VideoCapture(0)
test = False
x = 0
y = 0
z = 0
itorX = 0
itorY = 0
div = 10

def init():
    ret, imgBase = cap.read()
    print(type(imgBase))
    x, y, z = imgBase.shape
    global itorY,itorX
    itorX = (x / div)
    itorY = (y / div)

def analyseRecord(record):
    global itorY
    global itorX
    dangerCounts = np.zeros((itorX,itorY),dtype = np.uint8)
    for dangerMap in record:
        dangerCounts += dangerMap.astype(int)
    return np.any(np.greater(dangerCounts,5))


def overallScan(img1, img2):

    # Our operations on the frame come here

    hist1 = cv2.calcHist([img1],[0],None,[256],[0,256])
    hist2 = cv2.calcHist([img2],[0],None,[256],[0,256])
    sc = cv2.compareHist(hist1, hist2, cv.CV_COMP_BHATTACHARYYA)
    #print(hist1)
    if(sc > 0.15):
        return True
    else:
        return False

def percisesScan(img1, img2):
    global count, itorX, itorY,div
    dangerMap = np.zeros((itorX,itorY),dtype = np.bool)
    for X in range(0, itorX):
        for Y in range(0, itorY):
            #return que(results, -7, segment(img1, img2, X, Y))
            histS1 = cv2.calcHist([img1[X*div:(X+1)*div,Y*div:(Y+1)*div]],[0],None,[256],[0,256])
            histS2 = cv2.calcHist([img2[X*div:(X+1)*div,Y*div:(Y+1)*div]],[0],None,[256],[0,256])
            sc = cv2.compareHist(histS1, histS2, cv.CV_COMP_BHATTACHARYYA)
            #print sc
            dangerMap[X,Y] = sc > 0.95
    return dangerMap

def tic():
    global t
    t = time.time()

def toc():
    global t
    elapsed = time.time() - t
    print elapsed," Seconds Elapsed"

def scan(img1, img2):
    return percisesScan(img1,img2)



init()

dangerMapRecord = []
ret, imgOld = cap.read()
while(True):
    # do stuff
    tic()
    ret, imgNew = cap.read()
    if imgNew is not None:
        dangerMapRecord.append(scan(imgOld, imgNew))
        if len(dangerMapRecord) > 10:
            dangerMapRecord.pop(0)
            if analyseRecord(dangerMapRecord):
                sb.blockScreen()
                dangerMapRecord = []



        #cv2.imshow('frame',imgNew)
        imgOld =imgNew
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    toc()
# When everything done, release the capture
cap.release()
cv2.destroyAllWindows()
