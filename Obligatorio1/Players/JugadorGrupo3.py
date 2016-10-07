# -*- coding: utf-8 -*-
from sklearn.neural_network import MLPRegressor
from Player import Player
import random
from copy import deepcopy
from DataTypes import SquareType
from enum import Enum
import numpy as np
import pickle
import os

class ResultadoJugada():

    def __init__(self, jugada):

        self.valor = 0
        self.tablero_resultante = None
        self.jugada = jugada

class JugadorGrupo3(Player):
    name = 'JugadorGrupo3'

    def __init__(self, color, path = "nn.pkl", red = None):
        super(JugadorGrupo3, self).__init__(self.name, color=color)
        self._ann = Ann()
        self._tableros_resultantes = []

        self.cargar(path,red)

    def move(self, board, opponent_move):
        jugadas_posibles = board.get_possible_moves(self.color)

        resultados = []

        for j in jugadas_posibles:
            resultado = ResultadoJugada(j)
            resultado.valor, resultado.tablero_resultante = self._evaluar_jugada(j, board)
            resultados.append(resultado)

        mejorResultado = max(resultados, key=lambda r: r.valor)

        self._tableros_resultantes.append(mejorResultado.tablero_resultante)

        return mejorResultado.jugada

    def on_win(self, board):
        #print 'Gané y soy el color:' + self.color.name
        self._ann.entrenar(self._tableros_resultantes, EnumResultado.VICTORIA)
        self._tableros_resultantes = []

    def on_defeat(self, board):
        #print 'Perdí y soy el color:' + self.color.name
        self._ann.entrenar(self._tableros_resultantes, EnumResultado.DERROTA)
        self._tableros_resultantes = []

    def on_draw(self, board):
        #print 'Empaté y soy el color:' + self.color.name
        self._ann.entrenar(self._tableros_resultantes, EnumResultado.EMPATE)
        self._tableros_resultantes = []

    def on_error(self, board):
        raise Exception('Hubo un error.')

    def _evaluar_jugada(self, jugada, t):

        t = self._ejecutar_jugada(jugada,t)

        return self._evaluar_tablero(t)

    def _ejecutar_jugada(self,jugada, t):
        tablero = deepcopy(t)

        for square in tablero.get_squares_to_mark(jugada, self.color):
            tablero.set_position(square[0], square[1], self.color)

        return tablero

    def _evaluar_tablero(self, t):

        matriz = t.get_as_matrix()

        entrada = [self._transormarCasilla(square).value for fila in matriz for square in fila]

        return (self._ann.evaluar(np.array(entrada).reshape(1,-1)), entrada)

    def _transormarCasilla(self, casilla):
        if casilla == self.color.value:
            return EnumCasilla.PROPIA
        elif casilla == SquareType.EMPTY.value:
            return EnumCasilla.EMPTY
        else:
            return EnumCasilla.RIVAL

    def almacenar(self):
        self._ann.almacenar()

    def cargar(self, path, red):
        self._ann.cargar(path, red)

class AnnBuilder:

    @staticmethod
    def Red10():
        return MLPRegressor(hidden_layer_sizes=(10,), verbose=False, warm_start=True)

    @staticmethod
    def Red10_8():
        return MLPRegressor(hidden_layer_sizes=(10,8), verbose=False, warm_start=True)

class Ann:

    def __init__(self):

        self._nn = MLPRegressor(hidden_layer_sizes=(10,), verbose=False, warm_start=True)

    def evaluar(self, entrada):
        return self._nn.predict(entrada)

    def entrenar(self, tableros, resultado):

        tableros.reverse()
        valores = [resultado.value*(0.8**i) for i in range(len(tableros))]

        self._nn.partial_fit(tableros, np.array(valores).reshape(-1,1))

    def almacenar(self):
        pickle.dump(self._nn, open(self.path,'wb'))

    def cargar(self, path, red):
        self.path = path
        if os.path.isfile(path):
            self._nn = pickle.load(open(path, 'rb'))
        else:
            self._nn = red
            tableroVacio = [EnumCasilla.EMPTY.value for _ in xrange(64)]
            self.entrenar([tableroVacio], EnumResultado.EMPATE)


class EnumCasilla(Enum):
    RIVAL = -1
    PROPIA = 1
    EMPTY = 0

class EnumResultado(Enum):
    VICTORIA = 1
    EMPATE = 0
    DERROTA = -1



