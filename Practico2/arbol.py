
class Arbol:

    def __init__(self, valor):
        self.valor = valor
        self.hijos = {}

    def agregarRama(self, etiqueta, arbol):
        self.hijos[etiqueta] = arbol
