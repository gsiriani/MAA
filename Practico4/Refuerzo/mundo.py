from casilla import Casilla

class Mundo:

	def __init__(self, size):
		'''
		Construyo una matriz size*size de Casillas con transiciones 0 en todas
		las direcciones salvo en los bordes, donde la transicion es nula (el 
		mundo construido NO es circular) 
		'''
		self.casillas = []

		# Construyo una matriz de size*size
		for i in range(size):
			self.casillas[i] = []
			for j in range(size):
				
				# Por defecto las casillas tienen valor 0 en todas las direcciones
				izquierda = 0
				derecha = 0
				arriba = 0
				abajo = 0

				# Las casillas en los bordes tienen valor null, ya que el mundo NO es circular
				if i == 0:
					arriba = None
				if i == (size - 1):
					abajo = None
				if j == 0:
					izquierda = None
				if j == (size - 1):
					derecha = None

				# Construyo la casilla
				self.casillas[i][j] = Casilla(izquierda=izquierda, derecha=derecha, arriba=arriba, abajo=abajo)

	def setCasilla(self, i, j, casilla):
		self.casillas[i][j] = casilla

	def getCasilla(self, i, j)
		return self.casillas[i][j]