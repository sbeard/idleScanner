import cv2
import imutils
import numpy as np  
from matplotlib import pyplot as plt


corpse = cv2.imread("img/star5/corpsedemon.png")
lutz = cv2.imread("img/star5/lutz.png")
kamath = cv2.imread("img/star5/kamath.png")
#template = cv2.imread("kamath.png")  

HEROSIZE=corpse.shape[0]

img = cv2.imread("tst_img.png")  

#grayimg = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
#graylutz = cv2.cvtColor(corpse, cv2.COLOR_BGR2GRAY)

class Match:
    def __init__(self, result, maxconf, coor):
        self.result = result
        self.maxconf = maxconf
        self.coor = coor

def sameRegion(v, n):
    # Return true if (v)alue and (n)ew are within 5 pixels of each other
    return (v[0]-5 < n[0] < v[0]+5) & (v[1]-5 < n[1] < v[1]+5)

def combMatches(l):
    i = 1
    nl = l.copy()
    res = list()
    while(nl):
        res.append(nl[0])
        nl = [x for x in nl if not sameRegion(nl[0], x)]
    #import pdb; pdb.set_trace()
    return res 


def getMatches(img, template):
    result = cv2.matchTemplate(img, template, cv2.TM_CCOEFF_NORMED)  
    _, conf, _, _ = cv2.minMaxLoc(result) 
    confidence = 0.7
    y = list(zip(*np.where(result >= confidence)))
    y2 = [t[::-1] for t in y]
    # The match will give lots of close nearby matches, round the
    # the coordinates to nearest 10 to combine them for a better count
    #y3 = list(set([ (a - a%10, b - b%10) for a,b in y2]))
    y3 = combMatches(y2)
    return Match(result, conf, y3)

def markMatches(coor, img, color=(255,0,0)):
    for x in m.coor:
        img = cv2.rectangle(img, x, (x[0] + HEROSIZE, x[1]+ HEROSIZE), color, 10)


def show(img):
    plt.imshow(img)
    plt.show()

img2 = img.copy()

m = getMatches(img, corpse)
#markMatches(m.coor, img2, (255,0,0))
print("5* Corpsedemon: ", len(m.coor))

m = getMatches(img, lutz)
#markMatches(m.coor, img2, (0,255,0))
print("5* Lutz: ", len(m.coor))

m = getMatches(img, kamath)
#markMatches(m.coor, img2, (255,255,255))
print("5* Kamath: ", len(m.coor))

#img2 = cv2.cvtColor(img2, cv2.COLOR_BGR2RGB)
#show(img2)
