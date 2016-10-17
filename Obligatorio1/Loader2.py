# -*- coding: utf-8 -*-

import DataTypes
from Players.RandomPlayer import RandomPlayer
from Torneo import Torneo,Aprendiz,Contrincante, AnnBuilder

aprendices = []
aprendices.append(Aprendiz("nn-50-50-x3", [AnnBuilder.Red50_50(),AnnBuilder.Red50_50(),AnnBuilder.Red50_50()],3))
contrincantes = []
contrincantes.append(Contrincante("Random",RandomPlayer(DataTypes.SquareType.BLACK)))

torneo = Torneo(aprendices, contrincantes, 1, 1)
torneo.ejecutar()

