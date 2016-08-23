# -*- coding: UTF-8 -*-

# Simulador de entrenamiento

from learn import Learner, TipoAprendizaje
from representacion import Representacion
from maquinaAzar import MaquinaAzar
from maquina import Maquina

maquinaA = Maquina(Representacion())
maquinaB = Maquina(Representacion())
maquinaC = Maquina(Representacion())
maquinaD = Maquina(Representacion())
maquinaE = MaquinaAzar(Representacion())
maquinaF = MaquinaAzar(Representacion())

#learner = Learner(maquinaA,maquinaB,0.0001, TipoAprendizaje.APRENDEN_AMBAS_MAQUINAS, "pesos.csv")
#learner.run(30000)
#learner = Learner(maquinaC,maquinaD,0.0001,True)
#learner.run(5000)
#learner = Learner(maquinaA,maquinaC,0.0001,False)
#learner.run(5000)
maquinaA.weights = (8.538528846197535, -8.259931164561259, 4.219982743832252, -0.5303508427873997, -0.13032643613826694, -0.22460043067363522, 0.929435664292774, -0.21989435400207535, 5.630274541538001, -7.022011126636135, 31.786853639915293)
learner = Learner(maquinaA,maquinaE,0.0001,TipoAprendizaje.SIN_APRENDIZAJE)
#maquinaA.DebugOutput = True
#learner.DebugOutput = True
learner.run(1000)
#learner = Learner(maquinaE,maquinaF,0.0001,TipoAprendizaje.SIN_APRENDIZAJE)
#learner.run(1000)

