import cv2 as cv
import numpy as np
import matplotlib.pyplot as plt
import os
import time
import sys

def calc(rvec, tvec):
    r, _ = cv.Rodrigues(rvec)
    Rot = r.T
    Trans = -Rot @ tvec 
    Trans[0, 0] = -Trans[0, 0]
    Trans[2, 0] = -Trans[2, 0]

    return Rot, Trans

def update(history, fig, ax3d, ax2d, pltHist):
    plotter = np.array(history).squeeze()
    
    if plotter.ndim == 1 and plotter.size == 3: 
        X, Y, Z = plotter[0], plotter[1], plotter[2]
        ONS = True
    elif plotter.ndim > 1:
        X, Y, Z = plotter[:, 0], plotter[:, 1], plotter[:, 2]
        ONS = False
    else:
        return

    ax3d.cla()
    ax3d.set_title('Trayectoria')
    ax3d.set_xlabel('X')
    ax3d.set_ylabel('Y')
    ax3d.set_zlabel('Z')
    ax3d.grid(True)
    
    if ONS or len(history) <= 2:
        ax3d.scatter(X, Y, Z, c='r', marker='o', label='Posición')
        if not ONS:
            ax3d.plot(X, Y, Z, 'b-', label='Trayectoria')

        if ONS:
            CX, CY, CZ = X, Y, Z
        else:
            CX, CY, CZ = X[-1], Y[-1], Z[-1]
        
        margin = 200.0 
        ax3d.set_xlim(CX - margin, CX + margin)
        ax3d.set_ylim(CY - margin, CY + margin)
        ax3d.set_zlim(CZ - margin, CZ + margin)
        
    else:
        ax3d.plot(X, Y, Z, 'b-', label='Trayectoria') 
        ax3d.scatter(X, Y, Z, c=Z, cmap='viridis', marker='o', label='Ubicación') 
    
        rxnge = np.array([X.max()-X.min(), Y.max()-Y.min(), Z.max()-Z.min()]).max() / 2.0
        
        if rxnge < 50.0: rxnge = 50.0 
            
        MX = (X.max()+X.min()) * 0.5
        MY = (Y.max()+Y.min()) * 0.5
        MZ = (Z.max()+Z.min()) * 0.5
        ax3d.set_xlim(MX - rxnge, MX + rxnge)
        ax3d.set_ylim(MY - rxnge, MY + rxnge)
        ax3d.set_zlim(MZ - rxnge, MZ + rxnge)

    if len(history) > 1:
        T = np.array(pltHist)
        T_norm = T - T[0]

        DATA = np.array(history).squeeze()
        X2D = DATA[:, 0]
        Y2D = DATA[:, 1]
        Z2D = DATA[:, 2]

        ax2d.cla() 
        ax2d.set_title('Posiciones')
        ax2d.set_xlabel('Tiempo')
        ax2d.set_ylabel('Posición')
        ax2d.grid(True)

        ax2d.plot(T_norm, X2D, label='X', color='r')
        ax2d.plot(T_norm, Y2D, label='Y', color='g')
        ax2d.plot(T_norm, Z2D, label='Z', color='b')
        ax2d.legend()
        
        p2d = np.concatenate([X2D, Y2D, Z2D])
        min2D, max2D = p2d.min(), p2d.max()
        padding = (max2D - min2D) * 0.1
        ax2d.set_ylim(min2D - padding, max2D + padding)

    fig.canvas.draw_idle() 
    fig.canvas.flush_events()
    plt.pause(0.01)

