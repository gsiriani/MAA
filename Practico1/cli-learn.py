# -*- coding: UTF-8 -*-

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

learner = Learner(maquinaA,maquinaB,0.0001, TipoAprendizaje.APRENDEN_AMBAS_MAQUINAS, "pesos.csv")
learner.run(30000)
#learner = Learner(maquinaC,maquinaD,0.0001,True)
#learner.run(5000)
#learner = Learner(maquinaA,maquinaC,0.0001,False)
#learner.run(5000)
learner = Learner(maquinaA,maquinaE,0.0001,TipoAprendizaje.SIN_APRENDIZAJE)
#maquinaA.DebugOutput = True
#learner.DebugOutput = True
learner.run(1000)
#learner = Learner(maquinaE,maquinaF,0.0001,TipoAprendizaje.SIN_APRENDIZAJE)
#learner.run(1000)

