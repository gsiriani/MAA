from arbol import Arbol, TipoHijo
import itertools
from math import log

class Id3:
    '''
    Clase que implementa el algoritmo Id3
    '''

    def __init__(self, atributoObjetivo, valoresPosibles):
        '''
        La clase se inicializa con el valor objetivo que sera buscado
        por el algoritmo
        '''
        self.atributoObjetivo = atributoObjetivo
        self.valoresPosibles = valoresPosibles

    def ejecutar(self, ejemplos, atributos, maxDepth = None):
        '''
        Se ejecuta el algoritmo sobre la lista de datos "ejemplos", considerando los
        atributos "atributos".
        El algoritmo retorna un arbol de decision, de profundidad maxDepth (si no se
            especifica se considera profundidad infinita).
        '''

        objetivo = self.atributoObjetivo

        # Evaluo el caso en que todos los casos de prueba restantes tienen el mismo
        # valor en el atributo objetivo
        if len(set([e[objetivo] for e in ejemplos])) == 1:
            # Retorno una hoja de tipo UNICO con el unico valor posible de G3
            return Arbol(ejemplos[0][objetivo], TipoHijo.UNICO)

        # Evaluo el caso en que no me quedan atributos por considerar o alcance la
        # profundidad maxima estipulada para el arbol de decision
        if len(atributos) == 0 or (maxDepth is not None and maxDepth <= 0):
            # Retorno una hoja de tipo MAYORIA, cuyo valor es el valor de mayor
            # frecuencia entre los ejemplos restantes
            return Arbol(self.obtenerValorMasComun(ejemplos), TipoHijo.MAYORIA)

        # Obtengo el mejor clasificador local y su ganancia asociada
        mejorAtributo, ganancia = self.obtenerMejorClasificador(ejemplos, atributos)

        # Remuevo el atributo seleccionado de la lista de atributos a considerar
        nuevosAtributos = list(atributos)
        nuevosAtributos.remove(mejorAtributo)

        # Creo el nodo raiz. Las ganancias almacenadas son para uso estadistico
        a = Arbol(mejorAtributo)
        a.ganancia = ganancia
        sumaGanancias = sum([g[1] for g in self.obtenerGanancias(ejemplos, atributos)])
        a.gananciaRelativa =  ganancia /  sumaGanancias if sumaGanancias != 0 else 0

        for v in self.valoresPosibles[mejorAtributo]:
        # Para cada valor posible del atributo seleccionado, ejecuto un paso del algoritmo
        # y almaceno el arbol resultante en una de las ramas del arbol
            ejemplos_aux = [e for e in ejemplos if e[mejorAtributo]==v]

            if len(ejemplos_aux) != 0:

                rama = self.ejecutar(ejemplos_aux, nuevosAtributos, maxDepth - 1 if maxDepth is not None else None)
                a.agregarRama(v, rama)

            else:

                a.agregarRama(v, Arbol(self.obtenerValorMasComun(ejemplos), TipoHijo.ELSE))

        return a

    def obtenerGanancias(self, ejemplos, atributos):
        '''
        Retorna una lista con el nombre y la ganancia de cada atributo en la lista
        segun los ejemplos de entrenamiento
        '''
        return [(a, self.obtenerGananciaInformacion(ejemplos,a)) for a in atributos]

    def obtenerMejorClasificador(self,ejemplos, atributos):
        '''
        Retorna el par (atributo,ganancia) con la mayor ganancia calculada
        a partir de los ejemplos y los atributos a considerar
        '''
        ganancias = self.obtenerGanancias(ejemplos, atributos)

        return max(ganancias, key=lambda g: g[1])

    def obtenerEntropia(self, ejemplos, atributo):
        '''
        Retorna la entropia de un atributo en una lista de ejemplos
        '''
        entropia = 0

        for v in  set([e[atributo] for e in ejemplos]):
            proporcion = float(len([e for e in ejemplos if e[atributo] == v])) / len(ejemplos)

            entropia -= proporcion * log(proporcion)

        return entropia

    def obtenerGananciaInformacion(self,ejemplos, atributo):
        '''
        Retorna la ganancia de informacion de un atributo en una lista de ejemplos
        '''

        termino = 0

        for v in set([e[atributo] for e in ejemplos]):
            ejemplosSelecionados = [e for e in ejemplos if e[atributo] == v]
            termino += (float(len(ejemplosSelecionados))/len(ejemplos)) * \
                       self.obtenerEntropia(ejemplosSelecionados, atributo)

        return self.obtenerEntropia(ejemplos, atributo) - termino

    def obtenerValorMasComun(self,ejemplos):
        '''
        Retorna el valor mas comun del atributo objetivo en una lista de ejemplos
        '''
        cantidad = {}

        for e in ejemplos:
            if e[self.atributoObjetivo] in cantidad:
                cantidad[e[self.atributoObjetivo]] += 1
            else:
                cantidad[e[self.atributoObjetivo]] = 0

        return max(cantidad.iteritems(), key=lambda (k, v): v)[0]


