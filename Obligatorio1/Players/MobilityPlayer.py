# -*- coding:utf-8 -*-
from collections import defaultdict
from copy import deepcopy
from DataTypes import SquareType
from Player import Player
from Players import PositionalPlayer


class MobilityPlayer(Player):
    """Jugador que siempre elige la jugada que más fichas come."""

    name = 'MobilityPlayer'

    def __init__(self, color):
        super(MobilityPlayer, self).__init__(self.name, color)

    def move(self, board, opponent_move):
        """
        :param board: Board
        :param opponent_move: Move
        :return: Move
        """
        max_value = 0
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

        diferenciaFichas = 0
        tableroOcupado = 0

        esquinas = 0

        for x in xrange(8):
            for y in xrange(8):

                ficha = tablero[x][y]
                if ficha == SquareType.EMPTY:
                    break

                multiplicador = 1 if ficha == self.color else -1

                if (x == 0 or x == 7) and (y == 0 or y == 7):
                    esquinas += multiplicador

                diferenciaFichas += multiplicador
                tableroOcupado += 1

        otroColor = SquareType((self.color.value + 1) % 2)

        if float(tableroOcupado) / 64 <= 0.8:
            mobilidadColor = len(tablero.get_possible_moves(self.color))
            mobilidadOtroColor = len(tablero.get_possible_moves(otroColor))

            mobilidad = (mobilidadColor - mobilidadOtroColor) / float(mobilidadColor + mobilidadOtroColor)

            return esquinas * 10 + mobilidad
        else:
            return diferenciaFichas

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
