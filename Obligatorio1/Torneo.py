# -*- coding: utf-8 -*-

from CustomBatchGame import CustomBatchGame
from Players.RandomPlayer import RandomPlayer
from Players.GreedyPlayer import GreedyPlayer
from Players.JugadorGrupo3 import JugadorGrupo3,AnnBuilder
import numpy as np
import matplotlib.pyplot as plt
import DataTypes

class Estadisticas:

    def __init__(self):

        self.Blancos = (0,0,0)
        self.Negros = (0,0,0)
        self.HistoriaBlancos = []
        self.HistoriaNegros = []

    def Cargar(self, blancos, negros, esPrimerJugador, vuelta):

        if not esPrimerJugador:
            blancos = tuple(reversed(blancos))
            negros = tuple(reversed(negros))

        self.Blancos = tuple([sum(x) for x in zip(self.Blancos, blancos)])
        self.Negros = tuple([sum(x) for x in zip(self.Negros, negros)])

        if len(self.HistoriaBlancos) > vuelta:
            self.HistoriaBlancos[vuelta] =  tuple([sum(x) for x in zip(self.HistoriaBlancos[vuelta],blancos)])
            self.HistoriaNegros[vuelta] = tuple([sum(x) for x in zip(self.HistoriaNegros[vuelta], negros)])
        else:
            self.HistoriaBlancos.append(blancos)
            self.HistoriaNegros.append(negros)

    def ObtenerVictorias(self):
        return [sum(x) for x in zip([y[0] for y in self.HistoriaBlancos], [y[0] for y in self.HistoriaNegros])]


    def __str__(self):
        sumas = [sum(x) for x in zip(self.Negros, self.Blancos)]
        return "N: " + str(tuple([float(x)/sum(self.Negros) for x in self.Negros])) + "\n" + \
            "B: " + str(tuple([float(x) / sum(self.Blancos) for x in self.Blancos]))  + "\n" + \
            "T: " + str(tuple([float(x) / sum(sumas) for x in sumas]))


class Contrincante:

    def __init__(self, nombre, jugador):
        self.nombre = nombre
        self.jugador = jugador
        self.estadisticas = Estadisticas()


class Aprendiz:

    def __init__(self, nombre, red, minmax = 3):
        self.nombre = nombre
        self.red = red
        self.jugador = None
        self.minmax = minmax
        self.estadisticas = Estadisticas()

class Torneo:

    def __init__(self, aprendices, contrincantes, partidas = 50, torneos = 1):
        self.aprendices = aprendices
        self.contricantes = contrincantes
        self.partidas = partidas
        self.torneos = torneos

    def ejecutar(self):

        print("Iniciando torneo")

        for aprendiz in self.aprendices:
            aprendiz.jugador = JugadorGrupo3(None,aprendiz.nombre + '.pkl', aprendiz.red, aprendiz.minmax)

        for i in range(self.torneos):
            print ("Vuelta " + str(i) + " del torneo")
            self.ejecutarVuelta(i)

        for aprendiz in self.aprendices:
            print (aprendiz.nombre + " " + str(aprendiz.estadisticas))

        for contrincante in self.contricantes:
            print (contrincante.nombre + " " + str(contrincante.estadisticas))

        self.plot()

    def ejecutarVuelta(self, i):

        yaJugadas = []

        for aprendiz in self.aprendices:
            for contrincante in self.contricantes:
                self.ejecutarPartidas(aprendiz, contrincante, i)
                aprendiz.jugador.almacenar()

            for otroAprendiz in self.aprendices:
                if aprendiz == otroAprendiz or (otroAprendiz,aprendiz) in yaJugadas:
                    continue

                self.ejecutarPartidas(aprendiz, otroAprendiz, i)
                aprendiz.jugador.almacenar()
                otroAprendiz.jugador.almacenar()

                yaJugadas.append((aprendiz,otroAprendiz))


    def ejecutarPartidas(self, jugadorA, jugadorB, vuelta):
        print(jugadorA.nombre + " vs " + jugadorB.nombre)
        jugadorA.jugador.color = DataTypes.SquareType.BLACK
        jugadorB.jugador.color = DataTypes.SquareType.WHITE

        BvsW = [CustomBatchGame(black_player=jugadorA.jugador, white_player=jugadorB.jugador).play() for _ in
                xrange(self.partidas)]

        jugadorA.jugador.color = DataTypes.SquareType.WHITE
        jugadorB.jugador.color = DataTypes.SquareType.BLACK

        WvsB = [CustomBatchGame(black_player=jugadorB.jugador, white_player=jugadorA.jugador).play() for _ in
                xrange(self.partidas)]

        estatidicasB = self.obtenerSuma(BvsW, DataTypes.GameStatus.BLACK_WINS)
        estatidicasW = self.obtenerSuma(WvsB,DataTypes.GameStatus.WHITE_WINS)

        jugadorA.estadisticas.Cargar(estatidicasW,estatidicasB, True, vuelta)
        jugadorB.estadisticas.Cargar(estatidicasW, estatidicasB, False, vuelta)

        print(estatidicasW)
        print(estatidicasB)

        return (estatidicasW, estatidicasB)

    def plot(self):

        for aprendiz in self.aprendices:
            plt.plot(aprendiz.estadisticas.ObtenerVictorias(),label=aprendiz.nombre)

        for contrincante in self.contricantes:
            plt.plot(contrincante.estadisticas.ObtenerVictorias(),label=contrincante.nombre)

        plt.legend()
        plt.show()

    def obtenerSuma(self, partidas, color):
        victorias = sum([1 for p in partidas if p == color.value])
        empates = sum([1 for p in partidas if p == DataTypes.GameStatus.DRAW.value])
        derrotas = len(partidas) - (victorias + empates)

        return (victorias,empates,derrotas)
