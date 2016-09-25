
class Casilla:
	def __init__(self, izquierda=0, derecha=0, arriba=0, abajo=0):
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
		return (self.izquierda == None) and (self.derecha == None) and (self.arriba == None) and (self.abajo == None)


