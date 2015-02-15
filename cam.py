import numpy as np
import cv2
import cv
import datetime
import math

cap = cv2.VideoCapture(1)
data = [[False for i in range(100)] for j in range(10)]
test = False
x = 0
y = 0
z = 0
itorX = 0
itorY = 0
div = 6
imgS1 = np.zeros((div,div))
imgS2 = np.zeros((div,div))
tCount = [0,0,0,0,0,0,0,0,0,0]
count = 0

def init():
    ret, imgBase = cap.read()
    print(type(imgBase))
    x, y, z = imgBase.shape
    print x, y, z
    global itorY
    global itorX
    itorY = (y / div)
    itorX = (x / div)
    
def que(pos1, thresh, val,chunkX,chunkY):
    global count
    global data
    global tcount
    pos = pos1
    print tCount,pos
    if(len(data[pos]) < 10):
        if(val):
            tCount[pos] += 1
        else:
            tCount[pos] -= 1
    else:
        if(data[pos].pop(0)):
            tCount[pos] -= 1
        else:
            tCount[pos] += 1
        if(val):
            tCount[pos] += 1
        else:
            tCount[pos] -= 1
    count += 1
    if(count == 100):
        count = 0
    if(tCount[pos] >= thresh):
        return True
    else:
        return False
    
    

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
"""
def segment(img1, img2, X, Y):
    histS1 = histS2 = 0
    count = 0
    for i in range (X, X + div):
        for j in range (Y, Y + div):
            
            endSliceX = X + div
            histS1 += cv2.calcHist([img1[X:(X+div),Y:(Y+div)]],[0],None,[256],[0,256])
            histS2 += cv2.calcHist([img2[X:(X+div),Y:(Y+div)]],[0],None,[256],[0,256])
            sc = cv2.compareHist(histS1, histS2, cv.CV_COMP_BHATTACHARYYA)
            print sc
            if(sc > 0.3):
                test = que(points, -7, True)
            else:
                test = que(points, -7, True)
    return test
"""     
    
def percisesScan(img1, img2):
    global count
    for X in range(0, itorX):
        for Y in range(0, itorY):
            #return que(results, -7, segment(img1, img2, X, Y))
            histS1 = cv2.calcHist([img1[X*div:(X+1)*div,Y*div:(Y+1)*div]],[0],None,[256],[0,256])
            histS2 = cv2.calcHist([img2[X*div:(X+1)*div,Y*div:(Y+1)*div]],[0],None,[256],[0,256])
            sc = cv2.compareHist(histS1, histS2, cv.CV_COMP_BHATTACHARYYA)
            #print sc
            return que(count, -7, sc > 0.55,X,Y)
    return False        
                    
                    
                    
def scan(img1, img2):
    print percisesScan(img1,img2)


                
init()
while(True):
    ret, frame = cap.read()
    ret, img1 = cap.read()
    ret, img2 = cap.read()
    scan(img1, img2)
        


    
    
    
    #plt.hist(frame.ravel(),256,[0,256]); plt.show()
    #img1 = cv2.imread('C:/ICP/buterfly_1.jpg')
    #img1= cv2.cvtColor(img1,cv.CV_BGR2HSV)
    #img2 = cv2.imread('C:/ICP/buterfly_0.jpg')
    #img2= cv2.cvtColor(img2,cv.CV_BGR2HSV)
    #h = np.zeros((300,256,3))
    
    #bins = np.arange(256).reshape(256,1)
    #color = [ (255,0,0),(0,255,0),(0,0,255) ]
    
    #for ch, col in enumerate(color):
        #hist_item1 = cv2.calcHist([img1],[ch],None,[256],[0,255])
        #hist_item2 = cv2.calcHist([img2],[ch],None,[256],[0,255])
        #cv2.normalize(hist_item1,hist_item1,0,255,cv2.NORM_MINMAX)
        #cv2.normalize(hist_item2,hist_item2,0,255,cv2.NORM_MINMAX)
        #sc= cv.CompareHist(hist_item1, hist_item2, cv.CV_COMP_CORREL)
        #printsc
        #hist=np.int32(np.around(hist_item))
        #pts = np.column_stack((bins,hist))
        #cv2.polylines(h,[pts],False,col)
    
    #h=np.flipud(h)
    #cv2.imwrite('C:/hist.png',h)    
    
    #print gray
    # Display the resulting frame
    cv2.imshow('frame',img1)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
        
# When everything done, release the capture
cap.release()
cv2.destroyAllWindows()