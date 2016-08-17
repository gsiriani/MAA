# -*- coding: UTF-8 -*-

import math
import random

from damas import Damas, Turno


class Learner():

    victorias = 0
    empates = 0
    perdidas = 0
    jugadasTotales = 0

    maquinaA = None
    maquinaB = None

    def __init__(self, maquinaA, maquinaB, factorAprendizaje, aplicarAprendizajeAAmbasMaquinas):

        self.maquinaA = maquinaA
        self.maquinaB = maquinaB
        self.aplicarAprendizajeAAmbasMaquinas = aplicarAprendizajeAAmbasMaquinas
        self.magnitudesPesos = [0 for i in range(maquinaA.representacion.size + 1)]
        random.seed()

        self.factorAprendizaje = factorAprendizaje

    def run(self, iterations, sinAprendizaje = False):

        print ("Iniciando ejecución")

        for i in range(iterations):
            if i % 1000 == 0:
                print(str(i) + " iteraciones.")
                # print ("A" + str(self.maquinaA.weights))
                # print ("B" + str(self.maquinaB.weights))

            self.siguienteIteracion(sinAprendizaje)

        print ("Ejecución terminada.")
        print ("Partidas realizadas: " + str(iterations))
        print ("Victorias: " + str(self.victorias) + " ("  + str(float(self.victorias) / iterations * 100) + "%)")
        print ("Empates: " + str(self.empates) + " (" + str(float(self.empates) / iterations * 100) + "%)")
        print ("Perdidas: " + str(self.perdidas) + " (" + str(float(self.perdidas) / iterations * 100) + "%)")
        print ("Jugadas realizadas: " + str(self.jugadasTotales))
        print ("Pesos: " + str(self.maquinaA.weights))

        sumaMagnitudes = sum(self.magnitudesPesos)

        print "Pesos relativos" + str([(float(p) / sumaMagnitudes)*100 for p in self.magnitudesPesos])

    def generarTableroInicial(self):

        tableroGenerado = False
        nroJugadas = random.randint(0, 15)

        while not tableroGenerado:

            damas = Damas(Damas.tablero_base(), random.choice([Turno.BLANCA, Turno.NEGRA]))

            for i in range(nroJugadas):
                movimientoAlAzar = random.choice(damas.movimientosValidosCalculados)
                damas = damas.obtenerTableroResultante(movimientoAlAzar)

                if damas.partidaTerminada():
                    break

            if not damas.partidaTerminada():
                tableroGenerado = True

        return damas

    def aplicarAprendizaje(self, decisiones, valorFinal):

        weights = list(self.maquinaA.weights)

        for i,decision in enumerate(decisiones):

            valorEntrenamiento = decisiones[i + 1].valorTableroAlInicioDelTurno if i + 1 < len(decisiones) else valorFinal

            for j,w in enumerate(weights):

                valorParametro = decision.representacionTablero[j] if j < len(weights) -1 else 1

                if j < len(weights) - 1:
                    self.magnitudesPesos[j] += abs(weights[j])

                weights[j] = w + self.factorAprendizaje * valorParametro * \
                                 (valorEntrenamiento - decision.valorTableroResultante)

                assert not math.isnan(weights[j]) and not math.isinf(weights[j])

        return tuple(weights)

    def siguienteIteracion(self, sinAprendizaje):

        decisiones = []

        damas = self.generarTableroInicial()

        colorFichas = random.choice([Turno.BLANCA,Turno.NEGRA])

        while not damas.partidaTerminada():

            maquinaTurno = self.maquinaA if colorFichas == damas.turno else self.maquinaB

            decisionJugador = maquinaTurno.decidirProximaJugada(damas)

            if colorFichas == damas.turno:
                decisionJugador.valorTableroAlInicioDelTurno = \
                    maquinaTurno.valorTablero(maquinaTurno.representacion.obtener(damas.tablero),damas)
                decisiones += [decisionJugador]

            damas = decisionJugador.estadoResultante

        valorFinal = self.maquinaA.valorTablero(None,damas)

        if not sinAprendizaje:
            self.maquinaA.weights = self.aplicarAprendizaje(decisiones, valorFinal)

            if self.aplicarAprendizajeAAmbasMaquinas:
                self.maquinaB.weights = self.maquinaA.weights

        self.jugadasTotales += len(decisiones)

        if valorFinal == (100 * (1 if colorFichas == Turno.BLANCA else -1)):
            self.victorias += 1
        elif valorFinal == 0:
            self.empates += 1
        elif valorFinal == (-100 * (1 if colorFichas == Turno.BLANCA else -1)):
            self.perdidas += 1


class Resultado:
    valorTableroAlInicioDelTurno = None
    estadoResultante = None
    representacionTablero = None
    valorTableroResultante = None
