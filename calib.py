import numpy as np
import cv2 as cv
import glob, yaml, os, sys
from progress.bar import IncrementalBar

if __name__ == '__main__':
    criteria = (cv.TERM_CRITERIA_EPS + cv.TERM_CRITERIA_MAX_ITER, 80, 0.001)
    boardSize = (48, 33)
    objPoints, imgPoints = [], []
    objP = np.zeros((boardSize[1] * boardSize[0], 3), np.float32)
    objP[:, :2] = np.mgrid[0:boardSize[0], 0:boardSize[1]].T.reshape(-1, 2) * 4

    ext = '*.jpg'
    imgDir = glob.glob(f'./*IMG/{ext}')

    out = 'ChessBoard'
    os.makedirs(out, exist_ok=True)
    
    if not imgDir:
        exit(0)

    imgsUsed = []
    imgSize = None
    
    bar = IncrementalBar('Processing', max=len(imgDir))
    i = 0
    for _ in imgDir:
        img = cv.imread(_)
        imgGray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
        imgSize = (imgGray.shape[1], imgGray.shape[0])
        ret, corners = cv.findChessboardCorners(imgGray, boardSize, None)

        if not ret: 
            i += 1
            try:
                os.remove(_)
            except OSError as e:
                continue
        else:
            corners2 = cv.cornerSubPix(imgGray, corners, (11, 11), (-1, -1), criteria)
            imgPoints.append(corners2)
            objPoints.append(objP)
            cv.drawChessboardCorners(img, boardSize, corners2, ret)

            cv.imwrite(os.path.join(out, os.path.basename(_)) , img)

        bar.goto(imgDir.index(_))

    rms, K, D, rvecs, tvecs = cv.calibrateCamera(objPoints, imgPoints, imgSize, None, None)
    
    file = cv.FileStorage('chess.yaml', cv.FILE_STORAGE_WRITE)
    
    file.write('rms', rms)
    file.write('K', K)
    file.write('D', D)
    file.write('rvecs', np.concatenate(rvecs, axis=1))
    file.write('tvecs', np.concatenate(tvecs, axis=1))

    file.release()
    bar.finish()
    print(f'err {i} / {len(imgDir)}')
