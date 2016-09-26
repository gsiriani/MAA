import random
import math

class Funciones:

    @staticmethod
    def Sigmoid(x):
        return 1 / (1 + math.pow(math.e,-x))

class Ejemplo:

    def __init__(self, entrada, salidaEsperada):
        self.entrada = entrada
        self.salidaEsperada = salidaEsperada

class Ann:

    def __init__(self, cantidadEntrada, cantidadOculta, funcionActivacion, min, max):
        self.capaOculta = [Neurona(cantidadEntrada, funcionActivacion, min, max) for i in range(cantidadOculta)]
        self.neuronaSalida = Neurona(cantidadOculta, funcionActivacion, min, max)
        self.historia = []


    def entrenar(self, ejemplos, factorAprendizaje):

        for e in ejemplos:

            self.ejecutar(e.entrada)
            self.aplicarBackpropagation(e.salidaEsperada, factorAprendizaje)

    def ejecutar(self, entrada):

        salidaOculta = []

        for n in self.capaOculta:
            n.disparar(entrada)
            salidaOculta.append(n.salida)

        self.neuronaSalida.disparar(salidaOculta)

        return self.neuronaSalida.salida

    def aplicarBackpropagation(self, salidaEsperada, factorAprendizaje):

        valorSalida = self.neuronaSalida.salida

        errorSalida = valorSalida * (1 - valorSalida) * (salidaEsperada - valorSalida)
        self.historia.append(abs(errorSalida))

        # Calculo error de las neuronas de la capa oculta
        for i in range(len(self.capaOculta)):

            n = self.capaOculta[i]
            pesoSalidaN = self.neuronaSalida.pesos[i]

            errorOculta = n.salida * (1 - n.salida) * pesoSalidaN * errorSalida

            # Actualizo pesos de la neurona de la capa oculta
            for j in range(len(n.pesos)):
                peso = n.pesos[j]
                n.pesos[j] = peso + factorAprendizaje * errorOculta * n.entrada[j]

        # Actualizo pesos de la neurona de salida
        for j in range(len(self.neuronaSalida.pesos)):
            peso = self.neuronaSalida.pesos[j]
            salidaOculta = self.capaOculta[j].salida if j < len(self.neuronaSalida.pesos) - 1 else 1
            self.neuronaSalida.pesos[j] = peso + factorAprendizaje * errorSalida * salidaOculta


class Neurona:

    def __init__(self, cantidadEntradas, fn, min, max):
        self.salida = 0
        self.entrada = []
        self.fn = fn
        self.pesos = [random.uniform(min, max) for i in range(cantidadEntradas + 1)]

    def disparar(self, valores):
        self.entrada = valores
        self.entrada.append(1)
        ponderados = [v[0]*v[1] for v in zip(valores, self.pesos)]
        suma = sum(ponderados)

        self.salida = self.fn(suma)


