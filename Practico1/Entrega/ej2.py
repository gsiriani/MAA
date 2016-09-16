# -*- coding: UTF-8 -*-

# Simulador de entrenamiento

from learn import Learner, TipoAprendizaje
from representacion import Representacion
from maquinaAzar import MaquinaAzar
from maquina import Maquina, EvaluacionTableroFinal

maquinaEstatica = Maquina(Representacion(), EvaluacionTableroFinal.ESTATICA)
maquinaEstaticaC = Maquina(Representacion(), EvaluacionTableroFinal.ESTATICA)

maquinaDinamica = Maquina(Representacion(), EvaluacionTableroFinal.DIFERENCIA_FICHAS)
maquinaDinamicaC = Maquina(Representacion(), EvaluacionTableroFinal.DIFERENCIA_FICHAS)

learner = Learner(maquinaEstatica,maquinaEstaticaC,0.0001, TipoAprendizaje.APRENDEN_AMBAS_MAQUINAS,
                  fileOutput= "pesosE.csv")
learner.run(5000)

learner = Learner(maquinaDinamica,maquinaDinamicaC,0.0001, TipoAprendizaje.APRENDEN_AMBAS_MAQUINAS,
                  fileOutput= "pesosD.csv")
learner.run(5000)