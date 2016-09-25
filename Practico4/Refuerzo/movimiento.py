class Direccion:
	'''
	Enum que representa las distintas direcciones en que me puedo mover
	'''
	ARRIBA = 1
	ABAJO = 2
	IZQUIERDA = 3
	DERECHA = 4

class Movimiento:
	'''
	Clase que representa un movimiento realizado con su direccion y 
	valor de ganancia/penalizacion
	'''
	
	def __init__(self, direccion, valor):
		self.direccion = direccion
		self.valor = valor

	def getDireccion(self):
		return self.direccion

	def getValor(self):
		return self.valor

