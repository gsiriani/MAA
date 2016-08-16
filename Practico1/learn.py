# -*- coding: UTF-8 -*-

import random
import math

from damas import Damas, Turno, Casilla

class Representacion():

    size = 6

    @staticmethod
    def obtener(tablero):

        flattened = [casilla for fila in tablero for casilla in fila]

        cantidadBlancas = sum([1 for c in flattened if c == Casilla.BLANCA])
        cantidadNegras = sum([1 for c in flattened if c == Casilla.NEGRA])

        segurasBlancas = Representacion.obtenerSeguras(tablero, Turno.BLANCA)
        segurasNegras = Representacion.obtenerSeguras(tablero, Turno.NEGRA)

        distanciaLineaFondoBlancas = Representacion.distanciaLineaFondo(tablero, Turno.BLANCA)
        distanciaLineaFondoNegras = Representacion.distanciaLineaFondo(tablero, Turno.NEGRA)

        return cantidadBlancas, cantidadNegras, segurasBlancas, segurasNegras, distanciaLineaFondoBlancas,\
               distanciaLineaFondoNegras

    @staticmethod
    def obtenerSeguras(tablero, color):

        for i in range(8):
            cantidadSeguras = 1 if tablero[0][i] == color else 0
            cantidadSeguras += 1 if tablero[7][i] == color else 0
            cantidadSeguras += 1 if tablero[i][0] == color else 0
            cantidadSeguras += 1 if tablero[i][7] == color else 0

        return cantidadSeguras

    @staticmethod
    def distanciaLineaFondo(tablero, color):

        distancia = 0

        for x in range(8):
            for y in range(8):
                if tablero[x][y] == color:
                    distancia += 7 - x if color == Turno.BLANCA else x

        return distancia


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

        return damas.tablero


    def aplicarAprendizaje(self, decisiones, valorFinal):

        weights = list(self.maquinaA.weights)

        for i,decision in enumerate(decisiones):
            for j,w in enumerate(weights):

                valorEntrenamiento = decisiones[i+1].valorTableroAlInicioDelTurno if i+1 < len(decisiones) else valorFinal
                valorParametro = decision.representacionTablero[j] if j < len(weights) -1 else 1

                weights[j] = w + self.factorAprendizaje * valorParametro * \
                                 (valorEntrenamiento - decision.valorTableroResultante)

                assert not math.isnan(weights[j]) and not math.isinf(weights[j])

        return tuple(weights)

    def siguienteIteracion(self, sinAprendizaje):

        decisiones = []

        damas = Damas(self.generarTableroInicial(),random.choice([Turno.BLANCA,Turno.NEGRA]))

        colorFichas = damas.turno

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

class Maquina:

    MAX_INITIAL_WEIGHT = 1
    MIN_INITIAL_WEIGHT = -1

    representacion = None

    def __init__(self, representacion):

        self.representacion = representacion
        self.weights = tuple(random.uniform(self.MIN_INITIAL_WEIGHT, self.MAX_INITIAL_WEIGHT)
                         for i in range(representacion.size + 1))

    def valorTablero(self, representacion, damas):
        if damas.partidaTerminada():
            return self.valorTableroFinal(damas.tablero)

        valor = sum([x * y for x, y in zip(representacion, self.weights)]) + representacion[len(representacion) - 1]

        assert not math.isinf(valor)

        return valor

    def valorTableroFinal(self, tablero):
        flattened = [casilla for fila in tablero for casilla in fila]

        cantidadBlancas = sum([1 for c in flattened if c == Casilla.BLANCA])
        cantidadNegras = sum([1 for c in flattened if c == Casilla.NEGRA])

        return 0 if cantidadNegras == cantidadBlancas else (100 if cantidadBlancas > cantidadNegras else -100)


    def decidirProximaJugada(self, damas):
        movimientosPosibles = []

        for m in damas.movimientosValidosCalculados:
            resultado = Resultado()
            resultado.estadoResultante = damas.obtenerTableroResultante(m)
            resultado.representacionTablero = self.representacion.obtener(resultado.estadoResultante.tablero)
            resultado.valorTableroResultante = self.valorTablero(resultado.representacionTablero,
                                                                 resultado.estadoResultante)

            movimientosPosibles.append(resultado)

        if damas.turno == Turno.BLANCA:
            mejorResultado = max(movimientosPosibles, key=lambda r: r.valorTableroResultante)
        else:
            mejorResultado = min(movimientosPosibles, key=lambda r: r.valorTableroResultante)

        mejoresResultados = [r for r in movimientosPosibles if
                             r.valorTableroResultante == mejorResultado.valorTableroResultante]
        resultadoElegido = random.choice(mejoresResultados)

        return resultadoElegido


class MaquinaAzar:

    representacion = None

    def __init__(self, representacion):

        self.representacion = representacion
        self.weights = tuple(0 for i in range(representacion.size + 1))

    def valorTablero(self, representacion, damas):
        if damas.partidaTerminada():
            return self.valorTableroFinal(damas.tablero)
        else:
            return 0

    def valorTableroFinal(self, tablero):
        flattened = [casilla for fila in tablero for casilla in fila]

        cantidadBlancas = sum([1 for c in flattened if c == Casilla.BLANCA])
        cantidadNegras = sum([1 for c in flattened if c == Casilla.NEGRA])

        return 0 if cantidadNegras == cantidadBlancas else (100 if cantidadBlancas > cantidadNegras else -100)


    def decidirProximaJugada(self, damas):
        movimientosPosibles = []

        m = random.choice(damas.movimientosValidosCalculados)

        resultado = Resultado()
        resultado.estadoResultante = damas.obtenerTableroResultante(m)
        resultado.representacionTablero = self.representacion.obtener(resultado.estadoResultante.tablero)
        resultado.valorTableroResultante = self.valorTablero(resultado.representacionTablero, resultado.estadoResultante)

        return resultado

class Resultado:
    valorTableroAlInicioDelTurno = None
    estadoResultante = None
    representacionTablero = None
    valorTableroResultante = None
