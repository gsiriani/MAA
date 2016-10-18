# -*- coding: utf-8 -*-

from Torneo import Torneo, Aprendiz
from Players.GreedyPlayer import GreedyPlayer
from Players.JugadorGrupo3 import JugadorGrupo3
from Players.MobilityPlayer import MobilityPlayer
from Players.PositionalPlayer import PositionalPlayer
from Players.RandomPlayer import RandomPlayer
from BatchGame import BatchGame
import os
'''
aprendices = []
#aprendices.append(Aprendiz("nn", AnnBuilder.Red10(), 2))
#aprendices.append(Aprendiz("nn-no-minmax", AnnBuilder.Red10(), 1))
aprendices.append(Aprendiz("nn-2-layer", AnnBuilder.Red10_8(),1))
contrincantes = []
contrincantes.append(Contrincante("Random",RandomPlayer(DataTypes.SquareType.BLACK)))
'''

RandomNegro = [BatchGame(black_player=RandomPlayer, white_player=JugadorGrupo3).play() for _ in xrange(2)]
RandomBlanco = [BatchGame(black_player=JugadorGrupo3, white_player=RandomPlayer).play() for _ in xrange(2)]
print 'Random'
print 'Blanco: ' + str(len([x for x in RandomNegro if x == 0]))
print 'Negro: ' + str(len([x for x in RandomBlanco if x == 1]))

GreedNegro = [BatchGame(black_player=GreedyPlayer, white_player=JugadorGrupo3).play() for _ in xrange(2)]
GreedBlanco = [BatchGame(black_player=JugadorGrupo3, white_player=GreedyPlayer).play() for _ in xrange(2)]
print '\nGreedy'
print 'Blanco: ' + str(len([x for x in GreedNegro if x == 0]))
print 'Negro: ' + str(len([x for x in GreedBlanco if x == 1]))

MobilityNegro = [BatchGame(black_player=MobilityPlayer, white_player=JugadorGrupo3).play() for _ in xrange(2)]
MobilityBlanco = [BatchGame(black_player=JugadorGrupo3, white_player=MobilityPlayer).play() for _ in xrange(2)]
print '\nMobility'
print 'Blanco: ' + str(len([x for x in MobilityNegro if x == 0]))
print 'Negro: ' + str(len([x for x in MobilityBlanco if x == 1]))

PositionalNegro = [BatchGame(black_player=PositionalPlayer, white_player=JugadorGrupo3).play() for _ in xrange(2)]
PositionalBlanco = [BatchGame(black_player=JugadorGrupo3, white_player=PositionalPlayer).play() for _ in xrange(2)]
print '\nPositional'
print 'Blanco: ' + str(len([x for x in PositionalNegro if x == 0]))
print 'Negro: ' + str(len([x for x in PositionalBlanco if x == 1]))
