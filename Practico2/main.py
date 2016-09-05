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
builder.registrarAtributo("G3", lambda x: int(x)/5)

# Se reduce los valores posibles del atributo "absences" por "Pocas" o "Muchas"
builder.registrarAtributo("absences", lambda x: ('Pocas' if int(x) < 20 else 'Muchas'))

# Utilizamos el builder para obtener todos los objetos estudiante 
# (con los atributos deseados) a partir del archivo .csv
estudiantes = builder.obtenerEstudiantes("DataSets/student-por.csv")
print(str(len(estudiantes)) + " estudiantes cargados")

# Se genera la lista de atributos a considerar en el entrenamiento, partiendo de todos 
# los atributos definidos en el builder, y eliminando los que no queremos usar
atributos = builder.atributos.keys()
atributos.remove("age")
atributos.remove("G3")
atributos.remove("G2")
atributos.remove("Walc")
atributos.remove("G1")

# Se genera una instancia del algoritmo pasandole el atributo objetivo
id3 = Id3("G3")

# Ejecutamos una vez el algoritmo entrenando con todos los estudiantes para obtener
# unas estadisticas iniciales del arbol resultante
arbol = id3.ejecutar(estudiantes, atributos)
arbol.imprimirEstadisticas()
print("Relacion hojas/ejemplos: " + str(float(arbol.cantidadHojas())/len(estudiantes)))
# Dibujante.dibujar(arbol) # Dibuja el arbol para analizarlo graficamente


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

