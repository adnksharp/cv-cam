import cv2
import os
from datetime import datetime
from tabulate import tabulate

args = {attr: getattr(cv2, attr) for attr in dir(cv2) if attr.startswith('CAP')}

if __name__ == '__main__':
    for idx in range(2, 10):
        cap = cv2.VideoCapture(idx)
        if cap.isOpened():
            cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 1080)
            cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1920)
            print(f"\n/dev/video{idx} open.")

            while True:
                ret, frame = cap.read()
                if not ret:
                    print(f"/dev/video{idx} frame err.")
                    break

                tab = []
                for name, prop_id in sorted(args.items(), key=lambda x: x[1]):
                    if cap.get(prop_id) > 0:
                        tab.append([f'{name}', f'{cap.get(prop_id)}'])
            
                print(tabulate(tab))
                cv2.imshow(f"video{idx}", frame)
                key = cv2.waitKey(1) & 0xFF
                if key == ord('q'):
                    break
                now = datetime.now()
                folder = now.strftime("%y%m%d") + "IMG"
                if not os.path.exists(folder):
                    os.makedirs(folder)
                fname = now.strftime("%H%M%S%f")[:-3]  # HHMMSSsss

                img_path = os.path.join(folder, f"{fname}.jpg")
                cv2.imwrite(img_path, frame)

                folder = now.strftime("%y%m%d") + "INF"
                if not os.path.exists(folder):
                    os.makedirs(folder)
                txt_path = os.path.join(folder, f"{fname}.txt")
                with open(txt_path, "w", encoding="utf-8") as f:
                    f.write(str(tab))
                print(f"Guardado: {img_path}, {txt_path}")

            cap.release()
            cv2.destroyAllWindows()
            exit(0)
        else:
            print(f"/dev/video{idx} fail.")

    cv2.destroyAllWindows()
