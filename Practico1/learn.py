# -*- coding: UTF-8 -*-

import random
import math

from damas import Damas,Turno,Casilla

class Representacion():

    size = 2

    @staticmethod
    def obtener(tablero):

        flattened = [casilla for fila in tablero for casilla in fila]

        return sum([1 for c in flattened if c == Casilla.BLANCA]),sum([1 for c in flattened if c == Casilla.NEGRA])

class Learner():

    MAX_INITIAL_WEIGHT = 10
    MIN_INITIAL_WEIGHT = -10

    victorias = 0
    empates = 0
    jugadasTotales = 0

    def __init__(self, representacion, factorAprendizaje):

        self.representacion = representacion
        random.seed()
        self.weights = tuple(random.uniform(self.MIN_INITIAL_WEIGHT, self.MAX_INITIAL_WEIGHT)
                             for i in range(representacion.size + 1))
        self.factorAprendizaje = factorAprendizaje

    def run(self, iterations):

        print ("Iniciando ejecución")

        for i in range(iterations):
            self.siguienteIteracion()
            if i % 100 == 0:
                print(str(i) + " iteraciones")

        print ("Ejecución terminada.")
        print ("Partidas realizadas: " + str(iterations))
        print ("Victorias: " + str(self.victorias) + " ("  + str(float(self.victorias) / iterations * 100) + "%)")
        print ("Empates: " + str(self.empates) + " (" + str(float(self.empates) / iterations * 100) + "%)")
        print ("Jugadas realizadas: " + str(self.jugadasTotales))
        print ("Pesos: " + str(self.weights))

    def generarTableroInicial(self):

        return Damas.tablero_base()

    def valorTablero(self, representacion, damas):

        if damas.partidaTerminada():
            return self.valorTableroFinal(damas.tablero)

        # TODO: Incoporar el último peso
        valor = sum([x * y for x, y in zip(representacion,self.weights)]) # + representacion[len(representacion)-1]

        assert not math.isinf(valor)

        return valor

    def valorTableroFinal(self, tablero):

        flattened = [casilla for fila in tablero for casilla in fila]

        cantidadBlancas = sum([1 for c in flattened if c == Casilla.BLANCA])
        cantidadNegras = sum([1 for c in flattened if c == Casilla.NEGRA])

        return 0 if cantidadNegras == cantidadBlancas else (100 if cantidadBlancas > cantidadNegras else -100)

    def aplicarAprendizaje(self, decisiones, valorFinal):

        weights = list(self.weights)

        # TODO: Aprender sobre el bias

        for i,decision in enumerate(decisiones):
            for j,w in enumerate(weights):

                if(j < len(weights) - 1):
                    valorEntrenamiento = decisiones[i+1].valor if i+1 < len(decisiones) else valorFinal

                    weights[j] = w + self.factorAprendizaje * decision.representacion[j] * \
                                     (valorEntrenamiento - decision.valor)

                assert not math.isnan(weights[j]) and not math.isinf(weights[j])


        return tuple(weights)

    def siguienteIteracion(self):

        decisiones = []

        damas = Damas(self.generarTableroInicial(),random.choice([Turno.BLANCA,Turno.NEGRA]))

        colorFichas = damas.turno

        while not damas.partidaTerminada():

            resultados = []

            for m in damas.movimientosValidosCalculados:
                resultado = Resultado()
                resultado.damas = damas.obtenerTableroResultante(m)
                resultado.representacion = self.representacion.obtener(resultado.damas.tablero)
                resultado.valor = self.valorTablero(resultado.representacion,resultado.damas)

                resultados.append(resultado)

            if damas.turno == Turno.BLANCA:
                mejorResultado = max(resultados, key= lambda r: r.valor)
            else:
                mejorResultado = min(resultados, key=lambda r: r.valor)

            mejoresResultados = [r for r in resultados if r.valor == mejorResultado.valor]
            resultadoElegido = random.choice(mejoresResultados)

            if colorFichas == damas.turno:
                decisiones += [resultadoElegido]

            damas = resultadoElegido.damas

        valorFinal = self.valorTablero(None,damas)
        self.weights = self.aplicarAprendizaje(decisiones, valorFinal)
        self.jugadasTotales += len(decisiones)

        # TODO: Contar empates
        if valorFinal == (100 * (1 if damas.turno == Turno.BLANCA else -1)):
            self.victorias += 1
        elif valorFinal == 0:
            self.empates += 1

class Resultado:

    damas = None
    representacion = None
    valor = None

