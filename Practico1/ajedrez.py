from enum import Enum

class Casilla(Enum):
	# Enum que representa el estado de una casilla en el tablero
	blanca = 1 	# La casilla tiene una ficha blanca
	negra = 2	# La casilla tiene una ficha negra
	vacia = 3	# La casilla esta vacia
	invalida = 4	# La casilla es invalida

def iniciar_tablero():
	# Retorna un tablero inicial

	# Declaro la variable 
	tablero = [[0 for x in range(8)] for y in range(8)]

	# Completo las primeras 3 hileras con fichas blancas y casillas invalidas
	for x in range(0,3):
		for y in range(8):
			if ((x + y) % 2) == 0:
				tablero[x][y] = Casilla.blanca
			else:
				tablero[x][y] = Casilla.invalida

	# Completo las siguientes 2 hileras con casillas vacias y casillas invalidas
	for x in range(3,5):
		for y in range(8):
			if ((x + y) % 2) == 0:
				tablero[x][y] = Casilla.vacia
			else:
				tablero[x][y] = Casilla.invalida

	# Completo las ultimas 3 hileras con fichas negras y casillas invalidas
	for x in range(5,8):
		for y in range(8):
			if ((x + y) % 2) == 0:
				tablero[x][y] = Casilla.negra
			else:
				tablero[x][y] = Casilla.invalida

	return tablero


t = iniciar_tablero()
for f in t:
	print f