# -*- coding:utf-8 -*-
from collections import defaultdict
from copy import deepcopy

from DataTypes import SquareType
from Player import Player


class PositionalPlayer(Player):
    """Jugador que siempre elige la jugada que más fichas come."""

    name = 'PositionalPlayer'

    BOARD_VALUES = [
        [100, -20, 10, 5],
        [-20, -50, -2, -2],
        [10, -2, -1, -1],
        [5, -2, -1, -1]
    ]

    def __init__(self, color):
        super(PositionalPlayer, self).__init__(self.name, color)

    def move(self, board, opponent_move):
        """
        :param board: Board
        :param opponent_move: Move
        :return: Move
        """
        max_value = -99999
        chosen_move = None
        for move in board.get_possible_moves(self.color):
            nuevoTablero = self._ejecutar_jugada(move, board)
            valor = self._evaluar_jugada(nuevoTablero)
            if max_value < valor:
                chosen_move = move
                max_value = valor

        return chosen_move

    def _evaluar_jugada(self, t):

        if self._partida_finalizada(t):
            return self._puntaje_final(t)

        tablero = t.get_as_matrix()

        valorInicio = 0
        valorFin = 0
        tableroOcupado = 0

        for x in xrange(8):
            x = int(3.5 - abs(3.5 - x))
            for y in xrange(8):
                y = int(3.5 - abs(3.5 - y))

                ficha = tablero[x][y]
                if ficha == SquareType.EMPTY.value:
                    continue

                multiplicador = 1 if ficha == self.color.value else -1

                valorInicio += PositionalPlayer.BOARD_VALUES[x][y] * multiplicador
                valorFin += multiplicador
                tableroOcupado += 1

        return valorInicio if float(tableroOcupado) / 64 <= 0.8 else valorFin


    def _partida_finalizada(self, tablero):
        return not tablero.get_possible_moves(SquareType.BLACK) and not tablero.get_possible_moves(SquareType.WHITE)

    def _puntaje_final(self, t):
        results = defaultdict(int)
        otroColor = SquareType((self.color.value + 1) % 2)

        for i in xrange(8):
            for j in xrange(8):
                results[t.get_position(i, j)] += 1
        if results[self.color] > results[otroColor]:
            return 999
        if results[self.color] < results[otroColor]:
            return -999
        else:
            return 0


    def _ejecutar_jugada(self,jugada, t):
            tablero = deepcopy(t)

            for square in tablero.get_squares_to_mark(jugada, self.color):
                tablero.set_position(square[0], square[1], self.color)

            return tablero


    def on_win(self, board):
        pass
        #print 'Gané y soy el color:' + self.color.name

    def on_defeat(self, board):
        pass
        #print 'Perdí y soy el color:' + self.color.name

    def on_draw(self, board):
        pass
        #print 'Empaté y soy el color:' + self.color.name

    def on_error(self, board):
        raise Exception('Hubo un error.')
