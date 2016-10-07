# -*- coding: utf-8 -*-

from CustomBatchGame import CustomBatchGame
from Players.RandomPlayer import RandomPlayer
from Players.GreedyPlayer import GreedyPlayer
from Players.JugadorGrupo3 import JugadorGrupo3,AnnBuilder
import DataTypes

class Contrincante:

    def __init__(self, nombre, jugador):
        self.nombre = nombre
        self.jugador = jugador
        self.estadisticos = (0,0,0)

class Aprendiz:

    def __init__(self, nombre, red):
        self.nombre = nombre
        self.red = red
        self.jugador = None
        self.estadisticas = (0,0,0)

class Torneo:

    def __init__(self, aprendices, contrincantes, partidas = 50, torneos = 1):
        self.aprendices = aprendices
        self.contricantes = contrincantes
        self.partidas = partidas
        self.torneos = torneos

    def ejecutar(self):

        print("Iniciando torneo")

        for aprendiz in self.aprendices:
            aprendiz.jugador = JugadorGrupo3(None,aprendiz.nombre + '.pkl', aprendiz.red)

        for i in range(self.torneos):
            print ("Vuelta " + str(i) + " del torneo")
            self.ejecutarVuelta()

        for aprendiz in self.aprendices:
            print (aprendiz.nombre + " " + aprendiz.estadisticas)

        for contrincante in self.contricantes:
            print (contrincante.nombre + " " + contrincante.estadisticas)

    def ejecutarVuelta(self):

        for aprendiz in self.aprendices:
            for contrincante in self.contricantes:
                self.ejecutarPartidas(aprendiz, contrincante)
                aprendiz.jugador.almacenar()

            for otroAprendiz in self.aprendices:
                self.ejecutarPartidas(aprendiz, otroAprendiz)
                aprendiz.jugador.almacenar()
                otroAprendiz.jugador.almacenar()


    def ejecutarPartidas(self, jugadorA, jugadorB):
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

        jugadorA.estadisticas = tuple([sum(x) for x in zip(jugadorA.estadisticas, estatidicasW)])
        jugadorA.estadisticas = tuple([sum(x) for x in zip(jugadorA.estadisticas, estatidicasB)])

        jugadorB.estadisticas = tuple([sum(x) for x in zip(jugadorB.estadisticas, reversed(estatidicasW))])
        jugadorB.estadisticas = tuple([sum(x) for x in zip(jugadorB.estadisticas, reversed(estatidicasB))])

        print ("Resultado: B:" + str([float(e)/len(estatidicasB)for e in estatidicasB]) +
               " W:" + str([float(e)/len(estatidicasW)for e in estatidicasW]))

    def obtenerSuma(self, partidas, color):
        victorias = sum([1 for p in partidas if p == color.value])
        empates = sum([1 for p in partidas if p == DataTypes.GameStatus.DRAW])
        derrotas = len(partidas) - (victorias + empates)

        return (victorias,empates,derrotas)

aprendices = []
aprendices.append(Aprendiz("nn", AnnBuilder.Red10()))
aprendices.append(Aprendiz("nn2", AnnBuilder.Red10_8()))
contrincantes = []
contrincantes.append(Contrincante("Random",RandomPlayer(DataTypes.SquareType.BLACK)))

torneo = Torneo(aprendices, contrincantes)
torneo.ejecutar()
