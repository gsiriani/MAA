# -*- coding: utf-8 -*-

import time

import matplotlib.pyplot as plt
from sklearn.neural_network import MLPRegressor

import DataTypes
from CustomBatchGame import CustomBatchGame
from Players.JugadorGrupo3 import JugadorGrupo3
from extras.JugadorGrupoSimple import JugadorGrupoSimple


class Estadisticas:

    def __init__(self):

        self.Blancos = (0,0,0)
        self.Negros = (0,0,0)
        self.HistoriaBlancos = []
        self.HistoriaNegros = []
        self.HistoriaNegrosVs = {}
        self.HistoriaBlancosVs = {}
        self.PartidasJugadas = 0

    def Cargar(self, blancos, negros, esPrimerJugador, contrincante,vuelta):

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

        if not self.HistoriaNegrosVs.has_key(contrincante):
            self.HistoriaNegrosVs[contrincante] = (0, 0, 0)
            self.HistoriaBlancosVs[contrincante] = (0, 0, 0)

        self.PartidasJugadas += sum(blancos) + sum(negros)

        self.HistoriaNegrosVs[contrincante] = tuple([sum(x) for x in zip(self.HistoriaNegrosVs[contrincante], negros)])
        self.HistoriaBlancosVs[contrincante] = tuple([sum(x) for x in zip(self.HistoriaBlancosVs[contrincante], blancos)])

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

class AnnBuilder:
    @staticmethod
    def Red10():
        return MLPRegressor(hidden_layer_sizes=(10,), verbose=False, warm_start=True)

    @staticmethod
    def Red50():
        return MLPRegressor(hidden_layer_sizes=(50,), verbose=False, warm_start=True)

    @staticmethod
    def Red10_8():
        return MLPRegressor(hidden_layer_sizes=(10, 8), verbose=False, warm_start=True)

    @staticmethod
    def Red50_50():
        return MLPRegressor(hidden_layer_sizes=(50, 50), verbose=False, warm_start=True)



class Torneo:

    def __init__(self, aprendices, contrincantes, partidas = 50, torneos = 1):
        self.aprendices = aprendices
        self.contricantes = contrincantes
        self.partidas = partidas
        self.torneos = torneos
        self.comienzoAleatorio = False

    def ejecutar(self):

        print(time.asctime() + " - " +  "Iniciando torneo")

        for aprendiz in self.aprendices:
            if isinstance(aprendiz.red,list):
                print ("Inicializando jugador multi red")
                aprendiz.red = None if len(aprendiz.red) == 0 else aprendiz.red
                aprendiz.jugador = JugadorGrupo3(None, aprendiz.nombre + '.pkl', aprendiz.red, aprendiz.minmax)
            else:
                aprendiz.jugador = JugadorGrupoSimple(None, aprendiz.nombre + '.pkl', aprendiz.red, aprendiz.minmax)

        for i in range(self.torneos):
            print (time.asctime() + " - " + "*** Vuelta " + str(i) + " del torneo ***")
            self.ejecutarVuelta(i)

        for aprendiz in self.aprendices:
            print (time.asctime() + " - " + aprendiz.nombre + " " + str(aprendiz.estadisticas))

        for contrincante in self.contricantes:
            print (time.asctime() + " - " + contrincante.nombre + " " + str(contrincante.estadisticas))

        self.plot()

    def ejecutarVuelta(self, i):

        yaJugadas = []

        for aprendiz in self.aprendices:
            for contrincante in self.contricantes:
                self.ejecutarPartidas(aprendiz, contrincante, i)
                print (time.asctime() + " - " + "Entrenando...")
                aprendiz.jugador.entrenar()
                print (time.asctime() + " - " + "Fin de entrenamiento...")
                aprendiz.jugador.almacenar()

            for otroAprendiz in self.aprendices:
                if aprendiz == otroAprendiz or (otroAprendiz,aprendiz) in yaJugadas:
                    continue

                self.ejecutarPartidas(aprendiz, otroAprendiz, i)
                print (time.asctime() + " - " + "Entrenando...")

                aprendiz.jugador.entrenar()

                print (time.asctime() + " - " + "Fin de entrenamiento...")
                aprendiz.jugador.almacenar()
                print (time.asctime() + " - " + "Entrenando...")

                otroAprendiz.jugador.entrenar()

                print (time.asctime() + " - " + "Fin de entrenamiento...")
                otroAprendiz.jugador.almacenar()

                yaJugadas.append((aprendiz,otroAprendiz))


    def ejecutarPartidas(self, jugadorA, jugadorB, vuelta):
        print(time.asctime() + " - " + jugadorA.nombre + " vs " + jugadorB.nombre)
        jugadorA.jugador.color = DataTypes.SquareType.BLACK
        jugadorB.jugador.color = DataTypes.SquareType.WHITE

        BvsW = [CustomBatchGame(black_player=jugadorA.jugador, white_player=jugadorB.jugador, firstRandomMoves=self.comienzoAleatorio).play() for _ in
                xrange(self.partidas)]

        jugadorA.jugador.color = DataTypes.SquareType.WHITE
        jugadorB.jugador.color = DataTypes.SquareType.BLACK

        WvsB = [CustomBatchGame(black_player=jugadorB.jugador, white_player=jugadorA.jugador, firstRandomMoves=self.comienzoAleatorio).play() for _ in
                xrange(self.partidas)]

        estatidicasB = self.obtenerSuma(BvsW, DataTypes.GameStatus.BLACK_WINS)
        estatidicasW = self.obtenerSuma(WvsB,DataTypes.GameStatus.WHITE_WINS)

        jugadorA.estadisticas.Cargar(estatidicasW, estatidicasB, True, vuelta, jugadorB.nombre)
        jugadorB.estadisticas.Cargar(estatidicasW, estatidicasB, False, vuelta, jugadorA.nombre)

        print(time.asctime() + " - Jugando como Blancas - " + str(estatidicasW))
        print(time.asctime() + " - Jugando como Negras - " + str(estatidicasB))

        return (estatidicasW, estatidicasB)

    def plot(self):

        for aprendiz in self.aprendices:
            plt.plot(aprendiz.estadisticas.ObtenerVictorias(),label=aprendiz.nombre)

        for contrincante in self.contricantes:
            plt.plot(contrincante.estadisticas.ObtenerVictorias(),label=contrincante.nombre)

        plt.legend()
        plt.show()

        plt.clf()

        jugadores = []

        for aprendiz in self.aprendices:
            jugadores.append((aprendiz.nombre, aprendiz.estadisticas.Negros[0], aprendiz.estadisticas.Blancos[0],
                             float(aprendiz.estadisticas.PartidasJugadas)))

        for contrincante in self.contricantes:
            jugadores.append((contrincante.nombre, contrincante.estadisticas.Negros[0], contrincante.estadisticas.Blancos[0],
                             float(contrincante.estadisticas.PartidasJugadas)))

        bar_width = 0.75
        pos = [i + 1 for i in range(len(jugadores))]
        tick_pos = [i + (bar_width / 2) for i in pos]

        plt.bar(pos, [j[1]/j[3] for j in jugadores], label='Juega con negras',color='#F4561D', alpha=0.5)
        plt.bar(pos, [(j[1] + j[2])/j[3] for j in jugadores], label='Juega con blancas',color='#F1911E', alpha=0.5)

        plt.xticks(tick_pos ,[j[0] for j in jugadores])
        plt.xlim([min(tick_pos) - bar_width, max(tick_pos) + bar_width])

        plt.legend()
        plt.show()

    def obtenerSuma(self, partidas, color):
        victorias = sum([1 for p in partidas if p == color.value])
        empates = sum([1 for p in partidas if p == DataTypes.GameStatus.DRAW.value])
        derrotas = len(partidas) - (victorias + empates)

        return (victorias,empates,derrotas)
