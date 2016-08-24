# -*- coding: UTF-8 -*-
# Este archivo es un ejemplo de ejecucion del algoritmo de entrenamiento

# Simulador de entrenamiento

from learn import Learner, TipoAprendizaje
from representacion import Representacion
from maquinaAzar import MaquinaAzar
from maquina import Maquina, EvaluacionTableroFinal

maquinaEstatica = Maquina(Representacion(), EvaluacionTableroFinal.ESTATICA)
maquinaEstaticaC = Maquina(Representacion(), EvaluacionTableroFinal.ESTATICA)

maquinaDinamica = Maquina(Representacion(), EvaluacionTableroFinal.DIFERENCIA_FICHAS)
maquinaDinamicaC = Maquina(Representacion(), EvaluacionTableroFinal.DIFERENCIA_FICHAS)

maquinaAzar = MaquinaAzar(Representacion())

# Aprendizaje
print("Aprendizaje")
print("EvE")
learner = Learner(maquinaEstatica,maquinaEstaticaC,0.0001, TipoAprendizaje.APRENDEN_AMBAS_MAQUINAS)
learner.run(50)
print("DvD")
learner = Learner(maquinaDinamica,maquinaDinamicaC,0.0001, TipoAprendizaje.APRENDEN_AMBAS_MAQUINAS)
learner.run(50)

print("EvD")
learner = Learner(maquinaEstatica,maquinaDinamica,0.0001, TipoAprendizaje.SOLO_MAQUINA_A_APRENDE)
learner.run(50)
print("DvE")
learner = Learner(maquinaDinamica,maquinaEstatica,0.0001, TipoAprendizaje.SOLO_MAQUINA_A_APRENDE)
learner.run(50)

print("EvA")
learner = Learner(maquinaEstatica,maquinaAzar,0.0001, TipoAprendizaje.SOLO_MAQUINA_A_APRENDE)
learner.run(50)
print("DvA")
learner = Learner(maquinaDinamica,maquinaAzar,0.0001, TipoAprendizaje.SOLO_MAQUINA_A_APRENDE)
learner.run(50)

# Competencia
print("Competenncia")
print("EvD")
learner = Learner(maquinaEstatica,maquinaDinamica,0.0001, TipoAprendizaje.SIN_APRENDIZAJE)
learner.run(100)
print("EvA")
learner = Learner(maquinaEstatica,maquinaAzar,0.0001, TipoAprendizaje.SIN_APRENDIZAJE)
learner.run(100)
print("DvA")
learner = Learner(maquinaDinamica,maquinaAzar,0.0001, TipoAprendizaje.SIN_APRENDIZAJE)
learner.run(100)