# -*- coding: utf-8 -*-
import DataTypes
from Players.GreedyPlayer import GreedyPlayer
from Players.MobilityPlayer import MobilityPlayer
from Players.PositionalPlayer import PositionalPlayer
from Players.RandomPlayer import RandomPlayer
from Torneo import Torneo, Aprendiz, Contrincante
import os

aprendices = []
aprendices.append(Aprendiz(os.path.join("redes","otras","nn-50-x3"), [],1))
aprendices.append(Aprendiz(os.path.join("redes","nn-50-50-x3"), [],3))
aprendices.append(Aprendiz(os.path.join("redes","otras","nn-x3-no-minmax"), [],1))
aprendices.append(Aprendiz(os.path.join("redes","otras","nn10"), None, 1))
aprendices.append(Aprendiz(os.path.join("redes","otras","nn50"), None, 1))
contrincantes = []
contrincantes.append(Contrincante("Random",RandomPlayer(DataTypes.SquareType.BLACK)))
contrincantes.append(Contrincante("Positional",PositionalPlayer(DataTypes.SquareType.BLACK)))
contrincantes.append(Contrincante("Greedy",GreedyPlayer(DataTypes.SquareType.BLACK)))
contrincantes.append(Contrincante("Mobility",MobilityPlayer(DataTypes.SquareType.BLACK)))

torneo = Torneo(aprendices, contrincantes, 30, 1)
torneo.comienzoAleatorio = True
torneo.ejecutar()
