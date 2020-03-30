from dronekit import *
import math
from routes import getMultiHelix, getMultiFacade, getHelix, getFacade, getHelixinCoords
import numpy as np


def writeSimpleHelixMission(hmin, sep, nWPperCircle, bufferD, perimeter, filename):
    filename = filename + ".txt"
    file = open(str(filename), "w")
    file.write("QGC WPL 110\n")
    alpha = (2*np.pi)/nWPperCircle #rad
    x,y,z,theta = getHelix(sep, bufferD, perimeter)
    C = perimeter.C
    xf,yf,zf = getHelixinCoords(x,y,z,C)
    file.write("0 1 0 16 0 0 0 0 " + str(xf[0]) + " " + str(yf[0]) + " " + str(round(zf[0],2)) + " " + "1\n")
    i = 0
    j = 0
    rpm = 0
    while (j < len(xf)):
        if(round(alpha*i,1) == round(theta[j],1) or round(alpha*i,1) == round(theta[j] - (2*np.pi*rpm),1) or round(alpha*i,1) + 0.1 == round(theta[j],1) or round(alpha*i,1) - 0.1 == round(theta[j],1)):
            file.write(str(i + 1) +  " 0 10 82 0 0 0 0 " + str(xf[j]) + " " + str(yf[j]) + " " + str(round(zf[j],2)) + " " + "1\n")
            i = i + 1
        if(round(theta[j] - (2*np.pi*(rpm + 1))) == 0):
            rpm = rpm + 1
        j = j + 1

    #Añadimos el perimetro para comprobar (eliminar luego)
    file.write(str(i) +  " 0 10 16 0 0 0 0 " + str(perimeter.c1[0]) + " " + str(perimeter.c1[1]) + " " + str(0) + " " + "1\n")
    file.write(str(i + 1) +  " 0 10 16 0 0 0 0 " + str(perimeter.c2[0]) + " " + str(perimeter.c2[1]) + " " + str(0) + " " + "1\n")
    file.write(str(i + 2) +  " 0 10 16 0 0 0 0 " + str(perimeter.c3[0]) + " " + str(perimeter.c3[1]) + " " + str(0) + " " + "1\n")
    file.write(str(i + 3) +  " 0 10 16 0 0 0 0 " + str(perimeter.c4[0]) + " " + str(perimeter.c4[1]) + " " + str(0) + " " + "1\n")
    file.close()

def writeSimpleFacadeMission(sep, bufferD, wall, ori, filename):
    filename = filename + ".txt"
    file = open(str(filename), "w")
    file.write("QGC WPL 110\n")
    x,y,z = getFacade(sep,bufferD,wall,ori)
    j = 0
    while (j < len(x)):
        file.write(str(j + 1) +  " 0 10 16 0 0 0 0 " + str(x[j]) + " " + str(y[j]) + " " + str(round(z[j],2)) + " " + "1\n")
        j = j + 1
    
    #Añadimos la pared para comprobar (eliminar luego)
    file.write(str(j) +  " 0 10 16 0 0 0 0 " + str(wall.c1[0]) + " " + str(wall.c1[1]) + " " + str(0) + " " + "1\n")
    file.write(str(j + 1) +  " 0 10 16 0 0 0 0 " + str(wall.c2[0]) + " " + str(wall.c2[1]) + " " + str(0) + " " + "1\n")
    file.close()

def writeMultiFacadeMission(sep,bufferD,walls,ori,filename):
    filename = filename + ".txt"
    file = open(str(filename), "w")
    file.write("QGC WPL 110\n")
    x,y,z = getMultiFacade(sep,bufferD,walls,ori)
    j = 0
    while (j < len(x)):
        file.write(str(j + 1) +  " 0 10 16 0 0 0 0 " + str(x[j]) + " " + str(y[j]) + " " + str(round(z[j],2)) + " " + "1\n")
        j = j + 1
    
    #Añadimos la pared para comprobar (eliminar luego)
    i = 0
    while (i < len(walls)):
        wall = walls[i]
        file.write(str(j) +  " 0 10 16 0 0 0 0 " + str(wall.c1[0]) + " " + str(wall.c1[1]) + " " + str(0) + " " + "1\n")
        j = j + 1
        i = i + 1

def writeMultiHelixMission(sep,bufferD,bufferH,nWPperCircle,perimeters,filename):
    filename = filename + ".txt"
    file = open(str(filename), "w")
    file.write("QGC WPL 110\n")
    alpha = (2*np.pi)/nWPperCircle #rad
    x,y,z,theta = getMultiHelix(sep, bufferD,bufferH, perimeters)
    perimeters.sort()
    C = perimeters[0].C
    xf,yf,zf = getHelixinCoords(x,y,z,C)
    xf = xf[::-1]
    yf = yf[::-1]
    zf = zf[::-1]
    file.write("0 1 0 22 0 0 0 0 0 0 " + str(round(zf[0] + 2,2)) + " " + "1\n")
    file.write("1 0 10 16 0 0 0 0 " + str(xf[0]) + " " + str(yf[0]) + " " + str(round(zf[0] + 2,2)) + " " + "1\n")
    i = 0
    j = 0
    r = 0
    h = 1
    rpm = 0
    while (j < len(xf)):
        if(round(alpha*r,1) == round(theta[j],1) or round(alpha*r,1) == round(theta[j] - (2*np.pi*rpm),1) or round(alpha*r,1) + 0.1 == round(theta[j],1) or round(alpha*r,1) - 0.1 == round(theta[j],1)):
            file.write(str(i + 2) +  " 0 10 82 0 0 0 0 " + str(xf[j]) + " " + str(yf[j]) + " " + str(round(zf[j],2)) + " " + "1\n")
            i = i + 1
            r = r + 1
        if(round(theta[j] - (2*np.pi*(rpm + 1))) == 0):
            rpm = rpm + 1
        if(j == 199*h):
            file.write(str(i + 2) +  " 0 10 16 0 0 0 0 " + str(xf[j + 1]) + " " + str(yf[j + 1]) + " " + str(round(zf[j + 1],2)) + " " + "1\n")
            file.write(str(i + 3) +  " 0 10 16 0 0 0 0 " + str(xf[j + 2]) + " " + str(yf[j + 2]) + " " + str(round(zf[j + 2],2)) + " " + "1\n")
            r = 0
            h = h + 1
            i = i + 1
            j = j + 1

        j = j + 1

    file.write(str(i + 2) + " 0 10 16 0 0 0 0 " + str(xf[-1]) + " " + str(yf[-1]) + " " + str(round(zf[0] + 2,2)) + " " + "1\n")
    file.write(str(i + 3) + " 0 10 20 0 0 0 0 " + str(xf[-1]) + " " + str(yf[-1]) + " " + str(round(zf[0] + 2,2)) + " " + "1\n")
    file.write(str(i + 4) + " 0 10 21 0 0 0 0 0 0 0 1\n")
    file.close()