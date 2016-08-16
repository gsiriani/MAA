# -*- coding: UTF-8 -*-

from learn import Learner
from representacion import Representacion
from maquinaAzar import MaquinaAzar
from maquina import Maquina

maquinaA = Maquina(Representacion())
maquinaB = Maquina(Representacion())
maquinaC = Maquina(Representacion())
maquinaD = Maquina(Representacion())
maquinaE = MaquinaAzar(Representacion())

learner = Learner(maquinaA,maquinaB,0.0001, True)
learner.run(5000)
#learner = Learner(maquinaC,maquinaD,0.0001,True)
#learner.run(5000)
#learner = Learner(maquinaA,maquinaC,0.0001,False)
#learner.run(5000)
learner = Learner(maquinaA,maquinaE,0.0001,False)
learner.run(1000, True)
