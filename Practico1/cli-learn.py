# -*- coding: UTF-8 -*-

from learn import Learner, Representacion, Maquina

maquinaA = Maquina(Representacion())
maquinaB = Maquina(Representacion())

learner = Learner(maquinaA,maquinaB,0.001,False)
learner.run(2000)
learner = Learner(maquinaA,maquinaB,0.001,False)
learner.run(1000, True)
