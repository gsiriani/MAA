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
        return Turno.BLANCA if turno == Turno.NEGRA else Turno.NEGRA

class Direccion:
    BLANCA = 1
    NEGRA = -1

class Movimiento:

    def __init__(self, origen, destino):
        self.origen = origen

        if isinstance(destino,list):
            self.destino = destino
        else:
            self.destino = [destino]

    origen = None
    destino = []

    def esComida(self):
        return  abs(self.origen[0] - self.destino[0][0]) > 1

    def __eq__(self, other):

        return self.origen == other.origen and self.destino == other.destino

    def __ne__(self, other):

        return not self.__eq__(other)

class Damas:

    movimientosValidosCalculados = []

    def __init__(self, tablero = None, turno = None):
        self.turno = turno if turno is not None else Turno.BLANCA

        if tablero is not None:
            self.tablero = tablero
        else:
            self.tablero = Damas.tableroVacio()

        self.movimientosValidosCalculados = self.calcularMovimientosValidos()

    @staticmethod
    def tableroVacio():

        # Declaro la variable
        tablero = [[0 for x in range(8)] for y in range(8)]

        for x in range(8):
            for y in range(8):
                if ((x + y) % 2) == 0:
                    tablero[x][y] = Casilla.VACIA
                else:
                    tablero[x][y] = Casilla.INVALIDA

        return tablero

    @staticmethod
    def tablero_base():

        tablero = Damas.tableroVacio()

        # Completo las primeras 3 hileras con fichas blancas
        for x in range(3):
            for y in range(8):
                if ((x + y) % 2) == 0:
                    tablero[x][y] = Casilla.BLANCA

        # Completo las primeras 3 hileras con fichas blancas
        for x in range(5, 8):
            for y in range(8):
                if ((x + y) % 2) == 0:
                    tablero[x][y] = Casilla.NEGRA

        return tablero

    def esMovimientoValido(self, movimiento):

        return movimiento in self.movimientosValidosCalculados

    def calcularEsMovimientoValido(self, movimiento):

        x, y = movimiento.origen

        if x < 0 or x > 7 or y < 0 or y > 7:
            return False

        colorEnPosicion = self.tablero[x][y]

        if(colorEnPosicion != self.turno):
            return False

        # Sólo comidas simples

        if len(movimiento.destino) != 1:
            return False

        xDest, yDest = movimiento.destino[0]

        if xDest < 0 or xDest > 7 or yDest < 0 or yDest > 7:
            return False

        difX = xDest - x
        difY = yDest - y

        if difX == 0 or abs(difX) != abs(difY):
            return False

        signoX = difX/abs(difX)

        if (self.turno == Turno.BLANCA and signoX != Direccion.BLANCA) or\
                (self.turno == Turno.NEGRA and signoX != Direccion.NEGRA):
            return False

        if difX == 0 or abs(difX) > 2:
            return

        if self.tablero[xDest][yDest] != Casilla.VACIA:
            return False

        medioX = (xDest + x) / 2
        medioY = (yDest + y) / 2

        return abs(difX) == 1 or self.tablero[medioX][medioY] == Turno.otroTurno(self.turno)


    def obtenerTableroResultante(self,movimiento):

        if not self.esMovimientoValido(movimiento):
            return Damas(self.tablero, self.turno)

        tablero = self.tablero

        x,y = movimiento.origen
        tablero[x][y] = Casilla.VACIA

        for destino in movimiento.destino:
            xDest, yDest = destino
            if abs(xDest - x) > 1:
                tablero[(xDest + x) / 2][(yDest + y) / 2] = Casilla.VACIA

            x,y = xDest, yDest

        tablero[xDest][yDest] = self.turno

        return Damas(tablero, Turno.otroTurno(self.turno))


    def calcularMovimientosValidos(self):

        movimientos = []

        for x in range(8):
            for y in range(8):
                if self.tablero[x][y] == self.turno:
                    movimientos += self.calcularMovimientosValidosDePieza(x,y)

        if any(m.esComida() for m in movimientos):
            movimientos = [m for m in movimientos if m.esComida()]

        return movimientos

    def partidaTerminada(self):

        return len(self.movimientosValidosCalculados) == 0

    def movimientosValidosDePieza(self, x, y):

        return [m for m in self.movimientosValidosCalculados if m.origen[0] == x and m.origen[1] == y]

    def calcularMovimientosValidosDePieza(self, x,y):

        movimientos = []

        for xDest in range(8):

            difX = (xDest - x)

            movimiento = Movimiento((x, y), (xDest, y + difX))

            if self.calcularEsMovimientoValido(movimiento):
                movimientos.append(movimiento)

            movimiento = Movimiento((x, y), (xDest, y - difX))

            if self.calcularEsMovimientoValido(movimiento):
                movimientos.append(movimiento)


        return movimientos