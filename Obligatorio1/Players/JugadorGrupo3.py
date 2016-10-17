# -*- coding: utf-8 -*-
from collections import defaultdict
import collections
from sklearn.neural_network import MLPRegressor

from Move import Move
from Player import Player
import random
from copy import deepcopy
from DataTypes import SquareType
from enum import Enum
import numpy as np
import pickle
import os
import math
import sys

class ResultadoJugada():

    def __init__(self, jugada, valor = 0, tablero_resultante = None):

        self.valor = valor
        self.tablero_resultante = tablero_resultante
        self.jugada = jugada

class TranspositionTableItem():

    def __init__(self, resultado, profundidad):
        self.resultado = resultado
        self.profundidad = profundidad

class TramspositionTable():

    def __init__(self, tamanoMaximo = 10000):
        self.tamanoMaximo = tamanoMaximo
        self.tabla = collections.OrderedDict()
        self.consultas = 0
        self.consultasExitosas = 0

    def agregar(self, t, resultado, profundidad):
        if self.tabla.has_key(t):
            elemento = self.tabla[t]
            if elemento.profundidad <= profundidad:
                self.tabla.pop(t)
                elemento.resultado = resultado
                elemento.profundidad = profundidad
                self.tabla[t] = elemento
        else:

            if len(self.tabla) >= self.tamanoMaximo - 1:
                self.tabla.popitem(last=False)

            elemento = TranspositionTableItem(resultado, profundidad)
            self.tabla[t] = elemento

    def obtener(self, t, profundidad):

        self.consultas += 1

        if self.tabla.has_key(t):
            self.consultasExitosas += 1
            elemento = self.tabla[t]

            return elemento if elemento.profundidad >= profundidad else None

        return None

    def limpiar(self):

        self.tabla.clear()

class JugadorGrupo3(Player):
    name = 'JugadorGrupo3'

    def __init__(self, color, path = None, red = None, profundidadMinmax = 3):
        super(JugadorGrupo3, self).__init__(self.name, color=color)
        self._ann = [Ann(), Ann(), Ann()]
        self._tableros_resultantes = []
        self.cargar(path,red)
        self.profundidadMinMax = profundidadMinmax
        self.aplicarEntrenamiento = red is not None
        self.tablaTransposicion = TramspositionTable()
        self.epsilonGreedy = 0
        self.epsilonGreedyFactor = 0.999
        self.jugadasPosibles = None
        self.usoCache = []

        if path is None:
            self.path = os.path.join("redes","nn-50-50-x3")

    def encontrarJugadasPosibles(self, board):
        self.jugadasPosibles = []

        for x in xrange(8):
            for y in xrange(8):
                if board.get_position(x, y) == SquareType.EMPTY:
                    self.jugadasPosibles.append((x,y))


    def move(self, board, opponent_move):

        if self.jugadasPosibles is None:
            self.encontrarJugadasPosibles(board)
        elif opponent_move is not None:
            self.jugadasPosibles.remove((opponent_move.get_row(), opponent_move.get_col()))

        usarExploracion = random.uniform(0, 1) <= self.epsilonGreedy
        if not usarExploracion:
            mejorResultado = self.minmax(board, self.profundidadMinMax, True)
        else:
            mejorResultado = self.jugadaRandom(board)

        self._tableros_resultantes.append((mejorResultado.tablero_resultante,mejorResultado.valor))
        self.epsilonGreedy *= self.epsilonGreedyFactor

        if self.aplicarEntrenamiento:
            self.tablaTransposicion.limpiar()

        jugada = mejorResultado.jugada
        self.jugadasPosibles.remove((jugada.get_row(),jugada.get_col()))

        return mejorResultado.jugada

    def jugadaRandom(self, board):

        movimientos_posibles = self.get_possible_moves(board, self.color)
        jugada = random.choice(movimientos_posibles)
        nuevoTablero = self._ejecutar_jugada(jugada, board)
        valor, tablero = self._evaluar_tablero(nuevoTablero)
        return ResultadoJugada(jugada, valor, tablero)

    def minmax(self, board, profundidad, maximizar, alpha = - sys.maxint - 1, beta = sys.maxint):

        if profundidad == 0:
            valor, tablero = self._evaluar_tablero(board)
            return ResultadoJugada(None, valor, tablero)

        colorTurno = self.color if maximizar else SquareType((self.color.value + 1) % 2)
        movimientos_posibles = self.get_possible_moves(board, colorTurno)

        if len(movimientos_posibles) == 0:
            valor, tablero = self._evaluar_tablero(board)
            return ResultadoJugada(None, valor, tablero)

        tableroInicial = self._transformar_tablero(board)
        resultadoAlmacenado = self.tablaTransposicion.obtener(tableroInicial, profundidad)

        if resultadoAlmacenado is not None:
            return resultadoAlmacenado.resultado

        movimientos_posibles.sort(key=lambda x: self._evaluar_tablero(self._ejecutar_jugada(x, board))[0])
        movimientos_posibles.reverse()

        mejorResultado = None

        for j in movimientos_posibles:
            nuevoTablero = self._ejecutar_jugada(j, board)
            resultado = self.minmax(nuevoTablero, profundidad - 1, not maximizar, alpha, beta)
            resultado.jugada = j
            if maximizar:
                mejorResultado = resultado if mejorResultado is None or mejorResultado.valor < resultado.valor else mejorResultado
                alpha = max(alpha, mejorResultado.valor)
                if beta <= alpha:
                    break
            else:
                mejorResultado = resultado if mejorResultado is None or mejorResultado.valor > resultado.valor else mejorResultado
                beta = min(beta, mejorResultado.valor)
                if beta <= alpha:
                    break

        self.tablaTransposicion.agregar(tableroInicial, mejorResultado, profundidad)

        return mejorResultado

    def get_possible_moves(self, board, color):
        moves = []
        for x, y in self.jugadasPosibles:
            move = Move(x, y)
            if board.is_valid_move(move, color):
                moves.append(move)
        return moves


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
        self.jugadasPosibles = None
        self.usoCache.append(float(self.tablaTransposicion.consultasExitosas)/self.tablaTransposicion.consultas)
        self.tablaTransposicion.consultas = 0
        self.tablaTransposicion.consultasExitosas = 0

    def on_defeat(self, board):
        if self.aplicarEntrenamiento:
            resultado = EnumResultado.DERROTA if self.profundidadMinMax % 2 == 1 else EnumResultado.VICTORIA
            self.entrenarRedes(resultado)
        self._tableros_resultantes = []
        self.jugadasPosibles = None
        self.usoCache.append(float(self.tablaTransposicion.consultasExitosas) / self.tablaTransposicion.consultas)
        self.tablaTransposicion.consultas = 0
        self.tablaTransposicion.consultasExitosas = 0

    def on_draw(self, board):
        if self.aplicarEntrenamiento:
            self.entrenarRedes(EnumResultado.EMPATE)
        self._tableros_resultantes = []
        self.jugadasPosibles = None
        self.usoCache.append(float(self.tablaTransposicion.consultasExitosas) / self.tablaTransposicion.consultas)
        self.tablaTransposicion.consultas = 0
        self.tablaTransposicion.consultasExitosas = 0

    def on_error(self, board):
        raise Exception('Hubo un error.')

    def _ejecutar_jugada(self,jugada, t):
        tablero = deepcopy(t)

        for square in tablero.get_squares_to_mark(jugada, self.color):
            tablero.set_position(square[0], square[1], self.color)

        return tablero

    def smoothingCoeficient(self,n,u):

        return math.pow(math.e,-math.pow((n-u),2)/float(20**2))

    def _transformar_tablero(self, t):
        matriz = t.get_as_matrix()
        return tuple([self._transormarCasilla(square).value for fila in matriz for square in fila])

    def _evaluar_tablero(self, t):

        entrada = self._transformar_tablero(t)

        if self._partida_finalizada(t):
            return self._puntaje_final(t), entrada

        eval = [ann.evaluar(np.array(entrada).reshape(1,-1)) for ann in self._ann]
        n = self.cantidadFichas()
        coeficients = [self.smoothingCoeficient(n,4),self.smoothingCoeficient(n,34),self.smoothingCoeficient(n,64)]

        smoothed = sum(x[0]*x[1] for x in zip(eval,coeficients)) / sum(coeficients)

        return smoothed, entrada #self._ann[self.obtenerRedObjetivo()].evaluar(np.array(entrada).reshape(1,-1)), entrada #smoothed, entrada

    def _partida_finalizada(self,tablero):
        return not self.get_possible_moves(tablero, SquareType.BLACK) and not self.get_possible_moves(tablero, SquareType.WHITE)

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


    def _transormarCasilla(self, casilla):
        if casilla == SquareType.EMPTY.value:
            return EnumCasilla.EMPTY
        elif casilla == self.color.value:
            return EnumCasilla.PROPIA
        else:
            return EnumCasilla.RIVAL

    def almacenar(self):
        if self.aplicarEntrenamiento:
            self._ann[0].almacenar()
            self._ann[1].almacenar()
            self._ann[2].almacenar()

    def cargar(self, path, red):
        self._ann[0].cargar(os.path.join(os.path.dirname(path),"01_" + os.path.basename(path)),
                            red[0] if red is not None else None)
        self._ann[1].cargar(os.path.join(os.path.dirname(path),"02_" + os.path.basename(path)),
                            red[1] if red is not None else None)
        self._ann[2].cargar(os.path.join(os.path.dirname(path),"03_" + os.path.basename(path)),
                            red[2] if red is not None else None)

    def entrenar(self):
        if self.aplicarEntrenamiento:
            for ann in self._ann:
                ann.entrenar()

class Ann:
    def __init__(self):

        self._nn = MLPRegressor(hidden_layer_sizes=(10,), verbose=False, warm_start=True)
        self._entradas_entrenamiento = []
        self._salidas_esperadas_entrenamiento = []
        self.lambdaCoefficient = 0.9

    def evaluar(self, entrada):
        return self._nn.predict(entrada)

    def agregar_a_entrenamiento(self, tableros, resultado):

        tableros.reverse()
        for i in xrange(len(tableros)):
            tablero, valorEstimado = tableros[i][0], tableros[i][1]
            self._entradas_entrenamiento.append(tablero)
            if i == 0 or True:
                self._salidas_esperadas_entrenamiento.append(resultado.value)
            else:
                valorAAprender = valorEstimado + self.lambdaCoefficient * (
                self._salidas_esperadas_entrenamiento[i - 1] -
                valorEstimado)
                self._salidas_esperadas_entrenamiento.append(valorAAprender)

    def entrenar(self):
        self._nn.partial_fit(self._entradas_entrenamiento, self._salidas_esperadas_entrenamiento)
        self._entradas_entrenamiento = []
        self._salidas_esperadas_entrenamiento = []

    def almacenar(self):
        pickle.dump(self._nn, open(self.path, 'wb'))

    def cargar(self, path, red):
        self.path = path
        if os.path.isfile(path):
            self._nn = pickle.load(open(path, 'rb'))
        else:
            self._nn = red
            tableroVacio = ([EnumCasilla.EMPTY.value for _ in xrange(64)], 0)
            self.agregar_a_entrenamiento([tableroVacio], EnumResultado.EMPATE)
            self.entrenar()


class EnumCasilla(Enum):
    RIVAL = -1
    PROPIA = 1
    EMPTY = 0


class EnumResultado(Enum):
    VICTORIA = 1
    EMPATE = 0
    DERROTA = -1
