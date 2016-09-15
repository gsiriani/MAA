from estudiante import Atributo,EstudianteBuilder
# from arbol import *
# from id3 import Id3
from bayes import Bayes
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
builder.registrarAtributoParticionado("G3",4,1,20)
builder.registrarAtributoParticionado("famrel")
builder.registrarAtributoParticionado("freetime")
builder.registrarAtributoParticionado("goout")
builder.registrarAtributoParticionado("Dalc")
builder.registrarAtributoParticionado("Walc")
builder.registrarAtributoParticionado("health")
builder.registrarAtributoParticionado("absences",4,0,40)

# Utilizamos el builder para obtener todos los objetos estudiante
# (con los atributos deseados) a partir del archivo .csv
estudiantes = builder.obtenerEstudiantes("DataSets/student-por.csv")
valoresPosibles = builder.obtenerValoresPosibles(estudiantes)
print(str(len(estudiantes)) + " estudiantes cargados")

# Se genera la lista de atributos a considerar en el entrenamiento, partiendo de todos
# los atributos definidos en el builder, y eliminando los que no queremos usar
atributos = builder.atributos.keys()
#atributos.remove("G3")
atributos.remove("G2")
atributos.remove("G1")
atributos.remove("age")

# Se genera una instancia del algoritmo pasandole el atributo objetivo
# id3 = Id3("G3",valoresPosibles)
bayes = Bayes("G3", atributos, valoresPosibles)



# ------------------
# VALIDACION DE BAYES
# ------------------


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
validacionFinal = 0
validacionAjuste = {}
MAX_AJUSTE = 5
for i in range(1, MAX_AJUSTE):
    validacionAjuste[i] = 0

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
        # arbol = id3.ejecutar(estEntr,atributos)
        # resultados.append(arbol.validarLista(estTest, "G3"))
        (p, pc) = bayes.ejecutar(ejemplos= estEntr)
        resultados.append(bayes.validarLista(estTest, p, pc))

    validacionCruzada += sum([r/CANT_BLOQUES for r in resultados])


    # Entreno el arbol con estudiantesEntrenamiento y lo valido con estudiantesTest
    # arbol = id3.ejecutar(estudiantesEntrenamiento, atributos)
    # validacionFinal += arbol.validarLista(estudiantesTest, "G3")
    (p, pc) = bayes.ejecutar(ejemplos= estudiantesEntrenamiento)
    validacionFinal += bayes.validarLista(estudiantesTest, p, pc)

    for i in range(1, MAX_AJUSTE):
        # arbol = id3.ejecutar(estudiantesEntrenamiento, atributos, maxDepth = i)
        # validacionAjuste[i] += arbol.validarLista(estudiantesTest, "G3")
        (p, pc) = bayes.ejecutar(ejemplos= estudiantesEntrenamiento, ajuste= i)
        validacionAjuste[i] += bayes.validarLista(estudiantesTest, p, pc)


print 'Porcentaje de aciertos:'
print 'Valor mas probable: ' + str(100*validacionMasProbable/CANTIDAD_PRUEBAS)
print 'Validacion Cruzada: ' + str(100*validacionCruzada/CANTIDAD_PRUEBAS)
print 'Evaluacion por defecto: ' + str(100*validacionFinal/CANTIDAD_PRUEBAS)
for i in range(1,MAX_AJUSTE):
    print 'Evaluacion profundidad ' + str(i) + ': ' + str(100*validacionAjuste[i]/CANTIDAD_PRUEBAS)
