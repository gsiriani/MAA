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
from JugadorGrupo3 import Ann,EnumCasilla,EnumResultado
import os
import math

class ResultadoJugada():

    def __init__(self, jugada, valor = 0, tablero_resultante = None):

        self.valor = valor
        self.tablero_resultante = tablero_resultante
        self.jugada = jugada

class JugadorGrupo3x3(Player):
    name = 'JugadorGrupo3'

    def __init__(self, color, path = "nn-no-minmax.pkl", red = None, profundidadMinmax = 3):
        super(JugadorGrupo3x3, self).__init__(self.name, color=color)
        self._ann = [Ann(), Ann(), Ann()]
        self._tableros_resultantes = []
        self.cargar(path,red)
        self.profundidadMinMax = profundidadMinmax
        self.aplicarEntrenamiento = red is not None

    def move(self, board, opponent_move):
        mejorResultado = self.minmax(board, self.profundidadMinMax, True)

        self._tableros_resultantes.append((mejorResultado.tablero_resultante,mejorResultado.valor))

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

    def cantidadFichas(self):
        return 4 + len(self._tableros_resultantes) * 2 + (1 if self.color == SquareType.WHITE else 0)

    def obtenerRedObjetivo(self):
        return min(int((self.cantidadFichas() - 4) / 20),2)

    def entrenarRedes(self, resultado):

        for i in xrange(3):
            cotaInferior = min(i*10,len(self._tableros_resultantes))
            cotaSuperior = min((i+1) * 10, len(self._tableros_resultantes))
            conjuntoEntrenamiento = self._tableros_resultantes[cotaInferior:cotaSuperior]
            if len(conjuntoEntrenamiento) == 0:
                return
            self._ann[i].agregar_a_entrenamiento(conjuntoEntrenamiento, resultado)

    def on_win(self, board):
        if self.aplicarEntrenamiento:
            resultado = EnumResultado.VICTORIA if self.profundidadMinMax % 2 == 1 else EnumResultado.DERROTA
            self.entrenarRedes(resultado)
        self._tableros_resultantes = []

    def on_defeat(self, board):
        if self.aplicarEntrenamiento:
            resultado = EnumResultado.DERROTA if self.profundidadMinMax % 2 == 1 else EnumResultado.VICTORIA
            self.entrenarRedes(resultado)
        self._tableros_resultantes = []

    def on_draw(self, board):
        if self.aplicarEntrenamiento:
            self.entrenarRedes(EnumResultado.EMPATE)
        self._tableros_resultantes = []

    def on_error(self, board):
        raise Exception('Hubo un error.')

    def _ejecutar_jugada(self,jugada, t):
        tablero = deepcopy(t)

        for square in tablero.get_squares_to_mark(jugada, self.color):
            tablero.set_position(square[0], square[1], self.color)

        return tablero

    def smoothingCoeficient(self,n,u):

        return math.pow(math.e,-math.pow((n-u),2)/float(20**2))

    def _evaluar_tablero(self, t, invertir = False):

        matriz = t.get_as_matrix()

        entrada = [self._transormarCasilla(square, invertir).value for fila in matriz for square in fila]

        if self._partida_finalizada(t):
            return self._puntaje_final(t), entrada

        #eval = [ann.evaluar(np.array(entrada).reshape(1,-1)) for ann in self._ann]
        n = self.cantidadFichas()
        #coeficients = [self.smoothingCoeficient(n,4),self.smoothingCoeficient(n,34),self.smoothingCoeficient(n,64)]

        #smoothed = sum(x[0]*x[1] for x in zip(eval,coeficients)) / sum(coeficients)

        return self._ann[self.obtenerRedObjetivo()].evaluar(np.array(entrada).reshape(1,-1)), entrada #smoothed, entrada

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
            self._ann[0].almacenar()
            self._ann[1].almacenar()
            self._ann[2].almacenar()

    def cargar(self, path, red):
        self._ann[0].cargar("01_" + path, red[0] if red is not None else None)
        self._ann[1].cargar("02_" + path, red[1] if red is not None else None)
        self._ann[2].cargar("03_" + path, red[2] if red is not None else None)

    def entrenar(self):
        if self.aplicarEntrenamiento:
            for ann in self._ann:
                ann.entrenar()
