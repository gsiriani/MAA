class TipoHijo:
    '''
    Enumerado para identificar el tipo de hoja.
    '''
    UNICO = 0
    MAYORIA = 1,
    ELSE = 2

class Arbol:
    '''
    Arbol de desicion resultado del entrenamiento
    '''

    VALOR_ELSE = "*ELSE*"

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

    def agregarRamaElse(self, arbol):
        '''
        Rama auxiliar que se agrega para abarcar los casos no considerados en el entrenamiento.
        '''
        self.hijos[Arbol.VALOR_ELSE] = arbol

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


    def imprimirEstadisticas(self):        
        print("Altura maxima: " + str(self.alturaMaxima()))
        print("Altura minima: " + str(self.alturaMinima()))
        print("Cantidad de hojas: " + str(self.cantidadHojas()))

    
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

            if valor not in self.hijos:
                return self.hijos[Arbol.VALOR_ELSE].validar(caso, valorObjetivo)

            hijo = self.hijos[valor]

            return hijo.validar(caso, valorObjetivo)


