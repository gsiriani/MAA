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
CANTIDAD_PRUEBAS = 3

# Separo 1/5 de los casos de prueba
cantEstTest = len(estudiantes)/5

shuffle(estudiantes)

estudiantesTest = estudiantes[:cantEstTest]
estudiantesEntrenamiento = estudiantes[cantEstTest + 1:]

cantEstTest = len(estudiantes)/5
CANT_BLOQUES = 10
largoBloque = len(estudiantesEntrenamiento)/10

validacionFinal1 = 0
validacionFinal1SinPonderar = 0
validacionCruzada1 = 0

validacionFinal3 = 0
validacionFinal3SinPonderar = 0
validacionCruzada3 = 0
ponderaciones = None
for prueba in range(CANTIDAD_PRUEBAS):

    shuffle(estudiantes)
    estudiantesTest = estudiantes[:cantEstTest]
    estudiantesEntrenamiento = estudiantes[cantEstTest + 1:]

    resultados1 = []
    resultados3 = []

    knn = Knn(estudiantesEntrenamiento, "G3", atributos, operadores, ponderaciones)
    knnSinPonderar = Knn(estudiantesEntrenamiento, "G3", atributos, operadores)
    if ponderaciones is None:
        knn.entrenarPonderaciones(10, 3, 0.001, 30)

    validacionFinal1 += knn.validar(estudiantesTest, 1)
    validacionFinal3 += knn.validar(estudiantesTest, 3)
    validacionFinal1SinPonderar += knnSinPonderar.validar(estudiantesTest, 1)
    validacionFinal3SinPonderar += knnSinPonderar.validar(estudiantesTest, 3)

    ponderaciones = knn.ponderaciones
    print ponderaciones

    '''for i in range(CANT_BLOQUES):
        pos = i*largoBloque
        estTest = estudiantesEntrenamiento[pos:pos+largoBloque]
        estEntr = estudiantesEntrenamiento[:pos] + estudiantesEntrenamiento[pos+largoBloque:]

        knn = Knn(estEntr, "G3", atributos, operadores)
        knn.ponderaciones = ponderaciones
        resultados1.append(knn.validar(estTest, 1))
        resultados3.append(knn.validar(estTest, 3))

    validacionCruzada1 += sum([r/CANT_BLOQUES for r in resultados1])
    validacionCruzada3 += sum([r / CANT_BLOQUES for r in resultados3])
    '''
print 'Porcentaje de aciertos:'
print 'Evaluacion por defecto n=1: ' + str(100*validacionFinal1/CANTIDAD_PRUEBAS)
print 'Evaluacion por defecto n=3: ' + str(100*validacionFinal3/CANTIDAD_PRUEBAS)
print 'Evaluacion por defecto sin Ponderar n=1: ' + str(100*validacionFinal1SinPonderar/CANTIDAD_PRUEBAS)
print 'Evaluacion por defecto sin Ponderar n=3: ' + str(100*validacionFinal3SinPonderar/CANTIDAD_PRUEBAS)
