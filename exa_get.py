import cv2 as cv
import os


def get(DEVICE: int, DIR: str, FILE: str):
    cam = cv.VideoCapture(DEVICE)

    cam.set(cv.CAP_PROP_FRAME_HEIGHT, 1080)
    cam.set(cv.CAP_PROP_FRAME_WIDTH, 1920)

    if not cam.isOpened():
        return False

    ret, frame= cam.read()

    cam.release()

    if ret:
        os.makedirs(DIR, exist_ok = True)
        cv.imwrite(os.path.join(DIR, FILE), frame)
        return True
    return False

if __name__ == '__main__':
    device = 2
    dirf = './NOW'
    print(get(device, dirf, 'IMAGE.jpg'))
