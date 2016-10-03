class Direccion:
	'''
	Enum que representa las distintas direcciones en que me puedo mover
	'''
	ARRIBA = 'A'
	ABAJO = 'V'
	IZQUIERDA = '<'
	DERECHA = '>'

class Movimiento:
	'''
	Clase que representa un movimiento realizado con su direccion y 
	valor de ganancia/penalizacion
	'''
	
	def __init__(self, origen, destino, direccion, valor=0):
		self.origen = origen
		self.destino = destino
		self.direccion = direccion
		self.valor = valor

	def getOrigen(self):
		return self.origen

	def getDestino(self):
		return self.destino

	def getDireccion(self):
		return self.direccion

	def getValor(self):
		return self.valor

