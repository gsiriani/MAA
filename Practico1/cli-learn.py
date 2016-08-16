# -*- coding: UTF-8 -*-

from learn import Learner, Representacion, Maquina, MaquinaAzar

maquinaA = Maquina(Representacion())
maquinaB = Maquina(Representacion())
maquinaC = MaquinaAzar(Representacion())

learner = Learner(maquinaA,maquinaB,0.0001,True)
learner.run(10000)
learner = Learner(maquinaA,maquinaC,0.0001,False)
learner.run(1000, True)
