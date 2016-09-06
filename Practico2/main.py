from estudiante import Atributo,EstudianteBuilder
from arbol import *
from id3 import Id3
from random import shuffle
# from dibujante import Dibujante # Utilizado para dibujar el arbol. Requiere bibliotecas extra

# Generamos un nuevo constructor que, a partir de una linea de archivo .csv, construye
# un objeto de tipo Estudiante con los atributos deseados.
# Esto nos permite decidir que atributos utilizar y cuales son los posibles valores de cada uno.
builder = EstudianteBuilder()

# En principio registramos todos los atributos disponibles con sus valores por defecto.
builder.registrarAtributos(["school","sex","age","address",
                            "famsize","Pstatus","Medu","Fedu",
                            "Mjob","Fjob","reason","guardian",
                            "traveltime","studytime","failures",
                            "schoolsup","famsup","paid","activities",
                            "nursery","higher","internet","romantic","famrel",
                            "freetime","goout","Dalc","Walc","health","absences",
                            "G1","G2"])

# Al atributo objetivo G3 se le cambia la lista de valores posibles para simplificar el
# algoritmo.
builder.registrarAtributoParticionado("G3",3,1,20)
builder.registrarAtributoParticionado("G2",3,1,20)
builder.registrarAtributoParticionado("G1",3,1,20)
builder.registrarAtributoParticionado("famrel")
builder.registrarAtributoParticionado("freetime")
builder.registrarAtributoParticionado("goout")
builder.registrarAtributoParticionado("Dalc")
builder.registrarAtributoParticionado("Walc")
builder.registrarAtributoParticionado("health")

# Utilizamos el builder para obtener todos los objetos estudiante
# (con los atributos deseados) a partir del archivo .csv
estudiantes = builder.obtenerEstudiantes("DataSets/student-por.csv")
valoresPosibles = builder.obtenerValoresPosibles(estudiantes)
print(str(len(estudiantes)) + " estudiantes cargados")

# Se genera la lista de atributos a considerar en el entrenamiento, partiendo de todos
# los atributos definidos en el builder, y eliminando los que no queremos usar
atributos = builder.atributos.keys()
atributos.remove("G3")
atributos.remove("G2")
atributos.remove("G1")
atributos.remove("age")

# Se genera una instancia del algoritmo pasandole el atributo objetivo
id3 = Id3("G3",valoresPosibles)

# Ejecutamos una vez el algoritmo entrenando con todos los estudiantes para obtener
# unas estadisticas iniciales del arbol resultante
arbol = id3.ejecutar(estudiantes, atributos)
arbol.imprimirEstadisticas()
print("Relacion hojas/ejemplos: " + str(float(arbol.cantidadHojas())/len(estudiantes)))
print("Relacion hojas aprendidas/ejemplos: " + str(float(arbol.cantidadHojasAprendidas())/len(estudiantes)))
arbol.podar()
print("Podado del arbol")
arbol.imprimirEstadisticas()
print("Relacion hojas/ejemplos: " + str(float(arbol.cantidadHojas())/len(estudiantes)))
print("Relacion hojas aprendidas/ejemplos: " + str(float(arbol.cantidadHojasAprendidas())/len(estudiantes)))
# Dibujante.dibujar(arbol)

# ------------------
# VALIDACION CRUZADA
# ------------------

print "Validacion cruzada..."

# Separo 1/5 de los casos de prueba
cantEstTest = len(estudiantes)/5

shuffle(estudiantes)

estudiantesTest = estudiantes[:cantEstTest]
estudiantesEntrenamiento = estudiantes[cantEstTest + 1:]

# Realizo validacion cruzada sobre estudiantesEntrenamiento
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

# Entreno el arbol con estudiantesEntrenamiento y lo valido con estudiantesTest
arbol = id3.ejecutar(estudiantesEntrenamiento, atributos)
aciertos = arbol.validarLista(estudiantesTest, "G3")
print "Error: " + str(1 - aciertos)



# Se realizaran multiples pruebas para obtener una estimacion de la efectividad del algoritmo
# para cualquier eleccion de casos de entrenamiento / prueba
CANTIDAD_PRUEBAS = 25

cantEstTest = len(estudiantes)/5
CANT_BLOQUES = 10
largoBloque = len(estudiantesEntrenamiento)/10

validacionCruzada = 0
validacionFinal = 0
validacionPodas = {}
MAX_RAMAS = 10
for i in range(1, MAX_RAMAS):
    validacionPodas[i] = 0

for prueba in range(CANTIDAD_PRUEBAS):

    shuffle(estudiantes)
    estudiantesTest = estudiantes[:cantEstTest]
    estudiantesEntrenamiento = estudiantes[cantEstTest + 1:]

    resultados = []

    for i in range(CANT_BLOQUES):
        pos = i*largoBloque
        estTest = estudiantesEntrenamiento[pos:pos+largoBloque]
        estEntr = estudiantesEntrenamiento[:pos] + estudiantesEntrenamiento[pos+largoBloque:]
        arbol = id3.ejecutar(estEntr,atributos)
        resultados.append(arbol.validarLista(estTest, "G3"))

    validacionCruzada += sum([r/CANT_BLOQUES for r in resultados])


    # Entreno el arbol con estudiantesEntrenamiento y lo valido con estudiantesTest
    arbol = id3.ejecutar(estudiantesEntrenamiento, atributos)
    validacionFinal += arbol.validarLista(estudiantesTest, "G3")

    for i in range(1, MAX_RAMAS):
        arbol = id3.ejecutar(estudiantesEntrenamiento, atributos, maxDepth = i)
        validacionPodas[i] += arbol.validarLista(estudiantesTest, "G3")


print 'Porcentaje de aciertos aciertos:'
print 'Validacion Cruzada: ' + str(100*validacionCruzada/CANTIDAD_PRUEBAS)
print 'Evaluacion sin poda: ' + str(100*validacionFinal/CANTIDAD_PRUEBAS)
for i in range(1,MAX_RAMAS):
    print 'Evaluacion profundidad ' + str(i) + ': ' + str(100*validacionPodas[i]/CANTIDAD_PRUEBAS)
