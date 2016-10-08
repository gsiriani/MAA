# -*- coding: utf-8 -*-

from CustomBatchGame import CustomBatchGame
from Players.RandomPlayer import RandomPlayer
from Players.GreedyPlayer import GreedyPlayer
from Players.JugadorGrupo3 import JugadorGrupo3,AnnBuilder
import DataTypes

class Estadisticas:

    def __init__(self):

        self.Blancos = ()
        self.Negros = ()
        self.HistoriaBlancos = []
        self.HistoriaNegros = []

    def Cargar(self, blancos, negros, esPrimerJugador):

        if not esPrimerJugador:
            blancos = tuple(reversed(blancos))
            negros = tuple(reversed(negros))

        self.Blancos = tuple([sum(x) for x in zip(self.Blancos, blancos)])
        self.Negros = tuple([sum(x) for x in zip(self.Negros, negros)])
        self.HistoriaBlancos.append(blancos)
        self.HistoriaNegros.append(negros)


    def __str__(self):

        print "N: " + str(tuple([float(x)/sum(self.Negros) for x in self.Negros]))
        print "B: " + str(tuple([float(x) / sum(self.Blancos) for x in self.Blancos]))
        sumas = [x[0] + x[1] for x in zip(self.Negros, self.Blancos)]
        print "T: " + str(tuple([float(x) / sum(sumas) for x in sumas]))


class Contrincante:

    def __init__(self, nombre, jugador):
        self.nombre = nombre
        self.jugador = jugador
        self.estadisticas = Estadisticas()


class Aprendiz:

    def __init__(self, nombre, red):
        self.nombre = nombre
        self.red = red
        self.jugador = None
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
            aprendiz.jugador = JugadorGrupo3(None,aprendiz.nombre + '.pkl', aprendiz.red)

        for i in range(self.torneos):
            print ("Vuelta " + str(i) + " del torneo")
            self.ejecutarVuelta()

        for aprendiz in self.aprendices:
            print (aprendiz.nombre + " " + str(aprendiz.estadisticas))

        for contrincante in self.contricantes:
            print (contrincante.nombre + " " + str(contrincante.estadisticas))

    def ejecutarVuelta(self):

        yaJugadas = []

        for aprendiz in self.aprendices:
            for contrincante in self.contricantes:
                self.ejecutarPartidas(aprendiz, contrincante)
                aprendiz.jugador.almacenar()

            for otroAprendiz in self.aprendices:
                if aprendiz == otroAprendiz or (otroAprendiz,aprendiz) in yaJugadas:
                    continue

                self.ejecutarPartidas(aprendiz, otroAprendiz)
                aprendiz.jugador.almacenar()
                otroAprendiz.jugador.almacenar()

                yaJugadas.append((aprendiz,otroAprendiz))


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

        jugadorA.estadisticas.Cargar(estatidicasW,estatidicasB, True)
        jugadorB.estadisticas.Cargar(estatidicasW, estatidicasB, False)

        print(estatidicasW)
        print(estatidicasB)

    def obtenerSuma(self, partidas, color):
        victorias = sum([1 for p in partidas if p == color.value])
        empates = sum([1 for p in partidas if p == DataTypes.GameStatus.DRAW.value])
        derrotas = len(partidas) - (victorias + empates)

        return (victorias,empates,derrotas)

aprendices = []
aprendices.append(Aprendiz("nn", AnnBuilder.Red10()))
aprendices.append(Aprendiz("nn2", AnnBuilder.Red10_8()))
contrincantes = []
contrincantes.append(Contrincante("Random",RandomPlayer(DataTypes.SquareType.BLACK)))

torneo = Torneo(aprendices, contrincantes, 100, 10)
torneo.ejecutar()
