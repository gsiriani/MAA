from mundo import Mundo
from casilla import Casilla
from movimiento import Movimiento, Direccion
from random import choice

class AprendizajeQ:

	def __init__(self, mundo, facDescuento):
		self.mundo = mundo
		self.facDescuento = facDescuento

	def entrenar(self, iteraciones):
		# Inicializo el mundo con valores nulos
		mundoQ = Mundo(self.mundo.getSize())

		# Realizo un recorrido por cada iteraciones
		for i in range(iteraciones):
			recorrido = self.explorar()
			self.actualizarValores(mundoQ, recorrido)

		return mundoQ

	def explorar(self):

		# Selecciono al azar la casilla inicial
		i = choice(range(self.mundo.getSize()))
		j = choice(range(self.mundo.getSize()))
		casilla_actual = self.mundo.getCasilla(i, j)
		recorrido = []
		destino = (i,j)

		# Genero movimientos hasta alcanzar una casilla Goal
		while not casilla_actual.isGoal():
			# Selecciono movimiento
			movimientosValidos = casilla_actual.getMovimientosValidos()
			direccionMovimiento = choice(movimientosValidos)
			origen = destino
			destino = self.calcularDestino(origen, direccionMovimiento)
			movimiento = Movimiento(origen=origen, destino=destino, direccion=direccionMovimiento)
			recorrido.append(movimiento)

		return recorrido


	def actualizarValores(self, mundoQ, recorrido):
		for m in recorrido:
			print m.getOrigen() + ' ' + m.getDestino() + ' ' + m.getDireccion



	def calcularDestino(self, (i, j), direccion):
		if direccion == Direccion.IZQUIERDA:
			i -= 1
		if direccion == Direccion.DERECHA:
			i += 1
		if direccion == Direccion.ARRIBA:
			j -= 1
		if direccion == Direccion.ABAJO:
			j += 1
		return (i, j)

