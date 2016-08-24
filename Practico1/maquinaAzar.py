# Maquina que elije una jugada al azar entre aquellas validas. Se utiliza para validar el aprendizaje.

import random

from damas import Casilla
from learn import Resultado


class MaquinaAzar:

    representacion = None

    def __init__(self, representacion):

        self.representacion = representacion
        self.weights = tuple(0 for i in range(representacion.size + 1))

    def valorTablero(self, representacion, damas):
        if damas.partidaTerminada():
            return self.valorTableroFinal(damas.tablero)
        else:
            return 0

    def valorTableroFinal(self, tablero):
        flattened = [casilla for fila in tablero for casilla in fila]

        cantidadBlancas = sum([1 for c in flattened if c == Casilla.BLANCA])
        cantidadNegras = sum([1 for c in flattened if c == Casilla.NEGRA])

        return 0 if cantidadNegras == cantidadBlancas else (100 if cantidadBlancas > cantidadNegras else -100)


    def decidirProximaJugada(self, damas):
        # Elige movimiento al azar
        movimientosPosibles = []

        m = random.choice(damas.movimientosValidosCalculados)

        resultado = Resultado()
        resultado.estadoResultante = damas.obtenerTableroResultante(m)
        resultado.representacionTablero = self.representacion.obtener(resultado.estadoResultante.tablero)
        resultado.valorTableroResultante = self.valorTablero(resultado.representacionTablero, resultado.estadoResultante)

        return resultado