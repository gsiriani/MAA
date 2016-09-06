class TipoHijo:
    UNICO = 0
    MAYORIA = 1,
    ELSE = 2

class Arbol:

    def __init__(self, valor, tipoHijo = None):
        self.valor = valor
        self.hijos = {}
        self.ganancia = 0
        self.gananciaRelativa = 0
        self.tipoHijo = tipoHijo

    def agregarRama(self, etiqueta, arbol):
        self.hijos[etiqueta] = arbol

    def alturaMaxima(self):
        return 1 + (max([h.alturaMaxima() for h in self.hijos.values()]) if len(self.hijos) > 0 else 0)

    def alturaMinima(self):
        return 1 + (min([h.alturaMinima() for h in self.hijos.values()]) if len(self.hijos) > 0 else 0)

    def cantidadHojas(self):
        return sum([h.cantidadHojas() for h in self.hijos.values()]) if len(self.hijos) > 0 else 1


    def imprimirEstadisticas(self):

        print("Altura maxima: " + str(self.alturaMaxima()))
        print("Altura minima: " + str(self.alturaMinima()))
        print("Cantidad de hojas: " + str(self.cantidadHojas()))

    def validarLista(self, datos, valorObjetivo):

        return sum([(1 if self.validar(c, valorObjetivo) else 0) for c in datos])/float(len(datos))

    def validar(self, caso, valorObjetivo):

        if len(self.hijos) == 0:
            return self.valor == caso[valorObjetivo]
        else:
            valor = caso[self.valor]

            hijo = self.hijos[valor]

            return hijo.validar(caso, valorObjetivo)



        



