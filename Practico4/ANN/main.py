import random
import math
import numpy as np
import matplotlib.pyplot as plt
from entrenador import Entrenador, Entramiento
from ann import Ann, Ejemplo, Funciones

redes = {}

redChicaSigmoide = Ann(1, 5, Funciones.Sigmoid, -0.5, 0.5)
redGrandeSigmoide = Ann(1, 50, Funciones.Sigmoid, -0.5, 0.5)
redChicaHiperbolica = Ann(1, 5, Funciones.Tanh, -0.5, 0.5)
redGrandeHiperbolica = Ann(1, 50, Funciones.Tanh, -0.5, 0.5)

#redes["Chica sigmoide"] = Entramiento(redChicaSigmoide,0.1)
#redes["Grande sigmoide"] = Entramiento(redGrandeSigmoide,0.1)
redes["Chica hiperbolica"] = Entramiento(redChicaHiperbolica,0.000001)
redes["Grande hiperbolica"] = Entramiento(redGrandeHiperbolica,0.000001)

entrenador = Entrenador()
fnObjetivo = lambda x: math.sin(1.5*math.pi*x)/2
#fnObjetivo = lambda x: x**2
#fnObjetivo = lambda x: x
entrenador.entrenar(redes.values(), 2000, 50, fnObjetivo)

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