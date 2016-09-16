class TipoHijo:
    '''
    Enumerado para identificar el tipo de hoja.
    '''
    UNICO = 0
    MAYORIA = 1,
    ELSE = 2,
    PODA = 3

class Arbol:
    '''
    Arbol de desicion resultado del entrenamiento
    '''

    def __init__(self, valor, tipoHijo = None):
        '''
        Crea un nuevo arbol.
        Atributos:
            - valor: si el nodo es una hoja, valor es el valor de la misma.
                        En caso contrario, es el atributo que se considera en la rama.
            - hijos: diccionario que contiene un arbol para cada valor disponible del atributo
                        y una entrada extra (ELSE) para los valores no considerados durante el entrenamiento.
            - tipoHijo: si el arbol es una hoja, tipoHijo es el tipo de la hoja
        '''

        self.valor = valor
        self.hijos = {}
        self.ganancia = 0
        self.gananciaRelativa = 0
        self.tipoHijo = tipoHijo

    def agregarRama(self, etiqueta, arbol):
        '''
        Agrega una rama al arbol. La etiqueta representa el valor del atributo considerado.
        '''
        self.hijos[etiqueta] = arbol

    def alturaMaxima(self):
        '''
        Maxima distancia entre la raiz y una hoja
        '''
        return 1 + (max([h.alturaMaxima() for h in self.hijos.values()]) if len(self.hijos) > 0 else 0)

    def alturaMinima(self):
        '''
        Minima distancia entre la raiz y una hoja
        '''
        return 1 + (min([h.alturaMinima() for h in self.hijos.values()]) if len(self.hijos) > 0 else 0)

    def cantidadHojas(self):
        return sum([h.cantidadHojas() for h in self.hijos.values()]) if len(self.hijos) > 0 else 1

    def cantidadHojasAprendidas(self):
        valor = 1 if self.tipoHijo == TipoHijo.UNICO or self.tipoHijo == TipoHijo.MAYORIA else 0
        return sum([h.cantidadHojasAprendidas() for h in self.hijos.values()]) if len(self.hijos) > 0 else valor


    def imprimirEstadisticas(self):
        print("Altura maxima: " + str(self.alturaMaxima()))
        print("Altura minima: " + str(self.alturaMinima()))
        print("Cantidad de hojas: " + str(self.cantidadHojas()))
        print("Cantidad de hojas aprendidas: " + str(self.cantidadHojasAprendidas()))


    def validarLista(self, datos, valorObjetivo):
        '''
        Retorna la probabilidad de acierto del arbol dado un conjunto de datos
        de prueba y un valorObjetivo
        '''
        return sum([(1 if self.validar(c, valorObjetivo) else 0) for c in datos])/float(len(datos))

    def validar(self, caso, valorObjetivo):
        '''
        Retorna True si el valor de la hoja en la que desemboca el caso de prueba a traves del
        arbol conicide con el valor del atributo valorObjetivo del caso; False en caso contrario
        '''
        if len(self.hijos) == 0:
            return self.valor == caso[valorObjetivo]
        else:
            valor = caso[self.valor]

            hijo = self.hijos[valor]

            return hijo.validar(caso, valorObjetivo)

    def esHoja(self):
        return len(self.hijos) == 0

    def podar(self):

        if self.esHoja():
            return

        for h in self.hijos.values():
            h.podar()

        valorPrimerHijo = self.hijos.values()[0].valor

        if all([h.esHoja() and h.valor == valorPrimerHijo for h in self.hijos.values()]):
            self.hijos = {}
            self.valor = valorPrimerHijo
            self.tipoHijo = TipoHijo.PODA




