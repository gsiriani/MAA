# -*- coding: utf-8 -*-

from Game import Game
from DataTypes import SquareType, GameStatus
from copy import deepcopy
from Players.RandomPlayer import RandomPlayer
import random

class CustomBatchGame(Game):
    DIRS = 8

    def __init__(self, black_player, white_player, firstRandomMoves = False):
        self.players = {SquareType.BLACK: black_player,
                        SquareType.WHITE: white_player}
        self.firstRandomMoves = firstRandomMoves
        super(CustomBatchGame, self).__init__()

    def play(self):
        self._last_move = None
        remainingRandomMoves = random.randint(0,30) if self.firstRandomMoves else 0

        while self._game_status == GameStatus.PLAYING:
            posibleMoves = self._state.get_possible_moves(self._turn)
            if posibleMoves:
                if remainingRandomMoves > 0:
                    self._last_move = random.choice(posibleMoves)
                else:
                    self._last_move = self.players[self._turn].move(deepcopy(self._state), self._last_move)
                self._do_move(self._last_move, self._turn)
            else:
                self._last_move = None
            self._pass_turn()
            remainingRandomMoves -= 1

        self._log_to_file()
        if self._game_status == GameStatus.BLACK_WINS:
            self.players[SquareType.WHITE].on_defeat(deepcopy(self._state))
            self.players[SquareType.BLACK].on_win(deepcopy(self._state))
        elif self._game_status == GameStatus.WHITE_WINS:
            self.players[SquareType.WHITE].on_win(deepcopy(self._state))
            self.players[SquareType.BLACK].on_defeat(deepcopy(self._state))
        elif self._game_status == GameStatus.DRAW:
            self.players[SquareType.WHITE].on_draw(deepcopy(self._state))
            self.players[SquareType.BLACK].on_draw(deepcopy(self._state))
        else:
            self.players[SquareType.WHITE].on_error(deepcopy(self._state))
            self.players[SquareType.BLACK].on_error(deepcopy(self._state))
        return self._game_status.value

if __name__ == '__main__':
    CustomBatchGame().play()
