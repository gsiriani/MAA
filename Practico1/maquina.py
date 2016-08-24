# Maquina que elije segun los valores de sus weights la proxima jugada a ejecutar.

import math
import random

from damas import Casilla, Turno
from learn import Resultado

class EvaluacionTableroFinal:
    ESTATICA = 0
    DIFERENCIA_FICHAS = 1

class Maquina:

    MAX_INITIAL_WEIGHT = 100
    MIN_INITIAL_WEIGHT = -100

    DebugOutput = False

    representacion = None

    def __init__(self, representacion, evaluacioTableroFinal = EvaluacionTableroFinal.ESTATICA):

        self.representacion = representacion
        self.weights = tuple(random.uniform(self.MIN_INITIAL_WEIGHT, self.MAX_INITIAL_WEIGHT)
                         for i in range(representacion.size + 1))

        self.evaluacioTableroFinal = evaluacioTableroFinal

    def valorTablero(self, representacion, damas):#calcula el valor del tablero multiplicando los criterios por los pesos
        if damas.partidaTerminada():
            return self.valorTableroFinal(damas.tablero)

        valor = sum([x * y for x, y in zip(representacion, self.weights)]) + representacion[len(representacion) - 1]

        assert not math.isinf(valor)

        return valor

    def valorTableroFinal(self, tablero):
        flattened = [casilla for fila in tablero for casilla in fila]

        cantidadBlancas = sum([1 for c in flattened if c == Casilla.BLANCA])
        cantidadNegras = sum([1 for c in flattened if c == Casilla.NEGRA])

        if self.evaluacioTableroFinal == EvaluacionTableroFinal.ESTATICA:
            return 0 if cantidadNegras == cantidadBlancas else (100 if cantidadBlancas > cantidadNegras else -100)
        else:
            return (cantidadBlancas - cantidadNegras) * 100


    def decidirProximaJugada(self, damas):
        movimientosPosibles = []
        #calculo todas las jugadas posibles
        for m in damas.movimientosValidosCalculados:
            resultado = Resultado()
            resultado.estadoResultante = damas.obtenerTableroResultante(m)
            resultado.representacionTablero = self.representacion.obtener(resultado.estadoResultante.tablero)
            resultado.valorTableroResultante = self.valorTablero(resultado.representacionTablero,
                                                                 resultado.estadoResultante)

            movimientosPosibles.append(resultado)

        if self.DebugOutput:
            valores = [r.valorTableroResultante for r in movimientosPosibles]
            print ("Jugadas: " + str((min(valores),max(valores))))
        #elijo el mejor resultado segun el color con el que este jugando
        if damas.turno == Turno.BLANCA:
            mejorResultado = max(movimientosPosibles, key=lambda r: r.valorTableroResultante)
        else:
            mejorResultado = min(movimientosPosibles, key=lambda r: r.valorTableroResultante)
        #si hay mas de uno elijo cualquiera
        mejoresResultados = [r for r in movimientosPosibles if
                             r.valorTableroResultante == mejorResultado.valorTableroResultante]
        resultadoElegido = random.choice(mejoresResultados)

        return resultadoElegido