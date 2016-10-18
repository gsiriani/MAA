# -*- coding: utf-8 -*-
import os
import DataTypes
from Players.RandomPlayer import RandomPlayer
from Torneo import Torneo,Aprendiz,Contrincante, AnnBuilder
import matplotlib.pyplot as plt

aprendices = []
aprendices.append(Aprendiz(os.path.join("redes","otras","nn-50-x3"), [],3))
contrincantes = []
contrincantes.append(Contrincante("Random",RandomPlayer(DataTypes.SquareType.BLACK)))

torneo = Torneo(aprendices, contrincantes, 20, 1)
torneo.ejecutar()

plt.clf()
plt.plot(torneo.aprendices[0].jugador.usoCache)
plt.show()
