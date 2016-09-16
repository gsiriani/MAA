from estudiante import Atributo,EstudianteBuilder

class Setup():

    @staticmethod
    def setup():

        # Generamos un nuevo constructor que, a partir de una linea de archivo .csv, construye
        # un objeto de tipo Estudiante con los atributos deseados.
        # Esto nos permite decidir que atributos utilizar y cuales son los posibles valores de cada uno.
        Setup.builder = EstudianteBuilder()

        # En principio registramos todos los atributos disponibles con sus valores por defecto.
        Setup.builder.registrarAtributos(["school","sex","age","address",
                                    "famsize","Pstatus","Medu","Fedu",
                                    "Mjob","Fjob","reason","guardian",
                                    "traveltime","studytime","failures",
                                    "schoolsup","famsup","paid","activities",
                                    "nursery","higher","internet","romantic","famrel",
                                    "freetime","goout","Dalc","Walc","health","absences",
                                    "G1","G2"])

        # Al atributo objetivo G3 se le cambia la lista de valores posibles para simplificar el
        # algoritmo.
        Setup.builder.registrarAtributoParticionado("G3",4,1,20)
        Setup.builder.registrarAtributoParticionado("famrel")
        Setup.builder.registrarAtributoParticionado("freetime")
        Setup.builder.registrarAtributoParticionado("goout")
        Setup.builder.registrarAtributoParticionado("Dalc")
        Setup.builder.registrarAtributoParticionado("Walc")
        Setup.builder.registrarAtributoParticionado("health")
        Setup.builder.registrarAtributoParticionado("absences",4,0,40)

        # Utilizamos el builder para obtener todos los objetos estudiante
        # (con los atributos deseados) a partir del archivo .csv
        Setup.estudiantes = Setup.builder.obtenerEstudiantes("DataSets/student-por.csv")
        Setup.valoresPosibles = Setup.builder.obtenerValoresPosibles(Setup.estudiantes)
        print(str(len(Setup.estudiantes)) + " estudiantes cargados")

        # Se genera la lista de atributos a considerar en el entrenamiento, partiendo de todos
        # los atributos definidos en el builder, y eliminando los que no queremos usar
        Setup.atributos = Setup.builder.atributos.keys()
        #atributos.remove("G3")
        Setup.atributos.remove("G2")
        Setup.atributos.remove("G1")
        Setup.atributos.remove("age")
