import math
import random

from damas import Casilla, Turno
from learn import Resultado


class Maquina:

    MAX_INITIAL_WEIGHT = 10
    MIN_INITIAL_WEIGHT = -10

    representacion = None

    def __init__(self, representacion):

        self.representacion = representacion
        self.weights = tuple(random.uniform(self.MIN_INITIAL_WEIGHT, self.MAX_INITIAL_WEIGHT)
                         for i in range(representacion.size + 1))

    def valorTablero(self, representacion, damas):
        if damas.partidaTerminada():
            return self.valorTableroFinal(damas.tablero)

        valor = sum([x * y for x, y in zip(representacion, self.weights)]) + representacion[len(representacion) - 1]

        assert not math.isinf(valor)

        return valor

    def valorTableroFinal(self, tablero):
        flattened = [casilla for fila in tablero for casilla in fila]

        cantidadBlancas = sum([1 for c in flattened if c == Casilla.BLANCA])
        cantidadNegras = sum([1 for c in flattened if c == Casilla.NEGRA])

        return 0 if cantidadNegras == cantidadBlancas else (100 if cantidadBlancas > cantidadNegras else -100)


    def decidirProximaJugada(self, damas):
        movimientosPosibles = []

        for m in damas.movimientosValidosCalculados:
            resultado = Resultado()
            resultado.estadoResultante = damas.obtenerTableroResultante(m)
            resultado.representacionTablero = self.representacion.obtener(resultado.estadoResultante.tablero)
            resultado.valorTableroResultante = self.valorTablero(resultado.representacionTablero,
                                                                 resultado.estadoResultante)

            movimientosPosibles.append(resultado)

        if damas.turno == Turno.BLANCA:
            mejorResultado = max(movimientosPosibles, key=lambda r: r.valorTableroResultante)
        else:
            mejorResultado = min(movimientosPosibles, key=lambda r: r.valorTableroResultante)

        mejoresResultados = [r for r in movimientosPosibles if
                             r.valorTableroResultante == mejorResultado.valorTableroResultante]
        resultadoElegido = random.choice(mejoresResultados)

        return resultadoElegido