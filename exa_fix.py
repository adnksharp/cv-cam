import yaml, os
import cv2 as cv
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

data = 'chess.yaml'
dirf = './NOW'
imageIn = f'{dirf}/IMAGE.jpg'
imageOut = f'{dirf}/FIXED.jpg'

if __name__ == '__main__':
    if not os.path.exists(data):
        exit(1)
    
    fs = cv.FileStorage(data, cv.FileStorage_READ)
    mtx = fs.getNode('K').mat()
    dist = fs.getNode('D').mat()

    cam = cv.imread(imageIn)
    h, w = cam.shape[:2]

    newcam, roi = cv.getOptimalNewCameraMatrix(mtx, dist, (w,h), 1, (w,h))
    
    mapx, mapy = cv.initUndistortRectifyMap(mtx, dist, None, newcam, (w,h), 5)
    dst = cv.remap(cam, mapx, mapy, cv.INTER_LINEAR)

    x, y, w, h = roi
    dst = dst[y:y+h, x:x+w]
    cv.imwrite(imageOut, dst)
