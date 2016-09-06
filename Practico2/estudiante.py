import csv

class EstudianteBuilder:

    atributos = {}

    def registrarAtributo(self, nombre, conversor):

        self.atributos[nombre] = Atributo(conversor)

    def registrarAtributos(self, lista):

        for a in lista:
            self.atributos[a] = Atributo()

    def obtenerEstudiantes(self,archivo):

        estudiantes = []

        with open(archivo, 'rb') as csvFile:

            reader = csv.DictReader(csvFile, delimiter=';', quotechar='"')

            for linea in reader:
                e = self.convertirEstudiante(linea)
                estudiantes.append(e)

        return estudiantes

    def obtenerValoresPosibles(self, lineas):

        valores = {}

        for linea in lineas:
            for k, v in linea.iteritems():

                if not k in valores:
                    valores[k] = set()

                valores[k].add(v)

        return valores

    def convertirEstudiante(self, lineaEstudiante):

        estudiante = {}

        for k,v in lineaEstudiante.iteritems():
            if k in self.atributos:
                fnConversor = self.atributos[k].conversor
                estudiante[k] = fnConversor(v)

        return estudiante

class Atributo:

    def __init__(self, conversor = lambda x: x):
        self.conversor = conversor