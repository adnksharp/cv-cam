import yaml, os
import cv2 as cv
import numpy as np

if __name__ == '__main__':
    data = 'chess.yaml'
    dirf = './NOW'
    imageIn = f'{dirf}/IMAGE.jpg'
    imageOut = f'{dirf}/FIXED.jpg'
    if not os.path.exists(data):
        exit(1)
    
    fs = cv.FileStorage(data, cv.FileStorage_READ)
    mtx = fs.getNode('K').mat()
    dist = fs.getNode('D').mat()

    try:
        cam = cv.imread(imageIn)
        h, w = cam.shape[:2]

    except:
        pass

    newcam, roi = cv.getOptimalNewCameraMatrix(mtx, dist, (w,h), 1, (w,h))

    dst = cv.undistort(cam, mtx, dist, None, newcam)
 
    x, y, w, h = roi
    dst = dst[y:y+h, x:x+w]
    cv.imwrite(imageOut, dst)
