# -*- coding: UTF-8 -*-

# Simulador de entrenamiento

from learn import Learner, TipoAprendizaje
from representacion import Representacion
from maquinaAzar import MaquinaAzar
from maquina import Maquina, EvaluacionTableroFinal

maquinaEstatica = Maquina(Representacion(), EvaluacionTableroFinal.ESTATICA)
maquinaAzar = MaquinaAzar(Representacion())

maquinaEstatica.weights = (26.187072695411917, -32.84680592423919, 13.213702407264911,
                           57.504267170163494, 21.574640421320762, -23.00357084783828,
                           -1.193679277554918, 1.9201039975176828, 20.288830091323383,
                           -16.56871602519243, -80.97633510212901)

learner = Learner(maquinaEstatica,maquinaAzar,0.0001, TipoAprendizaje.SIN_APRENDIZAJE)

maquinaEstatica.DebugOutput = True
learner.DebugOutput = True

learner.run(1)