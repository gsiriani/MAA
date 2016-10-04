import random
import math
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import cm

from entrenador import Entrenador, Entramiento
from ann import Ann, Ejemplo, Funciones
from mpl_toolkits.mplot3d import Axes3D


redes = {}

redChicaSigmoide = Ann(2, 5, Funciones.Sigmoid, -0.5, 0.5)
redMedianaSigmoide = Ann(2, 20, Funciones.Sigmoid, -0.5, 0.5)
redMedianaSigmoide2 = Ann(2, 30, Funciones.Sigmoid, -0.5, 0.5)
redChicaSigmoide2 = Ann(2, 1, Funciones.Sigmoid, -0.5, 0.5)
redGrandeSigmoide = Ann(2, 50, Funciones.Sigmoid, -0.5, 0.5)
redChicaHiperbolica = Ann(2, 5, Funciones.Tanh, -3, 3)
redGrandeHiperbolica = Ann(2, 50, Funciones.Tanh, -3, 3)

redes["Logistica - 1"] = Entramiento(redChicaSigmoide2,0.01)
redes["Logistica - 5"] = Entramiento(redChicaSigmoide,0.01)
redes["Logistica - 30"] = Entramiento(redMedianaSigmoide2,0.1)
redes["Logistica - 20"] = Entramiento(redMedianaSigmoide,0.1)
redes["Logistica - 50"] = Entramiento(redGrandeSigmoide,0.1)
#redes["Tanh - 5"] = Entramiento(redChicaHiperbolica,0.01)
#redes["Grande hiperbolica"] = Entramiento(redGrandeHiperbolica,0.01)

entrenador = Entrenador()
#fnObjetivo = lambda x: math.sin(1.5*math.pi*x)/2.3 + 0.5
#fnObjetivo = lambda x: x**2
fnObjetivo = lambda x,y : 1 if x**2 + y**2 < 0.5 else 0
entrenador.entrenar(redes.values(), 100000, 40, fnObjetivo)

for k,v in redes.iteritems():
    plt.plot(v.errores, label=k)

plt.legend()
plt.show()

plt.clf()
rangoX = np.arange(-1, 1, 0.03)
rangoY = np.arange(-1, 1, 0.03)

fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
X, Y = np.meshgrid(rangoX, rangoY)
valoresRed = []

for k,v in redes.iteritems():
    zr = np.array([v.red.ejecutar([x,y]) for x,y in zip(np.ravel(X), np.ravel(Y))])
    valoresObjetivo = zr.reshape(X.shape)
    ax.plot_surface(X,Y,valoresObjetivo, rstride=1, cstride=1, cmap=cm.jet,
        linewidth=0, antialiased=True,alpha=0.3 ,label=k)

zs = np.array([fnObjetivo(x,y) for x,y in zip(np.ravel(X), np.ravel(Y))])
valoresObjetivo = zs.reshape(X.shape)
ax.plot_surface(X,Y,valoresObjetivo, rstride=1, cstride=1, cmap=cm.coolwarm,
    linewidth=0, antialiased=True,alpha=0.2,label="Funcion objetivo")

plt.show()
