import random
import math
import numpy as np
import matplotlib.pyplot as plt
from entrenador import Entrenador, Entramiento
from ann import Ann, Ejemplo, Funciones

redes = {}

redChicaSigmoide = Ann(1, 5, Funciones.Sigmoid, -0.5, 0.5)
redMedianaSigmoide = Ann(1, 20, Funciones.Sigmoid, -0.5, 0.5)
redMedianaSigmoide2 = Ann(1, 30, Funciones.Sigmoid, -0.5, 0.5)
redChicaSigmoide2 = Ann(1, 1, Funciones.Sigmoid, -0.5, 0.5)
redGrandeSigmoide = Ann(1, 50, Funciones.Sigmoid, -0.5, 0.5)
redChicaHiperbolica = Ann(1, 5, Funciones.Tanh, -3, 3)
redGrandeHiperbolica = Ann(1, 50, Funciones.Tanh, -5, 5)

redes["Logistica - 1"] = Entramiento(redChicaSigmoide2,0.01)
redes["Logistica - 5"] = Entramiento(redChicaSigmoide,0.01)
redes["Logistica - 30"] = Entramiento(redMedianaSigmoide2,0.1)
redes["Logistica - 20"] = Entramiento(redMedianaSigmoide,0.1)
redes["Logistica - 50"] = Entramiento(redGrandeSigmoide,0.1)
#redes["Tanh - 5"] = Entramiento(redChicaHiperbolica,0.01)
#redes["Tanh - 50"] = Entramiento(redGrandeHiperbolica,0.01)

entrenador = Entrenador()
#fnObjetivo = lambda x: math.sin(1.5*math.pi*x)/2.3 + 0.5
fnObjetivo = lambda x: x**2
#fnObjetivo = lambda x,y : 1 if x**2 + y**2 < 0.5 else 0
entrenador.entrenar(redes.values(), 100000, 40, fnObjetivo)

for k,v in redes.iteritems():
    plt.plot(v.errores, label=k)

plt.legend()
plt.show()

plt.clf()
rango = np.arange(-1, 1, 0.01)

for k,v in redes.iteritems():
    valoresRed = [v.red.ejecutar([p]) for p in rango]
    plt.plot(rango, valoresRed, label=k)
    print("*** Red: " + k + " ***")
    print("Salida: " + str(v.red.neuronaSalida.pesos))

valoresObjetivo = [fnObjetivo(p) for p in rango]
plt.plot(rango, valoresObjetivo, label="Funcion objetivo")

plt.legend()
plt.show()

for k,v in redes.iteritems():
    plt.clf()
    for nombreCorte, corte in v.cortes.iteritems():
        plt.plot(rango, corte, label=nombreCorte)
    plt.plot(rango, valoresObjetivo, label="Funcion objetivo")


plt.legend()
plt.show()