import random
from damas import Damas,Turno,Movimiento,Casilla

class Learner():

    MAX_INITIAL_WEIGHT = 100
    MIN_INITIAL_WEIGHT = -100

    def __init__(self, representacion, factorAprendizaje):

        self.representacion = representacion
        random.seed()
        self.weights = tuple(random.uniform(self.MIN_INITIAL_WEIGHT, self.MAX_INITIAL_WEIGHT)
                             for i in range(representacion.size + 1))
        self.factorAprendizaje = factorAprendizaje

    def run(self, iterations):
        for i in range(iterations):
            self.siguienteIteracion()

    def generarTableroInicial(self):

        return Damas.tablero_base()

    def valorTablero(self, representacion):

        return [x * y for x, y in zip(representacion,self.weights)]

    def aplicarAprendizaje(self, decisiones, valorEntrenamiento):

        weights = list(self.weights)

        for decision in decisiones.reverse():
            for i,w in weights:

                weights[i] = w + self.factorAprendizaje * decision.representacion[i] * \
                                 (valorEntrenamiento - decision.valor)

    def siguienteIteracion(self):

        decisiones = []

        damas = Damas(self.generarTableroInicial(),random.choice([Turno.BLANCA,Turno.NEGRA]))

        while not damas.partidaTerminada():

            resultados = []

            for m in damas.movimientosValidosCalculados:
                resultado = Resultado()
                resultado.tablero = damas.obtenerTableroResultante(m)
                resultado.representacion = self.representacion.obtener(resultado.tablero)
                resultado.valor = self.valorTablero(resultado.representacion)

                resultados.append(resultado)

            mejorResultado = max(resultados, key= lambda r: r.valor)
            mejoresResultados = [r for r in resultados if r.valor == mejorResultado.valor]
            resultadoElegido = random.choice(mejoresResultados)

            decisiones += resultadoElegido

            damas = resultadoElegido.tablero

        valorFinal = self.valorTablero(damas.tablero)

        self.aplicarAprendizaje(decisiones,valorFinal)

class Resultado:

    tablero = None
    representacion = None
    valor = None

