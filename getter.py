import cv2, yaml, os
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

file = "chess.yaml"
out = "cam.yaml"
pos = []
rot = []

if __name__ == '__main__':
    if not os.path.exists(file):
        exit(1)
    
    fs = cv2.FileStorage(file, cv2.FileStorage_READ)
    # rms = fs.getNode("rms").real()
    # K = fs.getNode("K").mat()
    # D = fs.getNode("D").mat()
    rvecs = fs.getNode("rvecs").mat()
    tvecs = fs.getNode("tvecs").mat()
    fs.release()
    
    for i in range(len(rvecs[0])):
        vrot = rvecs[:, i]
        Trans = tvecs[:, i]
        Rot, _ = cv2.Rodrigues(vrot)
        """
        MTH = np.eye(4)
        MTH[:3, :3] = Rot
        MTH[:3, 3] = Trans
        """

        RotT = Rot.T
        TransT = -Rot.T @ Trans
        """
        MTHT = np.eye(4)
        MTHT[:3, :3] = RotT
        MTHT[:3, 3] = TransT
        """
        
        rot.append(RotT)
        pos.append(Trans)
    
    plotter = np.array(pos)
    X = plotter[:, 0]
    Y = plotter[:, 1]
    Z = plotter[:, 2]

    fig = plt.figure(figsize=(10, 8))
    ax = fig.add_subplot(111, projection='3d')

    #ax.plot(X, Y, Z)
    ax.scatter(X, Y, Z, c=Z, cmap='viridis', marker='o')
    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.set_zlabel('Z')
    
    plt.show()
