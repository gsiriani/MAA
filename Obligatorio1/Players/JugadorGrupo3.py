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
    '''
        Representa una jugada a realizar junto al mejor (por minmax) tablero resultante y su valor asociado
    '''

    def __init__(self, jugada, valor = 0, tablero_resultante = None):

        self.valor = valor
        self.tablero_resultante = tablero_resultante
        self.jugada = jugada

class TranspositionTableItem():
    ''''
        Elemento cacheado en la tabla de transposicion
    '''

    def __init__(self, resultado, profundidad):
        self.resultado = resultado
        self.profundidad = profundidad

class TramspositionTable():
    ''''
        Tabla de transposicion. Implementado como un caché LRU
    '''

    def __init__(self, tamanoMaximo = 10000):
        self.tamanoMaximo = tamanoMaximo
        self.tabla = collections.OrderedDict()
        self.consultas = 0
        self.consultasExitosas = 0

    def agregar(self, t, resultado, profundidad):
        # Si ya hay un resultado asociado al tablero
        if self.tabla.has_key(t):
            elemento = self.tabla[t]
            # Lo remplazo si el valor está calculado para una profundidad menor
            if elemento.profundidad <= profundidad:
                self.tabla.pop(t)
                elemento.resultado = resultado
                elemento.profundidad = profundidad
                self.tabla[t] = elemento
        else:
            # Quito el elemento añadido y no actualizado hace más tiempo
            if len(self.tabla) >= self.tamanoMaximo - 1:
                self.tabla.popitem(last=False)

            elemento = TranspositionTableItem(resultado, profundidad)
            self.tabla[t] = elemento

    def obtener(self, t, profundidad):
        # Conservo la cantidad de consulta realizadas
        self.consultas += 1

        if self.tabla.has_key(t):
            self.consultasExitosas += 1
            elemento = self.tabla[t]

            # Devuelvo un elemento sólo si la profundidad para la que fue
            # calculado es mayor o igual a la solcitada
            return elemento if elemento.profundidad >= profundidad else None

        return None

    def limpiar(self):

        self.tabla.clear()

class JugadorGrupo3(Player):
    '''
        Jugador implementado
    '''

    name = 'JugadorGrupo3'

    def __init__(self, color, path = None, red = None, profundidadMinmax = 3):
        super(JugadorGrupo3, self).__init__(self.name, color=color)

        self._tableros_resultantes = []
        self.tablaTransposicion = TramspositionTable()

        self.profundidadMinMax = profundidadMinmax

        self._ann = [Ann(), Ann(), Ann()]

        # Si no le paso una red, no se la entrena
        self.aplicarEntrenamiento = red is not None

        # Se emplean para controlar la política de exploración-explotación del jugador
        self.epsilonGreedy = 0
        self.epsilonGreedyFactor = 0.999

        # Empleado para optimizar la búsqueda de jugadas posibles
        self.jugadasPosibles = None

        # Almacena con fines estadisticos el hit ratio del caché
        self.usoCache = []

        # Si no paso el path a una red entrenada, cargo la red por defecto
        if path is None:
            path = os.path.join("redes","nn-50-50-x3.pkl")

        self.cargar(path,red)

    def encontrarJugadasPosibles(self, board):
        '''
            Como es posible que el tablero ya se encuentre inicializado
            en la primera jugada, busco todas las fichas a las que me podría mover
        '''
        self.jugadasPosibles = []

        for x in xrange(8):
            for y in xrange(8):
                if board.get_position(x, y) == SquareType.EMPTY:
                    self.jugadasPosibles.append((x,y))


    def move(self, board, opponent_move):

        # Primer movimiento por parte del jugador
        if self.jugadasPosibles is None:
            self.encontrarJugadasPosibles(board)
        elif opponent_move is not None:
            # Elimino como jugada posible la posicion ocupada por el opnente
            self.jugadasPosibles.remove((opponent_move.get_row(), opponent_move.get_col()))

        # Probabilidad epsilonGreedy de realizar una jugada al azar
        usarExploracion = random.uniform(0, 1) <= self.epsilonGreedy
        if not usarExploracion:
            mejorResultado = self.minmax(board, self.profundidadMinMax, True)
        else:
            mejorResultado = self.jugadaRandom(board)

        # Almaceno los tableros evaluados para el posterior entrenamiento
        self._tableros_resultantes.append((mejorResultado.tablero_resultante,mejorResultado.valor))

        # Decaimiento exponencial del epsilonGreedy
        self.epsilonGreedy *= self.epsilonGreedyFactor

        # Si se aplica entrenamiento la tabla de transposición queda invalidada
        if self.aplicarEntrenamiento:
            self.tablaTransposicion.limpiar()

        jugada = mejorResultado.jugada
        # La jugada a realizar se quita de las posibles
        self.jugadasPosibles.remove((jugada.get_row(),jugada.get_col()))

        return mejorResultado.jugada

    def jugadaRandom(self, board):
        '''
        Elijo una jugada al azar
        '''

        movimientos_posibles = self.get_possible_moves(board, self.color)
        jugada = random.choice(movimientos_posibles)
        nuevoTablero = self._ejecutar_jugada(jugada, board)
        valor, tablero = self._evaluar_tablero(nuevoTablero)

        return ResultadoJugada(jugada, valor, tablero)


    def minmax(self, board, profundidad, maximizar, alpha = - sys.maxint - 1, beta = sys.maxint):

        # Si es una hoja, devuelvo la evaluación del tablero
        if profundidad == 0:
            valor, tablero = self._evaluar_tablero(board)
            return ResultadoJugada(None, valor, tablero)

        # Determino el color que juega en esta evaluación
        colorTurno = self.color if maximizar else SquareType((self.color.value + 1) % 2)
        movimientos_posibles = self.get_possible_moves(board, colorTurno)

        # Si no hay movimintos posibles, es una hoja
        if len(movimientos_posibles) == 0:
            valor, tablero = self._evaluar_tablero(board)
            return ResultadoJugada(None, valor, tablero)

        tableroInicial = self._transformar_tablero(board)

        # Busco en la tabla de transposición por el tablero
        resultadoAlmacenado = self.tablaTransposicion.obtener(tableroInicial, profundidad)

        if resultadoAlmacenado is not None:
            return resultadoAlmacenado.resultado

        # Ordeno las jugadas a partir de una evaluación de primer nivel
        # para maximizar las chances de cutoff por alpha-beta prunning
        movimientos_posibles.sort(key=lambda x: self._evaluar_tablero(self._ejecutar_jugada(x, board))[0])
        movimientos_posibles.reverse()

        mejorResultado = None

        for j in movimientos_posibles:
            nuevoTablero = self._ejecutar_jugada(j, board)
            # Aplicación recursiva del minmax
            resultado = self.minmax(nuevoTablero, profundidad - 1, not maximizar, alpha, beta)
            resultado.jugada = j
            if maximizar:
                mejorResultado = resultado if mejorResultado is None or mejorResultado.valor < resultado.valor else mejorResultado
                alpha = max(alpha, mejorResultado.valor)
                # Poda beta
                if beta <= alpha:
                    break
            else:
                mejorResultado = resultado if mejorResultado is None or mejorResultado.valor > resultado.valor else mejorResultado
                beta = min(beta, mejorResultado.valor)
                # Poda alfa
                if beta <= alpha:
                    break

        # El tablero calculado se incorpora a la tabla de transposición
        self.tablaTransposicion.agregar(tableroInicial, mejorResultado, profundidad)

        return mejorResultado

    def get_possible_moves(self, board, color):
        '''
            Versión optimizada de board.get_possibles_moves considerando las jugadas
            anteriores para quitarlas de las jugadas a evaluar
        '''
        moves = []
        for x, y in self.jugadasPosibles:
            move = Move(x, y)
            if board.is_valid_move(move, color):
                moves.append(move)
        return moves


    def cantidadFichas(self):
        '''
        Estimación de la cantidad de fichas del tablero (en O(1)) para la decisión de la red a entrenar
        '''
        return 4 + len(self._tableros_resultantes) * 2 + (1 if self.color == SquareType.WHITE else 0)

    def entrenarRedes(self, resultado):
        '''
            Se almacenan las evaluaciones de las redes para el entrenamiento posterior
        '''

        for i in xrange(3):

            # Las redes se entrenan con los movimientos [0,9], [10,19] y [20,29]
            cotaInferior = min(i*10,len(self._tableros_resultantes))
            cotaSuperior = min((i+1) * 10, len(self._tableros_resultantes))
            conjuntoEntrenamiento = self._tableros_resultantes[cotaInferior:cotaSuperior]
            # Si no se alcanzó la red
            if len(conjuntoEntrenamiento) == 0:
                return

            self._ann[i].agregar_a_entrenamiento(conjuntoEntrenamiento, resultado)

    def limpieza(self):
        '''
            Se reinicializan algunos valores para la siguiente partida
        '''
        self._tableros_resultantes = []
        self.jugadasPosibles = None

        # Se acutaliza la historia del hit ratio de la tabla de transposición
        if self.tablaTransposicion.consultas > 0:
            self.usoCache.append(float(self.tablaTransposicion.consultasExitosas) / self.tablaTransposicion.consultas)

        self.tablaTransposicion.consultas = 0
        self.tablaTransposicion.consultasExitosas = 0

    def on_win(self, board):
        if self.aplicarEntrenamiento:
            resultado = EnumResultado.VICTORIA if self.profundidadMinMax % 2 == 1 else EnumResultado.DERROTA
            self.entrenarRedes(resultado)
        self.limpieza()

    def on_defeat(self, board):
        if self.aplicarEntrenamiento:
            resultado = EnumResultado.DERROTA if self.profundidadMinMax % 2 == 1 else EnumResultado.VICTORIA
            self.entrenarRedes(resultado)
        self.limpieza()

    def on_draw(self, board):

        if self.aplicarEntrenamiento:
            self.entrenarRedes(EnumResultado.EMPATE)
        self.limpieza()

    def on_error(self, board):
        raise Exception('Hubo un error.')

    def _ejecutar_jugada(self,jugada, t):
        '''
            Se devuelve una copia del tablero con la jugada aplicada
        '''

        tablero = deepcopy(t)

        for square in tablero.get_squares_to_mark(jugada, self.color):
            tablero.set_position(square[0], square[1], self.color)

        return tablero

    def smoothingCoeficient(self,n,u):
        '''
            Calcula el coeficiente del n-ésimo término de la función de smoothing
        '''
        return math.pow(math.e,-math.pow((n-u),2)/float(20**2))

    def _transformar_tablero(self, t):
        '''
            Obtiene la representación del tablero utilizada por la red
        '''
        matriz = t.get_as_matrix()
        return tuple([self._transormarCasilla(square).value for fila in matriz for square in fila])

    def _evaluar_tablero(self, t):
        '''
            Evalúo el tablero a partir del resultado de las redes
        '''
        entrada = self._transformar_tablero(t)

        # Si el tablero representa una partida finalizada utilizo
        # una evaluación estática
        if self._partida_finalizada(t):
            return self._puntaje_final(t), entrada

        # Obtengo la evaluación de las tres redes
        eval = [ann.evaluar(np.array(entrada).reshape(1,-1)) for ann in self._ann]
        n = self.cantidadFichas()
        coeficients = [self.smoothingCoeficient(n,4),self.smoothingCoeficient(n,34),self.smoothingCoeficient(n,64)]

        smoothed = sum(x[0]*x[1] for x in zip(eval,coeficients)) / sum(coeficients)

        # Devuelvo el valor del tablero y la representación del tablero evaluado
        return smoothed, entrada

    def _partida_finalizada(self,tablero):
        '''
            Determina si la partida está finalizada
        '''
        return not self.get_possible_moves(tablero, SquareType.BLACK) and not self.get_possible_moves(tablero, SquareType.WHITE)

    def _puntaje_final(self, t):
        '''
            Evaluación estática del tablero según la diferencia de fichas
        '''

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
        '''
            Obtiene el tipo de casilla según la pertencia de la ficha de haberla
        '''
        if casilla == SquareType.EMPTY.value:
            return EnumCasilla.EMPTY
        elif casilla == self.color.value:
            return EnumCasilla.PROPIA
        else:
            return EnumCasilla.RIVAL

    def almacenar(self):
        '''
            Persiste el estado de la red
        '''
        if self.aplicarEntrenamiento:
            self._ann[0].almacenar()
            self._ann[1].almacenar()
            self._ann[2].almacenar()

    def cargar(self, path, red):
        '''
            Obtiene el estado persistido de la red
        '''
        self._ann[0].cargar(os.path.join(os.path.dirname(path),"01_" + os.path.basename(path)),
                            red[0] if red is not None else None)
        self._ann[1].cargar(os.path.join(os.path.dirname(path),"02_" + os.path.basename(path)),
                            red[1] if red is not None else None)
        self._ann[2].cargar(os.path.join(os.path.dirname(path),"03_" + os.path.basename(path)),
                            red[2] if red is not None else None)

    def entrenar(self):
        '''
            Entrena las redes a partir
        '''
        if self.aplicarEntrenamiento:
            for ann in self._ann:
                ann.entrenar()

class Ann:
    '''
        Implementación e interfaz de la funcionalidad presentada de la ANN
    '''
    def __init__(self):

        self._nn = MLPRegressor(hidden_layer_sizes=(10,), verbose=False, warm_start=True)
        self._entradas_entrenamiento = []
        self._salidas_esperadas_entrenamiento = []
        # Parámetro de TD-lambda
        self.lambdaCoefficient = 0.9

    def evaluar(self, entrada):
        '''
            Devuelve la evaluación de la red para la entrada
        '''
        return self._nn.predict(entrada)

    def agregar_a_entrenamiento(self, tableros, resultado):
        '''
            Incorpora los datos de la partida a los ejemplos de entrenamiento
        '''

        # Presento la partida de adelante para atrás
        tableros.reverse()
        for i in xrange(len(tableros)):
            # Representación del tablero, Valor estimado
            tablero, valorEstimado = tableros[i][0], tableros[i][1]
            self._entradas_entrenamiento.append(tablero)
            if i == 0 or True:
                # Si es el resultado final, utilizo como salida esperada el resultado de la partida
                self._salidas_esperadas_entrenamiento.append(resultado.value)
            else:
                # El valor a aprender dado por según TD-lambda
                valorAAprender = valorEstimado + self.lambdaCoefficient * (
                    self._salidas_esperadas_entrenamiento[i - 1] - valorEstimado)
                self._salidas_esperadas_entrenamiento.append(valorAAprender)

    def entrenar(self):
        '''
            Aplico el entrenamiento a partir de los datos almacenados
        '''
        self._nn.partial_fit(self._entradas_entrenamiento, self._salidas_esperadas_entrenamiento)
        self._entradas_entrenamiento = []
        self._salidas_esperadas_entrenamiento = []

    def almacenar(self):
        '''
            Serializo y persisto la red
        '''
        pickle.dump(self._nn, open(self.path, 'wb'))

    def cargar(self, path, red):
        '''
            Deserealizo o creo una nueva red
        '''
        self.path = path
        if os.path.isfile(path):
            # Si el archivo especificado existe, deserealizo la red
            self._nn = pickle.load(open(path, 'rb'))
        else:
            # Si no, inicializo la red especificada
            self._nn = red
            tableroVacio = ([EnumCasilla.EMPTY.value for _ in xrange(64)], 0)
            self.agregar_a_entrenamiento([tableroVacio], EnumResultado.EMPATE)
            self.entrenar()


class EnumCasilla(Enum):
    '''
        Representa el estado de una casilla relativo al jugador
    '''

    RIVAL = -1
    PROPIA = 1
    EMPTY = 0


class EnumResultado(Enum):
    '''
        Salidas esperadas de la red según el resultado de la partida
    '''
    VICTORIA = 1
    EMPATE = 0
    DERROTA = -1
