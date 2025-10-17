import exa_get, exa_fix, exa_plot, exa_pos
import os
import time
import sys
import numpy as np
import cv2 as cv
import matplotlib.pyplot as plt

ID = 2
DIR = './NOW'
CFILE = 'chess.yaml'
ORIGINAL = 'IMAGE.jpg'
FIXED = 'FIXED.jpg'
OUTDATA = 'now.yaml'
OUTIMG = f'{DIR}/CHESS.jpg'
SLEEP = 0.5

ODIR = os.path.join(DIR, ORIGINAL)
FDIR = os.path.join(DIR, FIXED)

fig = plt.figure(figsize=(18, 8))
ax3d = fig.add_subplot(1, 2, 1, projection='3d')
ax2d = fig.add_subplot(1, 2, 2)
plt.ion()
plt.show(block=False) 

pos = [np.array([[0.0], [0.0], [0.0]])]
rot = [np.eye(3)]
hist = [0.0]


if __name__ == '__main__':
    os.makedirs(DIR, exist_ok=True)
    
    try:
        while True:
            run = time.time()
            
            if not exa_get.get(ID, DIR, ORIGINAL):
                time.sleep(SLEEP)
                continue

            if not exa_fix.do(CFILE, ODIR, FDIR):
                time.sleep(SLEEP)
                continue

            if exa_pos.set(CFILE, FDIR, OUTDATA, OUTIMG):
                try:
                    fs = cv.FileStorage(OUTDATA, cv.FILE_STORAGE_READ)
                    rvecs = fs.getNode("rvecs").mat()
                    tvecs = fs.getNode("tvecs").mat()
                    fs.release()

                    if rvecs is not None and tvecs is not None:
                        Rot, Trans = exa_plot.calc(rvecs, tvecs)
                        
                        newPos = Trans.flatten()
                        oldPos = pos[-1].flatten()
                        
                        if not np.allclose(newPos, oldPos):
                            pos.append(Trans)
                            rot.append(Rot)
                            hist.append(run)
                            
                            exa_plot.update(pos, fig, ax3d, ax2d, hist) 

                except Exception as e:
                    continue
            
            times = time.time() - run
            sleep = max(0, SLEEP - times)
            time.sleep(sleep)

    except KeyboardInterrupt:
        fig.savefig('graph.pdf', bbox_inches='tight')
        plt.close(fig) 
        sys.exit(0)
