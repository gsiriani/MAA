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

class Direccion: #se asumen estos valores para facilitar las cuentas en el codigo
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

    def esParcial(self, parcial):

        if self.origen != parcial.origen:
            return False

        for i, d in enumerate(parcial.destino):

            if d != self.destino[i]:
                return False

        return True

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
    def tableroVacio(): #retorna un tablero sin piezas

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
    def tablero_base(): #retorna un tablero con las piezas en sus posiciones iniciales

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

    def calcularEsMovimientoValido(self, movimiento):#verifica si el movimiento es valido ya sea simple o compuesto

        x, y = movimiento.origen

        if x < 0 or x > 7 or y < 0 or y > 7:
            return False

        colorEnPosicion = self.tablero[x][y]

        if(colorEnPosicion != self.turno):
            return False

        xDest,yDest = movimiento.destino[len(movimiento.destino) - 1]
        if len(movimiento.destino) == 1:  
			#el movimiento es simple
            return self.esValidoMovimientoSimple(x, y, xDest, yDest, self.turno, self.tablero)
        else:
			#el movimiento es compuesto
            xDest0,yDest0 = movimiento.destino[len(movimiento.destino) - 2]
            return self.esValidoMovimientoSimple(xDest0, yDest0,xDest, yDest, self.turno, self.tablero)


    def esValidoMovimientoSimple(self, xOrigen, yOrigen, xDest, yDest, turno, tablero):
	
        if xDest < 0 or xDest > 7 or yDest < 0 or yDest > 7:
            return False

        difX = xDest - xOrigen
        difY = yDest - yOrigen

        if difX == 0 or abs(difX) != abs(difY):
            return False

        signoX = difX/abs(difX)

        if (turno == Turno.BLANCA and signoX != Direccion.BLANCA) or\
                (turno == Turno.NEGRA and signoX != Direccion.NEGRA):
            return False

        if difX == 0 or abs(difX) > 2:
            return

        if tablero[xDest][yDest] != Casilla.VACIA:
            return False

        medioX = (xDest + xOrigen) / 2
        medioY = (yDest + yOrigen) / 2

        return abs(difX) == 1 or tablero[medioX][medioY] == Turno.otroTurno(turno)

    def obtenerTableroResultante(self,movimiento):#retorna el tablero resultante de haber realizado el movimiento
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

    def calcularMovimientosValidosDePieza(self, x,y, destinos = []):

        soloComidas = len(destinos) != 0

        if len(destinos) == 0:
            xDest,yDest = x,y
        else:
            ultimoDestino = destinos[len(destinos) - 1]
            xDest,yDest = ultimoDestino
        movimientos = []

        rango = [2] if soloComidas else [1,2]

        for delta in rango:

            self.calcularMovimientoEnDireccionDePieza(x,y,xDest, yDest, delta, 1, 1, destinos, movimientos)
            self.calcularMovimientoEnDireccionDePieza(x,y,xDest, yDest, delta, 1, -1, destinos, movimientos)
            self.calcularMovimientoEnDireccionDePieza(x,y,xDest, yDest, delta, -1, 1, destinos, movimientos)
            self.calcularMovimientoEnDireccionDePieza(x,y,xDest, yDest, delta, -1, -1, destinos, movimientos)


        return movimientos

    def calcularMovimientoEnDireccionDePieza(self, x, y, xDest, yDest, delta, multX, multY, destinos, movimientos):

        nuevosDestinos = destinos + [(xDest + delta * multX, yDest + delta * multY)]
        movimiento = Movimiento((x, y), nuevosDestinos)

        if self.calcularEsMovimientoValido(movimiento):
			#verifica si es posible comer multiples piezas 
            if delta == 2:
                cadena = self.calcularMovimientosValidosDePieza(x,y, nuevosDestinos)

                if len(cadena) == 0:
                    movimientos.append(movimiento)
                else:
                    movimientos += cadena
            else:
            movimientos.append(movimiento)


