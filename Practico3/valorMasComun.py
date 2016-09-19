from estudiante import Atributo,EstudianteBuilder

from random import shuffle
from setup import Setup

Setup.setup()

atributos = Setup.atributos
estudiantes = Setup.estudiantes
valoresPosibles = Setup.valoresPosibles


# -----------------------------
# VALIDACION DE VALOR MAS COMUN
# -----------------------------


# Se realizaran multiples pruebas para obtener una estimacion de la efectividad del algoritmo
# para cualquier eleccion de casos de entrenamiento / prueba
CANTIDAD_PRUEBAS = 100

# Separo 1/5 de los casos de prueba
cantEstTest = len(estudiantes)/5

shuffle(estudiantes)

estudiantesTest = estudiantes[:cantEstTest]
estudiantesEntrenamiento = estudiantes[cantEstTest + 1:]

cantEstTest = len(estudiantes)/5
CANT_BLOQUES = 10
largoBloque = len(estudiantesEntrenamiento)/10

validacionMasProbable = 0
validacionCruzada = 0

for prueba in range(CANTIDAD_PRUEBAS):

    shuffle(estudiantes)
    estudiantesTest = estudiantes[:cantEstTest]
    estudiantesEntrenamiento = estudiantes[cantEstTest + 1:]

    # Obtengo porcentaje de aciertos sugiriendo opcion mas probable
    cant = {}
    for v in valoresPosibles["G3"]:
        cant[v] = len([e for e in estudiantesEntrenamiento if e["G3"] == v])
    masProbable = max(cant.iteritems(), key=lambda (k, v): v)[0]
    correctos = 0
    for e in estudiantesTest:
        if e["G3"] == masProbable:
            correctos += 1
    validacionMasProbable += float(correctos)/len(estudiantesTest)

    resultados = []

    for i in range(CANT_BLOQUES):
        pos = i*largoBloque
        estTest = estudiantesEntrenamiento[pos:pos+largoBloque]
        estEntr = estudiantesEntrenamiento[:pos] + estudiantesEntrenamiento[pos+largoBloque:]
        cant = {}
        for v in valoresPosibles["G3"]:
            cant[v] = len([e for e in estEntr if e["G3"] == v])
        masProbable = max(cant.iteritems(), key=lambda (k, v): v)[0]
        correctos = 0
        for e in estTest:
            if e["G3"] == masProbable:
                correctos += 1
        resultados.append(float(correctos)/len(estTest))

    validacionCruzada += sum([r/CANT_BLOQUES for r in resultados])

print 'Porcentaje de aciertos:'
print 'Valor mas probable: ' + str(100*validacionMasProbable/CANTIDAD_PRUEBAS)
print 'Validacion Cruzada: ' + str(100*validacionCruzada/CANTIDAD_PRUEBAS)