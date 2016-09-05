from graphviz import Digraph
from arbol import Arbol

class Dibujante:

    @staticmethod
    def dibujar(arbol):

        dot = Digraph(format='png')

        Dibujante.subDibujar(arbol, dot)
        dot.render('output2.png', view=True)

    @staticmethod
    def subDibujar(arbol, dot):

        dot.node(str(id(arbol)), str(arbol.valor) +
                 ("\n(" + str(round(arbol.ganancia,2)) + "," +
                  str(round(arbol.gananciaRelativa*100,2))+ "%)" if arbol.ganancia != 0 else ""))

        for l, h in arbol.hijos.iteritems():
            Dibujante.subDibujar(h, dot)
            dot.edge(str(id(arbol)), str(id(h)), label=l)


