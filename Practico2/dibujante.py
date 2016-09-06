from graphviz import Digraph
from arbol import Arbol

class Dibujante:
    '''
    Clase que permite obtener una representacion grafica de un arbol de decision
    '''

    @staticmethod
    def dibujar(arbol):
        '''
        Construye una representacion grafica del arbol en formato .png
        '''

        dot = Digraph(format='png')

        Dibujante.subDibujar(arbol, dot)
        dot.render('output2.png', view=True)

    @staticmethod
    def subDibujar(arbol, dot):
        '''
        Sub-rutina que dibuja un nodo del arbol y se llama recursivamente para dibujar 
        a los hijos
        '''
        dot.node(str(id(arbol)), str(arbol.valor) +
                 ("\n(" + str(round(arbol.ganancia,2)) + "," +
                  str(round(arbol.gananciaRelativa*100,2))+ "%)" if arbol.ganancia != 0 else ""))

        for l, h in arbol.hijos.iteritems():
            Dibujante.subDibujar(h, dot)
            dot.edge(str(id(arbol)), str(id(h)), label=str(l))


