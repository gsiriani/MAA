from graphviz import Digraph
from arbol import Arbol

class Dibujante:

    @staticmethod
    def dibujar(arbol):

        dot = Digraph()

        Dibujante.subDibujar(arbol, dot)
        dot.render('output2.gv', view=True)

    @staticmethod
    def subDibujar(arbol, dot):

        dot.node(str(id(arbol)), arbol.valor)

        for l, h in arbol.hijos.iteritems():
            Dibujante.subDibujar(h, dot)
            dot.edge(str(id(arbol)), str(id(h)), label=l)


