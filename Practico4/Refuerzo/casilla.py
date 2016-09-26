from movimiento import Direccion

class Casilla:
	'''
	Clase que representa una casilla con su valor de trancision para cada direccion
	'''

	def __init__(self, izquierda=None, derecha=None, arriba=None, abajo=None):
		'''
		La casilla creada por defecto no tiene transiciones posibles (es Goal)
		'''
		self.izquierda = izquierda
		self.derecha = derecha
		self.arriba = arriba
		self.abajo = abajo

	def getArriba(self):
		return self.arriba

	def getAbajo(self):
		return self.abajo

	def getIzquierda(self):
		return self.izquierda

	def getDerecha(self):
		return self.derecha

	def setArriba(self, valor):
		self.arriba = valor

	def setAbajo(self, valor):
		self.abajo = valor

	def setIzquierda(self, valor):
		self.izquierda = valor

	def setDerecha(self, valor):
		self.derecha = valor

	def isGoal(self):
		'''
		Una casilla es meta (Goal) si no tiene trancisiones posibles
		'''
		return (self.izquierda == None) and (self.derecha == None) and (self.arriba == None) and (self.abajo == None)

	def getMovimientosValidos(self):
		'''
		Retorna una lista con todas las direcciones posibles en las que me puedo mover
		'''
		movimientos = []
		if self.izquierda != None:
			movimientos.append(Direccion.IZQUIERDA)
		if self.derecha != None:
			movimientos.append(Direccion.DERECHA)
		if self.arriba != None:
			movimientos.append(Direccion.ARRIBA)
		if self.abajo != None:
			movimientos.append(Direccion.ABAJO)
		return movimientos


