# -*- coding: utf-8 -*-

from CustomBatchGame import CustomBatchGame
from Players.RandomPlayer import RandomPlayer
from Players.GreedyPlayer import GreedyPlayer
from Players.JugadorGrupo3 import JugadorGrupo3,AnnBuilder
import numpy as np
import matplotlib.pyplot as plt
import DataTypes
from Torneo import Torneo,AnnBuilder,Aprendiz,Contrincante

aprendices = []
aprendices.append(Aprendiz("nn-x3", [AnnBuilder.Red10(),AnnBuilder.Red10(),AnnBuilder.Red10()],1))
contrincantes = []
contrincantes.append(Contrincante("Random",RandomPlayer(DataTypes.SquareType.BLACK)))

torneo = Torneo(aprendices, contrincantes, 100, 100)
torneo.ejecutar()

