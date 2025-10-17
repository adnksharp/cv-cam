import yaml, os
import cv2 as cv
import numpy as np

def do(DATA: str, IN: str, OUT: str, ):
    if not os.path.exists(DATA):
        return False

    fs = cv.FileStorage(DATA, cv.FileStorage_READ)
    mtx = fs.getNode('K').mat()
    dist = fs.getNode('D').mat()
    fs.release()

    cam = cv.imread(IN)
    if cam is None:
        return False
    h, w = cam.shape[:2]
    newcam, roi = cv.getOptimalNewCameraMatrix(mtx, dist, (w, h), 1, (w, h))

    dst = cv.undistort(cam, mtx, dist, None, newcam)

    x, y, w_roi, h_roi = roi
    dst = dst[y:y+h_roi, x:x+w_roi]

    cv.imwrite(OUT, dst)
    return True


if __name__ == '__main__':
    data = 'chess.yaml'
    dirf = './NOW'
    imageIn = f'{dirf}/IMAGE.jpg'
    imageOut = f'{dirf}/FIXED.jpg'
    print(do(data, imageIn, imageOut))
