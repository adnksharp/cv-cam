import numpy as np
import cv2 as cv
import glob, yaml, os, sys

def set(DATA: str, FILE: str, OUT_DATA: str, OUT_IMG: str):
    criteria = (cv.TERM_CRITERIA_EPS + cv.TERM_CRITERIA_MAX_ITER, 80, 0.001)
    boardSize = (48, 33)
    objP = np.zeros((boardSize[1] * boardSize[0], 3), np.float32)
    objP[:, :2] = np.mgrid[0:boardSize[0], 0:boardSize[1]].T.reshape(-1, 2) * 4

    fs = cv.FileStorage(DATA, cv.FileStorage_READ)
    mtx = fs.getNode('K').mat()
    dist = fs.getNode('D').mat()
    fs.release()

    cam = cv.imread(FILE)
    if cam is None:
        return False
    gray = cv.cvtColor(cam, cv.COLOR_BGR2GRAY)

    ret, corners = cv.findChessboardCorners(gray, boardSize, None)
    if not ret:
        return False

    corners2 = cv.cornerSubPix(gray, corners, (11, 11), (-1, -1), criteria)
    ret_pnp, rvec, tvec = cv.solvePnP(objP, corners2, mtx, dist)
    if not ret_pnp:
        return False

    file = cv.FileStorage(OUT_DATA, cv.FILE_STORAGE_WRITE)
    file.write('rvecs', rvec)
    file.write('tvecs', tvec)
    file.release()

    cv.drawChessboardCorners(cam, boardSize, corners2, ret)
    cv.imwrite(OUT_IMG, cam)
    return True

if __name__ == '__main__':
    image = './NOW/FIXED.jpg'
    out = './NOW/CHESS.jpg'
    data = 'chess.yaml'
    now = 'now.yaml'
    print(get(data, image, now, out))
