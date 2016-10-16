# -*- coding: utf-8 -*-

from CustomBatchGame import CustomBatchGame
from Players.RandomPlayer import RandomPlayer
from Players.GreedyPlayer import GreedyPlayer
from Players.JugadorGrupo3 import JugadorGrupo3,AnnBuilder
import numpy as np
import matplotlib.pyplot as plt
import DataTypes
from Players.PositionalPlayer import PositionalPlayer
from Players.MobilityPlayer import MobilityPlayer
from Players.GreedyPlayer import GreedyPlayer

from Torneo import Torneo,AnnBuilder,Aprendiz,Contrincante
'''
aprendices = []
#aprendices.append(Aprendiz("nn", AnnBuilder.Red10(), 2))
#aprendices.append(Aprendiz("nn-no-minmax", AnnBuilder.Red10(), 1))
aprendices.append(Aprendiz("nn-2-layer", AnnBuilder.Red10_8(),1))
contrincantes = []
contrincantes.append(Contrincante("Random",RandomPlayer(DataTypes.SquareType.BLACK)))

torneo = Torneo(aprendices, contrincantes, 100, 100)
torneo.ejecutar()
'''
'''
aprendices = []

aprendices.append(Aprendiz("nn-no-minmax", None, 1))
aprendices.append(Aprendiz("nn-minmax-3", None, 3))
contrincantes = []
contrincantes.append(Contrincante("Random",RandomPlayer(DataTypes.SquareType.BLACK)))

torneo = Torneo(aprendices, contrincantes, 10, 10)
torneo.ejecutar()
'''

aprendices = []
aprendices.append(Aprendiz("nn-50-x3", [],1))
aprendices.append(Aprendiz("nn-x3-no-minmax", [],1))
aprendices.append(Aprendiz("nn10", None, 1))
aprendices.append(Aprendiz("nn50", None, 1))
contrincantes = []
#contrincantes.append(Contrincante("Random",RandomPlayer(DataTypes.SquareType.BLACK)))
#contrincantes.append(Contrincante("Positional",PositionalPlayer(DataTypes.SquareType.BLACK)))
#contrincantes.append(Contrincante("Greedy",GreedyPlayer(DataTypes.SquareType.BLACK)))
#contrincantes.append(Contrincante("Mobility",MobilityPlayer(DataTypes.SquareType.BLACK)))

torneo = Torneo(aprendices, contrincantes, 100, 1)
torneo.comienzoAleatorio = True
torneo.ejecutar()
