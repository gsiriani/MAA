from arbol import Arbol
import itertools
from math import log

class Id3:

    def __init__(self, atributoObjetivo):
        self.atributoObjetivo = atributoObjetivo

    def ejecutar(self, ejemplos, atributos, maxDepth = 3):

        objetivo = self.atributoObjetivo

        primerValor = ejemplos[0][objetivo]

        if len(ejemplos) == 1 or all([primerValor == e[objetivo] for e in ejemplos]):
            return Arbol(primerValor)

        if len(atributos) == 0 or maxDepth <= 0:
            return Arbol(self.obtenerValorMasComun(ejemplos))

        mejorAtributo = self.obtenerMejorClasificador(ejemplos, atributos)

        nuevosAtributos = list(atributos)
        nuevosAtributos.remove(mejorAtributo)

        a = Arbol(mejorAtributo)

        for v in self.valoresPosibles(mejorAtributo, ejemplos):
            ejemplos_aux = [e for e in ejemplos if e[mejorAtributo]==v]
            rama = self.ejecutar(ejemplos_aux, nuevosAtributos, maxDepth - 1)
            a.agregarRama(v, rama)

        return a


    def valoresPosibles(self, atributo, ejemplos):

        return set([e[atributo] for e in ejemplos])

    def obtenerMejorClasificador(self,ejemplos, atributos):

        return max(atributos, key=lambda a:self.obtenerGananciaInformacion(ejemplos,a))

    def obtenerEntropia(self, ejemplos, atributo):

        entropia = 0

        for v in self.valoresPosibles(atributo, ejemplos):
            proporcion = float(len([e for e in ejemplos if e[atributo] == v])) / len(ejemplos)
            entropia -= proporcion * log(proporcion)

        return entropia

    def obtenerGananciaInformacion(self,ejemplos, atributo):

        termino = 0

        for v in self.valoresPosibles(atributo, ejemplos):
            ejemplosSelecionados = [e for e in ejemplos if e[atributo] == v]
            termino += (float(len(ejemplosSelecionados))/len(ejemplos)) * \
                       self.obtenerEntropia(ejemplosSelecionados, atributo)

        return self.obtenerEntropia(ejemplos, atributo) - termino

    def obtenerValorMasComun(self,ejemplos):

        cantidad = {}

        for e in ejemplos:
            if e[self.atributoObjetivo] in cantidad:
                cantidad[e[self.atributoObjetivo]] += 1
            else:
                cantidad[e[self.atributoObjetivo]] = 0

        return max(cantidad.iteritems(), key=lambda (k, v): v)[0]


