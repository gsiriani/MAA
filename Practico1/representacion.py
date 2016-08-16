from damas import Casilla, Turno, Damas


class Representacion():

    size = 10

    @staticmethod
    def obtener(tablero):

        flattened = [casilla for fila in tablero for casilla in fila]

        cantidadBlancas = sum([1 for c in flattened if c == Casilla.BLANCA])
        cantidadNegras = sum([1 for c in flattened if c == Casilla.NEGRA])

        segurasBlancas = Representacion.obtenerSeguras(tablero, Turno.BLANCA)
        segurasNegras = Representacion.obtenerSeguras(tablero, Turno.NEGRA)

        distanciaLineaFondoBlancas = Representacion.distanciaLineaFondo(tablero, Turno.BLANCA)
        distanciaLineaFondoNegras = Representacion.distanciaLineaFondo(tablero, Turno.NEGRA)

        cantidadMovimientosBlancas, cantidadComidasBlancas = Representacion.cantidadMovimientosYComidas(tablero, Turno.BLANCA)
        cantidadMovimientosNegras, cantidadComidasNegras = Representacion.cantidadMovimientosYComidas(tablero, Turno.NEGRA)

        return cantidadBlancas, cantidadNegras, segurasBlancas, segurasNegras, distanciaLineaFondoBlancas,\
               distanciaLineaFondoNegras,cantidadMovimientosBlancas,cantidadMovimientosNegras, \
               cantidadComidasBlancas, cantidadComidasNegras

    @staticmethod
    def obtenerSeguras(tablero, color):

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
    def cantidadMovimientosYComidas(tablero, color):

        damas = Damas(tablero, color)

        cantidadComidas = len([m for m in damas.movimientosValidosCalculados if m.esComida()])
        cantidadMovimientos = len(damas.movimientosValidosCalculados) - cantidadComidas

        return (cantidadMovimientos, cantidadComidas)