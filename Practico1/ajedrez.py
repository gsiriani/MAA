# -*- coding: UTF-8 -*-

class Casilla:
    # Enum que representa el estado de una casilla en el tablero
    BLANCA = 1  # La casilla tiene una ficha blanca
    NEGRA = 2  # La casilla tiene una ficha negra
    VACIA = 3  # La casilla esta vacia
    INVALIDA = 4  # La casilla es invalida


class Turno:
    BLANCA = Casilla.BLANCA
    NEGRA = Casilla.NEGRA

    @staticmethod
    def otroTurno(turno):
        return Turno.BLANCA if turno == Turno.NEGRA else Turno.BLANCA

class Direccion:
    BLANCA = 1
    NEGRA = -1

class Movimiento:

    def __init__(self, origen, destino):
        self.Origen = origen

        if isinstance(destino,list):
            self.Destino = destino
        else:
            self.Destino = [destino]

    Origen = (-1,-1)
    Destino = []

class Tablero:
    def iniciar_tablero(self):
        # Retorna un tablero inicial

        # Declaro la variable
        self.tablero = [[0 for x in range(8)] for y in range(8)]

        for x in range(8):
            for y in range(8):
                if ((x + y) % 2) == 0:
                    self.tablero[x][y] = Casilla.VACIA
                else:
                    self.tablero[x][y] = Casilla.INVALIDA

    def tablero_base(self):

        # Completo las primeras 3 hileras con fichas blancas
        for x in range(3):
            for y in range(8):
                if ((x + y) % 2) == 0:
                    self.tablero[x][y] = Casilla.BLANCA

        # Completo las primeras 3 hileras con fichas blancas
        for x in range(5, 8):
            for y in range(8):
                if ((x + y) % 2) == 0:
                    self.tablero[x][y] = Casilla.NEGRA

    def esMovimientoValido(self, movimiento, turno):

        x, y = movimiento.Destino

        if x < 0 or x > 7 or y < 0 or y > 7:
            return False

        colorEnPosicion = self.tablero[x][y]

        if(colorEnPosicion != turno):
            return False

        # Sólo comidas simples

        if len(movimiento.Destino) != 1:
            return False

        xDest, yDest = movimiento.Destino[0]

        if xDest < 0 or xDest > 7 or yDest < 0 or yDest > 7:
            return False

        difX = xDest - x
        difY = yDest - y

        if abs(difX) != abs(difY):
            return False

        signoX = difX/abs(difX)

        if (Turno.BLANCA and signoX != Direccion.BLANCA) or\
                (Turno.NEGRA and signoX != Direccion.BLANCA):
            return False

        if difX == 0:
            return

        if self.tablero[xDest][yDest] != Casilla.VACIA:
            return False

        medioX = (xDest + x) / 2
        medioY = (yDest + y) / 2

        return difX == 1 or self.tablero[medioX][medioY] == Turno.otroTurno(turno)

