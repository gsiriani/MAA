from arbol import Arbol, TipoHijo
import itertools
from math import log

class Id3:

    def __init__(self, atributoObjetivo):
        self.atributoObjetivo = atributoObjetivo

    def ejecutar(self, ejemplos, atributos, maxDepth = None):

        objetivo = self.atributoObjetivo

        if len(set([e[objetivo] for e in ejemplos])) == 1:
            return Arbol(ejemplos[0][objetivo], TipoHijo.UNICO)

        if len(atributos) == 0 or (maxDepth is not None and maxDepth <= 0):
            return Arbol(self.obtenerValorMasComun(ejemplos), TipoHijo.MAYORIA)

        mejorAtributo, ganancia = self.obtenerMejorClasificador(ejemplos, atributos)

        nuevosAtributos = list(atributos)
        nuevosAtributos.remove(mejorAtributo)

        a = Arbol(mejorAtributo)
        a.ganancia = ganancia
        sumaGanancias = sum([g[1] for g in self.obtenerGanancias(ejemplos, atributos)])
        a.gananciaRelativa =  ganancia /  sumaGanancias if sumaGanancias != 0 else 0

        for v in self.valoresPosibles(mejorAtributo, ejemplos):
            ejemplos_aux = [e for e in ejemplos if e[mejorAtributo]==v]
            rama = self.ejecutar(ejemplos_aux, nuevosAtributos, maxDepth - 1 if maxDepth is not None else None)
            a.agregarRama(v, rama)

        a.agregarRamaElse(Arbol(self.obtenerValorMasComun(ejemplos), TipoHijo.ELSE))

        return a


    def valoresPosibles(self, atributo, ejemplos):

        return set([e[atributo] for e in ejemplos])

    def obtenerGanancias(self, ejemplos, atributos):

        return [(a, self.obtenerGananciaInformacion(ejemplos,a)) for a in atributos]

    def obtenerMejorClasificador(self,ejemplos, atributos):

        ganancias =  self.obtenerGanancias(ejemplos,atributos)

        return max(ganancias, key=lambda g: g[1])

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


