from random import shuffle
from setup import Setup
from Knn import Knn
from OperadoresBuilder import OperadoresBuilder

Setup.setup()

atributos = Setup.atributos
estudiantes = Setup.estudiantes
valoresPosibles = Setup.valoresPosibles

operadores = {}

OperadoresBuilder.multiple(operadores, OperadoresBuilder.hamming, ["school", "sex", "schoolsup", "famsup", "paid",
                                                                   "activities", "nursery", "higher", "internet",
                                                                   "romantic", "address", "famsize", "Pstatus",
                                                                   "Mjob", "Fjob", "reason", "guardian"])

OperadoresBuilder.multiple(operadores, OperadoresBuilder.rango, ["age","Medu","Fedu",
                                    "traveltime","studytime","failures","famrel",
                                    "freetime","goout","Dalc","Walc","health","absences"], valoresPosibles)

knn = Knn(estudiantes, "G3", atributos, operadores)


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

validacionFinal1 = 0
validacionCruzada1 = 0

validacionFinal3 = 0
validacionCruzada3 = 0

for prueba in range(CANTIDAD_PRUEBAS):

    shuffle(estudiantes)
    estudiantesTest = estudiantes[:cantEstTest]
    estudiantesEntrenamiento = estudiantes[cantEstTest + 1:]

    resultados1 = []
    resultados3 = []

    for i in range(CANT_BLOQUES):
        pos = i*largoBloque
        estTest = estudiantesEntrenamiento[pos:pos+largoBloque]
        estEntr = estudiantesEntrenamiento[:pos] + estudiantesEntrenamiento[pos+largoBloque:]

        knn = Knn(estEntr, "G3", atributos, operadores)
        resultados1.append(knn.validar(estTest,1))
        resultados3.append(knn.validar(estTest, 3))

    validacionCruzada1 += sum([r/CANT_BLOQUES for r in resultados1])
    validacionCruzada3 += sum([r / CANT_BLOQUES for r in resultados3])

    knn = Knn(estudiantesEntrenamiento, "G3", atributos, operadores)
    validacionFinal1 += knn.validar(estudiantesTest,1)
    validacionFinal3 += knn.validar(estudiantesTest, 3)

print 'Porcentaje de aciertos:'
print 'Validacion Cruzada n=1: ' + str(100*validacionCruzada1/CANTIDAD_PRUEBAS)
print 'Evaluacion por defecto n=1: ' + str(100*validacionFinal1/CANTIDAD_PRUEBAS)
print 'Validacion Cruzada n=3: ' + str(100*validacionCruzada3/CANTIDAD_PRUEBAS)
print 'Evaluacion por defecto n=3: ' + str(100*validacionFinal3/CANTIDAD_PRUEBAS)
