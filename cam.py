import numpy as np
import cv2
import cv
import datetime

cap = cv2.VideoCapture(1)
results = []
tCount = 0

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
    
    x, y, z = img2.shape
    histS1 = histS2 = 0
    count = 0
    for i in range (0,x):
        for j in range (0,y):
            count += 1
            histS1 += cv2.calcHist([img1[(i,j)]],[0],None,[256],[0,256])
            histS2 += cv2.calcHist([img2[(i,j)]],[0],None,[256],[0,256])
            if(count == 100):
                sc = cv2.compareHist(histS1, histS2, cv.CV_COMP_BHATTACHARYYA)
                if(sc > 0.3):
                    return True
                else:
                    return False                
                

while(True):
    ret, frame = cap.read()
    ret, img1 = cap.read()
    ret, img2 = cap.read()
    if(img2 is None):
        break
    r = (overallScan(img1, img2))
    if(len(results) < 10):
        if(r):
            tCount += 1
        else:
            tCount -= 1
    else:
        if(results.pop(0)):
            tCount -= 1
        else:
            tCount += 1
        if(r):
            tCount += 1
        else:
            tCount -= 1
    results.append((overallScan(img1, img2)))
    if(tCount >= -7):
        print(True)
    else:
        print(False)
        


    
    
    
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