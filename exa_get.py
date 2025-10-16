import cv2 as cv
import os

device = 2
dirf = './NOW'

if __name__ == '__main__':
    os.makedirs(dirf, exist_ok=True)
    cam = cv.VideoCapture(device)
    cam.set(cv.CAP_PROP_FRAME_HEIGHT, 1080)
    cam.set(cv.CAP_PROP_FRAME_WIDTH, 1920)

    if cam.isOpened():
        print('RUNING...')
        while True:
            ret, frame = cam.read()
            cv.imwrite(os.path.join(dirf, f'IMAGE.jpg'), frame)
        cv.release()
    cv.destroyAllWindows()
