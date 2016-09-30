from mundo import Mundo
from casilla import Casilla
from movimiento import Movimiento, Direccion
from random import choice

class AprendizajeQ:

	def __init__(self, mundo, facDescuento):
		self.mundo = mundo
		self.facDescuento = facDescuento

	def entrenar(self, iteraciones, mundoQ=None):
		'''
		Exploro el mundo y luego corrigo mis estimaciones
		'''
		if mundoQ == None:
			# Inicializo el mundo con valores nulos
			mundoQ = Mundo(self.mundo.getSize())

		# Realizo un recorrido por cada iteracion
		for i in range(iteraciones):
			recorrido = self.explorar()
			self.actualizarValores(mundoQ, recorrido)

		return mundoQ

	def explorar(self):
		'''
		Realizo un recorrido aleatorio por el mundo y retorno la
		secuencia de pasos con la ganancia/descuento de cada uno
		'''

		# Selecciono al azar la casilla inicial
		i = choice(range(self.mundo.getSize()))
		j = choice(range(self.mundo.getSize()))
		casilla_actual = self.mundo.getCasilla(i, j)

		# Si elijo una Goal, itero hasta obtener una No Goal
		while casilla_actual.isGoal():			
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
			valor = self.obtenerValorCasilla(casilla_actual, direccionMovimiento)
			movimiento = Movimiento(origen=origen, destino=destino, direccion=direccionMovimiento, valor=valor)
			recorrido.append(movimiento)
			casilla_actual = self.mundo.getCasilla(destino[0], destino[1])

		return recorrido


	def actualizarValores(self, mundoQ, recorrido):
		'''
		Dado un recorrido, lo revierto para actualizar mi estimacion del mundo
		'''
		recorrido.reverse()
		for m in recorrido:
			# Recupero las casillas
			casillaOrigen = mundoQ.getCasilla(m.getOrigen()[0], m.getOrigen()[1])			
			casillaDestino = mundoQ.getCasilla(m.getDestino()[0], m.getDestino()[1])

			# Obtengo el maximo valor posible de la casilla destino
			maxDestino = casillaDestino.maximoValorPosible()

			# Calculo el nuevo valor de la accion en la casilla (Q(s,a))
			nuevoValor = m.getValor() + self.facDescuento*maxDestino

			# Actualizo el valor de la casilla
			casillaCorregida = self.corregirCasilla(casillaOrigen, m.getDireccion(), nuevoValor)
			mundoQ.setCasilla(m.getOrigen()[0], m.getOrigen()[1], casillaCorregida)


	def obtenerValorCasilla(self, casilla, direccion):
		'''
		Obtengo el valor de la casilla para determinada direccion
		'''
		if direccion == Direccion.IZQUIERDA:
			valor = casilla.getIzquierda()
		if direccion == Direccion.DERECHA:
			valor = casilla.getDerecha()
		if direccion == Direccion.ARRIBA:
			valor = casilla.getArriba()
		if direccion == Direccion.ABAJO:
			valor = casilla.getAbajo()
		return valor

	def calcularDestino(self, (i, j), direccion):
		'''
		Obtengo las coordenadas de la siguiente casilla a visitar dada una 
		direccion de movimiento
		'''
		if direccion == Direccion.IZQUIERDA:
			j -= 1
		if direccion == Direccion.DERECHA:
			j += 1
		if direccion == Direccion.ARRIBA:
			i -= 1
		if direccion == Direccion.ABAJO:
			i += 1
		return (i, j)

	def corregirCasilla(self, casilla, direccion, valor):
		'''
		Actualizo el valor de la casilla en determinada direccion
		'''
		if direccion == Direccion.IZQUIERDA:
			casilla.setIzquierda(valor)
		if direccion == Direccion.DERECHA:
			casilla.setDerecha(valor)
		if direccion == Direccion.ARRIBA:
			casilla.setArriba(valor)
		if direccion == Direccion.ABAJO:
			casilla.setAbajo(valor)
		return casilla


