from estudiante import Atributo,EstudianteBuilder
from arbol import *
from id3 import Id3
from dibujante import Dibujante
from random import shuffle

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
estudiantes = builder.obtenerEstudiantes("DataSets\student-por.csv")
print(str(len(estudiantes)) + " estudiantes cargados")

atributos = builder.atributos.keys()
atributos.remove("age")
atributos.remove("G3")
atributos.remove("G2")
atributos.remove("Walc")
atributos.remove("G1")

id3 = Id3("G3")
arbol = id3.ejecutar(estudiantes, atributos)
arbol.imprimirEstadisticas()
print("Relacion hojas/ejemplos: " + str(float(arbol.cantidadHojas())/len(estudiantes)))
Dibujante.dibujar(arbol)

# Validacion cruzada

# Separo 1/5 de los casos de prueba
cantEstTest = len(estudiantes)/5

shuffle(estudiantes)

estudiantesTest = estudiantes[:cantEstTest]
estudiantesEntrenamiento = estudiantes[cantEstTest + 1:]

TAMANO_BLOQUE = 10

cantBloques = len(estudiantesEntrenamiento)/TAMANO_BLOQUE
resultados = []

for i in range(cantBloques):
    pos = i*TAMANO_BLOQUE
    estTest = estudiantesEntrenamiento[pos:pos+TAMANO_BLOQUE]
    estEntr = estudiantesEntrenamiento[:pos] + estudiantesEntrenamiento[pos+TAMANO_BLOQUE:]
    arbol = id3.ejecutar(estEntr,atributos)
    #print(estTest)
    resultados.append(arbol.validarLista(estTest, "G3"))
    #print ("Resultado validacion " + str(i) + ": " + str(resultados[i] * 100) + "%")

error = sum([r/cantBloques for r in resultados])
print ("Error medio: " + str(1 - error))