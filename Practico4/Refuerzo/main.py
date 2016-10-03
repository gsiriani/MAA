from mundo import Mundo
from casilla import Casilla
from aprendizajeQ import AprendizajeQ

# CREO EL MUNDO DEL PROBLEMA
# --------------------------

print 'Construyendo mundo'
# Mundo por defecto de tamano 6*6
sizeMundo = 6
mundo = Mundo(sizeMundo)
# Transiciones con valores especiales
mundo.setCasilla(1, 1, Casilla(izquierda=0, derecha=-20, arriba=0, abajo=0))
mundo.setCasilla(1, 2, Casilla(izquierda=0, derecha=0, arriba=0, abajo=80))
mundo.setCasilla(1, 3, Casilla(izquierda=0, derecha=0, arriba=0, abajo=80))
mundo.setCasilla(1, 4, Casilla(izquierda=-20, derecha=0, arriba=0, abajo=0))
mundo.setCasilla(4, 2, Casilla(izquierda=0, derecha=0, arriba=20, abajo=0))
mundo.setCasilla(4, 3, Casilla(izquierda=0, derecha=0, arriba=20, abajo=0))
# Las casillas del Goal no tienen transiciones hacia afuera
mundo.setCasilla(2, 2, Casilla())
mundo.setCasilla(2, 3, Casilla())
mundo.setCasilla(3, 2, Casilla())
mundo.setCasilla(3, 3, Casilla())

print 'Comienza entrenamiento'

# ENTRENO PARA GAMMA = 0.8
# ------------------------
print '\nDescuento = 0.8\n--------------'

# Inicializo el algoritmo
algoritmoQ = AprendizajeQ(mundo, 0.8)

print '5 iteraciones:'
rQ = algoritmoQ.entrenar(5)

for i in range(sizeMundo):
	fila = ''
	for j in range(sizeMundo):
		c = rQ.getCasilla(i,j)
		fila += ' ' + str(c.maximaDireccionPosible())
	print fila

print '10 iteraciones:'
rQ = algoritmoQ.entrenar(5, rQ)

for i in range(sizeMundo):
	fila = ''
	for j in range(sizeMundo):
		c = rQ.getCasilla(i,j)
		fila += ' ' + str(c.maximaDireccionPosible())
	print fila

print '30 iteraciones:'
rQ = algoritmoQ.entrenar(20, rQ)

for i in range(sizeMundo):
	fila = ''
	for j in range(sizeMundo):
		c = rQ.getCasilla(i,j)
		fila += ' ' + str(c.maximaDireccionPosible())
	print fila



# ENTRENO PARA GAMMA = 0.4
# ------------------------
print '\nDescuento = 0.4\n--------------'

# Inicializo el algoritmo
algoritmoQ = AprendizajeQ(mundo, 0.4)

print '5 iteraciones:'
rQ = algoritmoQ.entrenar(5)

for i in range(sizeMundo):
	fila = ''
	for j in range(sizeMundo):
		c = rQ.getCasilla(i,j)
		fila += ' ' + str(c.maximaDireccionPosible())
	print fila

print '10 iteraciones:'
rQ = algoritmoQ.entrenar(5, rQ)

for i in range(sizeMundo):
	fila = ''
	for j in range(sizeMundo):
		c = rQ.getCasilla(i,j)
		fila += ' ' + str(c.maximaDireccionPosible())
	print fila

print '30 iteraciones:'
rQ = algoritmoQ.entrenar(20, rQ)

for i in range(sizeMundo):
	fila = ''
	for j in range(sizeMundo):
		c = rQ.getCasilla(i,j)
		fila += ' ' + str(c.maximaDireccionPosible())
	print fila
