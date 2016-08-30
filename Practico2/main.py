from estudiante import Atributo,EstudianteBuilder
from arbol import *
from id3 import Id3
from dibujante import Dibujante

builder = EstudianteBuilder()

builder.registrarAtributos(["school","sex","age","address",
                            "famsize","Pstatus","Medu","Fedu",
                            "Mjob","Fjob","reason","guardian",
                            "traveltime","studytime","failures",
                            "schoolsup","famsup","paid","activities",
                            "nursery","higher","internet","romantic","famrel",
                            "freetime","goout","Dalc","Walc","health","absences",
                            "G1","G2"])
builder.registrarAtributo("G3", lambda x: ('Reprobado' if int(x) < 10 else 'Aprobado'))
builder.registrarAtributo("absences", lambda x: ('Nerd' if int(x) < 20 else 'Falton'))
estudiantes = builder.obtenerEstudiantes("DataSets\student-mat.csv")
print(str(len(estudiantes)) + " estudiantes cargados")

atributos = builder.atributos.keys()
atributos.remove("age")
atributos.remove("G3")
atributos.remove("G2")
atributos.remove("Walc")
atributos.remove("G1")

id3 = Id3("G3")
arbol = id3.ejecutar(estudiantes, atributos, 4)

Dibujante.dibujar(arbol)