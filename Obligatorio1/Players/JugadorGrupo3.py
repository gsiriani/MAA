# -*- coding: utf-8 -*-
from collections import defaultdict

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

    def __init__(self, jugada, valor = 0, tablero_resultante = None):

        self.valor = valor
        self.tablero_resultante = tablero_resultante
        self.jugada = jugada

class JugadorGrupo3(Player):
    name = 'JugadorGrupo3'

    def __init__(self, color, path = "nn-no-minmax.pkl", red = None, profundidadMinmax = 3):
        super(JugadorGrupo3, self).__init__(self.name, color=color)
        self._ann = Ann()
        self._tableros_resultantes = []
        self.cargar(path,red)
        self.profundidadMinMax = profundidadMinmax
        self.aplicarEntrenamiento = red is not None

    def move(self, board, opponent_move):
        mejorResultado = self.minmax(board, self.profundidadMinMax, True)

        self._tableros_resultantes.append(mejorResultado.tablero_resultante)

        return mejorResultado.jugada

    def minmax(self, board, profundidad, maximizar):

        if profundidad == 0:
            valor, tablero = self._evaluar_tablero(board)
            return ResultadoJugada(None, valor, tablero)

        colorTurno = self.color if maximizar else SquareType((self.color.value + 1) % 2)
        movimientos_posibles = board.get_possible_moves(colorTurno)

        if len(movimientos_posibles) == 0:
            valor, tablero = self._evaluar_tablero(board)
            return ResultadoJugada(None, valor, tablero)

        resultados = []

        for j in movimientos_posibles:
            nuevoTablero = self._ejecutar_jugada(j, board)
            resultado = self.minmax(nuevoTablero, profundidad - 1, not maximizar)
            resultado.jugada = j
            resultados.append(resultado)

        if maximizar:
            mejorResultado = max(resultados, key=lambda r: r.valor)
        else:
            mejorResultado = min(resultados, key=lambda r: r.valor)

        return mejorResultado


    def on_win(self, board):
        if self.aplicarEntrenamiento:
            resultado = EnumResultado.VICTORIA if self.profundidadMinMax % 2 == 1 else EnumResultado.DERROTA
            self._ann.entrenar(self._tableros_resultantes, resultado)
        self._tableros_resultantes = []

    def on_defeat(self, board):
        if self.aplicarEntrenamiento:
            resultado = EnumResultado.VICTORIA if self.profundidadMinMax % 2 == 1 else EnumResultado.DERROTA
            self._ann.entrenar(self._tableros_resultantes, resultado)
        self._tableros_resultantes = []

    def on_draw(self, board):
        if self.aplicarEntrenamiento:
            self._ann.entrenar(self._tableros_resultantes, EnumResultado.EMPATE)
        self._tableros_resultantes = []

    def on_error(self, board):
        raise Exception('Hubo un error.')

    def _ejecutar_jugada(self,jugada, t):
        tablero = deepcopy(t)

        for square in tablero.get_squares_to_mark(jugada, self.color):
            tablero.set_position(square[0], square[1], self.color)

        return tablero

    def _evaluar_tablero(self, t, invertir = False):

        matriz = t.get_as_matrix()

        entrada = [self._transormarCasilla(square, invertir).value for fila in matriz for square in fila]

        if self._partida_finalizada(t):
            return self._puntaje_final(t), entrada

        return (self._ann.evaluar(np.array(entrada).reshape(1,-1)), entrada)

    def _partida_finalizada(self,tablero):
        return not tablero.get_possible_moves(SquareType.BLACK) and not tablero.get_possible_moves(SquareType.WHITE)

    def _puntaje_final(self, t):
        results = defaultdict(int)
        otroColor = SquareType((self.color.value + 1) % 2)

        for i in xrange(8):
            for j in xrange(8):
                results[t.get_position(i, j)] += 1
        if results[self.color] > results[otroColor]:
            return EnumResultado.VICTORIA.value
        if results[self.color] < results[otroColor]:
            return EnumResultado.DERROTA.value
        else:
            return EnumResultado.EMPATE.value


    def _transormarCasilla(self, casilla, invertir):
        if casilla == SquareType.EMPTY.value:
            return EnumCasilla.EMPTY
        elif (not invertir and casilla == self.color.value) or (invertir and casilla != self.color.value):
            return EnumCasilla.PROPIA
        else:
            return EnumCasilla.RIVAL

    def almacenar(self):
        if self.aplicarEntrenamiento:
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



