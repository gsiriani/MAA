# -*- coding: UTF-8 -*-

import math
import random
import csv

from damas import Damas, Turno

class TipoAprendizaje():

    APRENDEN_AMBAS_MAQUINAS = 0
    SOLO_MAQUINA_A_APRENDE = 1
    SIN_APRENDIZAJE = 2

class Learner():

    # estadístcas
    victorias = 0
    empates = 0
    perdidas = 0
    jugadasTotales = 0

    # la maquina A es la que aprende
    maquinaA = None
    # la maquina B es la contrincante
    maquinaB = None

    # tipo de aprendizaje a aplicar
    tipoAprendizaje = None

    DebugOutput = False

    writer = None
    file = None

    def __init__(self, maquinaA, maquinaB, factorAprendizaje, tipoAprendizaje = TipoAprendizaje.APRENDEN_AMBAS_MAQUINAS,
                 fileOutput = None):

        self.maquinaA = maquinaA
        self.maquinaB = maquinaB
        self.tipoAprendizaje = tipoAprendizaje

        # Lleva el conteo del aporte de los terminos de la funcion de fitness
        self.magnitudesPesos = [0 for i in range(maquinaA.representacion.size)]
        random.seed()

        self.factorAprendizaje = factorAprendizaje

        if fileOutput is not None:
            self.file = open(fileOutput, 'wb')
            self.writer = csv.writer(self.file, dialect='excel')

    # Ejecuta un número especificado de partidas
    def run(self, iterations):

        print ("Iniciando ejecución")

        if self.writer is not None:
            self.writer.writerow(self.maquinaA.weights)

        for i in range(iterations):
            if i % 1000 == 0:
                print(str(i) + " iteraciones.")

            self.siguienteIteracion()

            if self.writer is not None:
                self.writer.writerow(self.maquinaA.weights)

        if self.writer is not None:
            self.file.close()

        # Se imprimen las estadísticas de las iteraciones
        print ("Ejecución terminada.")
        print ("Partidas realizadas: " + str(iterations))
        print ("Victorias: " + str(self.victorias) + " (" + str(float(self.victorias) / iterations * 100) + "%)")
        print ("Empates: " + str(self.empates) + " (" + str(float(self.empates) / iterations * 100) + "%)")
        print ("Perdidas: " + str(self.perdidas) + " (" + str(float(self.perdidas) / iterations * 100) + "%)")
        print ("Jugadas realizadas: " + str(self.jugadasTotales))
        print ("Pesos: " + str(self.maquinaA.weights))

        sumaMagnitudes = sum(self.magnitudesPesos)

        if sumaMagnitudes > 0:
            # Aporte porcentual de cada termino de la fitness function
            print "Pesos relativos" + str([(float(p) / sumaMagnitudes)*100 for p in self.magnitudesPesos])

    # Se genera la partida inicial tomando un número de jugadas aleatorias iniciales
    def generarTableroInicial(self):

        tableroGenerado = False
        nroJugadas = random.randint(0, 15)

        # Se itera hasta obtener un tablero aceptable
        while not tableroGenerado:

            damas = Damas(Damas.tablero_base(), random.choice([Turno.BLANCA, Turno.NEGRA]))

            for i in range(nroJugadas):
                movimientoAlAzar = random.choice(damas.movimientosValidosCalculados)
                damas = damas.obtenerTableroResultante(movimientoAlAzar)

                if damas.partidaTerminada():
                    break

            # No se aceptan partidas terminadas como tableros iniciales
            if not damas.partidaTerminada():
                tableroGenerado = True

        return damas

    # Se aplica Least Mean Squares para ajustar los weights de la fitness function
    def aplicarAprendizaje(self, decisiones, valorFinal):

        weights = list(self.maquinaA.weights)

        for i,decision in enumerate(decisiones):

            # El valor objetivo se toma como el valor del tablero al inicio del turno siguiente
            # o como el valor final de la partida si es la ultima jugada
            valorEntrenamiento = decisiones[i + 1].valorTableroAlInicioDelTurno if i + 1 < len(decisiones) else valorFinal

            for j,w in enumerate(weights):

                # Se toman los valores de la representación y se toma 1 como el valor de le representacióm
                valorParametro = decision.representacionTablero[j] if j < len(weights) -1 else 1

                # Se incorporan los datos de los pesos
                if j < len(weights) - 1:
                    self.magnitudesPesos[j] += abs(weights[j] * decision.representacionTablero[j])

                weights[j] = w + self.factorAprendizaje * valorParametro * \
                                 (valorEntrenamiento - decision.valorTableroResultante)

                assert not math.isnan(weights[j]) and not math.isinf(weights[j])

        return tuple(weights)

    def siguienteIteracion(self):

        decisiones = []

        damas = self.generarTableroInicial()

        colorFichas = random.choice([Turno.BLANCA, Turno.NEGRA])

        while not damas.partidaTerminada():

            maquinaTurno = self.maquinaA if colorFichas == damas.turno else self.maquinaB

            decisionJugador = maquinaTurno.decidirProximaJugada(damas)

            if self.DebugOutput:
                print("****")
                print("Turno de " + "BLANCAS" if damas.turno == Turno.BLANCA else "NEGRAS")
                print("Turno de " + "MAQUINA A" if maquinaTurno == self.maquinaA else "MAQUINA B")
                print("Se elige jugada con valor " + str(decisionJugador.valorTableroResultante))
                print("****")

            if colorFichas == damas.turno:
                decisionJugador.valorTableroAlInicioDelTurno = \
                    maquinaTurno.valorTablero(maquinaTurno.representacion.obtener(damas.tablero),damas)
                decisiones += [decisionJugador]

                damas = decisionJugador.estadoResultante

        valorFinal = self.maquinaA.valorTablero(None,damas)

        if self.DebugOutput:
            print("### Valor final: " + str(valorFinal) + " ###")

        if self.tipoAprendizaje != TipoAprendizaje.SIN_APRENDIZAJE:
            self.maquinaA.weights = self.aplicarAprendizaje(decisiones, valorFinal)

            if self.tipoAprendizaje == TipoAprendizaje.APRENDEN_AMBAS_MAQUINAS:
                self.maquinaB.weights = self.maquinaA.weights

        self.jugadasTotales += len(decisiones)

        if valorFinal * (1 if colorFichas == Turno.BLANCA else -1) > 0 :
            self.victorias += 1
        elif valorFinal == 0:
            self.empates += 1
        else:
            self.perdidas += 1


class Resultado:
    valorTableroAlInicioDelTurno = None
    estadoResultante = None
    representacionTablero = None
    valorTableroResultante = None
