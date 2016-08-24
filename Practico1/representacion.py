# Contiene una clase que implementa una de las representaciones usadas para la ejecucion del aprendizaje LMS.

from damas import Casilla, Turno, Damas


class Representacion():

    size = 10

    @staticmethod
    def obtener(tablero):#retorna el valor de los criterios usados para evaluar el tablero

        flattened = [casilla for fila in tablero for casilla in fila]

        cantidadBlancas = sum([1 for c in flattened if c == Casilla.BLANCA])
        cantidadNegras = sum([1 for c in flattened if c == Casilla.NEGRA])

        segurasBlancas = Representacion.obtenerSeguras(tablero, Turno.BLANCA)
        segurasNegras = Representacion.obtenerSeguras(tablero, Turno.NEGRA)

        distanciaLineaFondoBlancas = Representacion.distanciaLineaFondo(tablero, Turno.BLANCA)
        distanciaLineaFondoNegras = Representacion.distanciaLineaFondo(tablero, Turno.NEGRA)

        cantidadMovimientosBlancas, cantidadComidasBlancas = Representacion.cantidadMovimientosYComidas(tablero, Turno.BLANCA)
        cantidadMovimientosNegras, cantidadComidasNegras = Representacion.cantidadMovimientosYComidas(tablero, Turno.NEGRA)

        cantidadAmenazadasBlancas = Representacion.cantidadAmenazadas(tablero, Turno.BLANCA)
        cantidadAmenazadasNegras = Representacion.cantidadAmenazadas(tablero, Turno.NEGRA)

        return cantidadBlancas, cantidadNegras, segurasBlancas, segurasNegras,distanciaLineaFondoBlancas,\
               distanciaLineaFondoNegras, cantidadMovimientosBlancas, cantidadMovimientosNegras, cantidadAmenazadasBlancas,\
               cantidadAmenazadasNegras

    @staticmethod
    def obtenerSeguras(tablero, color):#retorna la cantidad de fichas que estan en una posicion segura

        for i in range(8):
            cantidadSeguras = 1 if tablero[0][i] == color else 0
            cantidadSeguras += 1 if tablero[7][i] == color else 0
            cantidadSeguras += 1 if tablero[i][0] == color else 0
            cantidadSeguras += 1 if tablero[i][7] == color else 0

        return cantidadSeguras

    @staticmethod
    def distanciaLineaFondo(tablero, color):

        distancia = 0

        for x in range(8):
            for y in range(8):
                if tablero[x][y] == color:
                    distancia += 7 - x if color == Turno.BLANCA else x

        return distancia

    @staticmethod
    def cantidadMovimientosYComidas(tablero, color): #retorna la cantidad de movimientos y comidas validas

        damas = Damas(tablero, color)

        cantidadComidas = len([m for m in damas.movimientosValidosCalculados if m.esComida()])
        cantidadMovimientos = len(damas.movimientosValidosCalculados) - cantidadComidas

        return (cantidadMovimientos, cantidadComidas)

    @staticmethod
    def cantidadAmenazadas(tablero, color):  # retorna la cantidad de movimientos y comidas validas

        damas = Damas(tablero, color)

        comidas = [m for m in damas.movimientosValidosCalculados if m.esComida()]

        posiblesComidas = set()

        for m in comidas:
            x,y = m.origen

            for xDest, yDest in m.destino:
                posiblesComidas.add(((xDest + x)/2,(yDest + y)/2))
                x,y = xDest, yDest

        return len(posiblesComidas)