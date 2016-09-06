from estudiante import Atributo,EstudianteBuilder
from arbol import *
from id3 import Id3
from dibujante import Dibujante
from random import shuffle
# from dibujante import Dibujante # Utilizado para dibujar el arbol. Requiere bibliotecas extra

builder = EstudianteBuilder()

builder.registrarAtributos(["school","sex","age","address",
                            "famsize","Pstatus","Medu","Fedu",
                            "Mjob","Fjob","reason","guardian",
                            "traveltime","studytime","failures",
                            "schoolsup","famsup","paid","activities",
                            "nursery","higher","internet","romantic","famrel",
                            "freetime","goout","Dalc","Walc","health","absences",
                            "G1","G2"])
builder.registrarAtributo("G3", lambda x: int(x)/5)
builder.registrarAtributo("absences", lambda x: ('Nerd' if int(x) < 20 else 'Falton'))
estudiantes = builder.obtenerEstudiantes("DataSets/student-por.csv")
valoresPosibles = builder.obtenerValoresPosibles(estudiantes)
print(str(len(estudiantes)) + " estudiantes cargados")

atributos = builder.atributos.keys()
atributos.remove("age")
atributos.remove("G3")
atributos.remove("G2")
atributos.remove("Walc")
atributos.remove("G1")

id3 = Id3("G3",valoresPosibles)
arbol = id3.ejecutar(estudiantes, atributos)
arbol.imprimirEstadisticas()
print("Relacion hojas/ejemplos: " + str(float(arbol.cantidadHojas())/len(estudiantes)))

Dibujante.dibujar(arbol)

# ------------------
# VALIDACION CRUZADA
# ------------------

print "Validacion cruzada..."

# Separo 1/5 de los casos de prueba
cantEstTest = len(estudiantes)/5

shuffle(estudiantes)

estudiantesTest = estudiantes[:cantEstTest]
estudiantesEntrenamiento = estudiantes[cantEstTest + 1:]


CANT_BLOQUES = 10

largoBloque = len(estudiantesEntrenamiento)/10

resultados = []

for i in range(CANT_BLOQUES):
    pos = i*largoBloque
    estTest = estudiantesEntrenamiento[pos:pos+largoBloque]
    estEntr = estudiantesEntrenamiento[:pos] + estudiantesEntrenamiento[pos+largoBloque:]
    arbol = id3.ejecutar(estEntr,atributos)
    resultados.append(arbol.validarLista(estTest, "G3"))

aciertos = sum([r/CANT_BLOQUES for r in resultados])
print ("Error medio: " + str(1 - aciertos))


# ------------------
# EVALUACION FINAL
# ------------------

print "Evaluacion final..."

arbol = id3.ejecutar(estudiantesEntrenamiento, atributos)
aciertos = arbol.validarLista(estudiantesTest, "G3")
print "Error: " + str(1 - aciertos)

