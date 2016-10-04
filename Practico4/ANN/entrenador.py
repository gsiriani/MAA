import numpy as np
import random
import inspect
import functools
from ann import Ann, Ejemplo, Funciones

class Entramiento:

    def __init__(self, red, factorDeAprendizaje):

        self.cortes = {}
        self.errores = []
        self.red = red
        self.factorDeAprendizaje = factorDeAprendizaje

class Entrenador:

    def entrenar(self, redes, iteraciones, ejemplos, fnObjetivo):

        proximoCorte = 0

        for j in range(iteraciones):

            ejemplosDeEntrenamiento = []

            for i in range(ejemplos):
                numeroParametros = len(inspect.getargspec(fnObjetivo)[0])

                x = [random.uniform(-1, 1) for p in range(numeroParametros)]
                llamada = functools.partial(fnObjetivo, *x)
                ejemplosDeEntrenamiento.append(Ejemplo(x, llamada()))

            for r in redes:

                r.red.entrenar(ejemplosDeEntrenamiento, r.factorDeAprendizaje)
                r.errores.append(sum(r.red.historia))
                r.red.historia = []

                if j == proximoCorte or j == iteraciones - 1:
                    rango = np.arange(-1, 1, 0.01)
                    r.cortes[str(proximoCorte)] = [r.red.ejecutar([p]) for p in rango]
                    proximoCorte = (proximoCorte if proximoCorte > 0 else 1) * 10

            if j % 100 == 0:
                print ("Corrida " + str(j))


        return redes


