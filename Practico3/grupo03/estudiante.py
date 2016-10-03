import csv
import math

class EstudianteBuilder:
    '''
    Esta clase es utilizada para construir estudiantes a partir de archivos .csv
    y una lista de atributos (con funciones de conversion de valores) a considerar
    '''

    atributos = {}

    def registrarAtributo(self, nombre, conversor):
        '''
        Agrega un nuevo atributo a considerar junto con la funcion que a partir del
        valor en el .csv, le otorga un valor adecuado a nuestro modelo
        '''
        self.atributos[nombre] = Atributo(conversor)

    def registrarAtributoParticionado(self, nombre, particiones = 3,min = 1, max = 5):
        '''
        Agrega un nuevo atributo a considerar junto con la funcion que a partir del
        valor en el .csv, le otorga un valor adecuado a nuestro modelo
        '''
        tamano = float(max - min)/particiones
        self.atributos[nombre] = Atributo(lambda x: int(math.floor((float(x) - min) / tamano)))

    def registrarAtributoParticionadoPorLista(self, nombre, puntos):
        '''
        Agrega un nuevo atributo a considerar junto con la funcion que a partir del
        valor en el .csv, le otorga un valor adecuado a nuestro modelo
        '''

        puntosOrdenados = list(puntos)
        puntosOrdenados.sort()

        def obtenerParticion(x):
            for i in range(len(puntosOrdenados)):
                if x <= puntosOrdenados[i]:
                    return i

            return len(puntosOrdenados)


        self.atributos[nombre] = Atributo(obtenerParticion)


    def registrarAtributos(self, lista):
        '''
        Agrega una lista de atributos con la funcion id como conversor de valores
        por defecto
        '''
        for a in lista:
            self.atributos[a] = Atributo()

    def obtenerEstudiantes(self,archivo):
        '''
        Retorna una lista de objetos estudiante a partir de un archivo .csv
        que tiene los valores para cada atributo de cada estudiante.
        '''

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
        '''
        A partir de una linea del archivo .csv con los valores de los atributos de
        un estudiante, retorna un estudiante (codificado como un diccionario) con
        los valores de sus atributos modificados mediante las funciones de conversion
        especificadas para cada atributo del builder.
        '''
        estudiante = {}

        for k,v in lineaEstudiante.iteritems():
            if k in self.atributos:
                fnConversor = self.atributos[k].conversor
                estudiante[k] = fnConversor(v)

        return estudiante

class Atributo:
    '''
    Clase auxiliar que almacena la funcion de conversion de valor de los atributos 
    '''
    def __init__(self, conversor = lambda x: x):
        '''
        La funcion de conversion por defecto es la funcion identidad
        '''
        self.conversor = conversor