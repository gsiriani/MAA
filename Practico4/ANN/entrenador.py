import random
import inspect
import functools
from ann import Ann, Ejemplo, Funciones

class Entramiento:

    def __init__(self, red, factorDeAprendizaje):

        self.errores = []
        self.red = red
        self.factorDeAprendizaje = factorDeAprendizaje

class Entrenador:

    def entrenar(self, redes, iteraciones, ejemplos, fnObjetivo):

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

            if j % 100 == 0:
                print ("Corrida " + str(j))

        return redes
