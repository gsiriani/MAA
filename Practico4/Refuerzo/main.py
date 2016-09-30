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

# Inicializo el algoritmo
algoritmoQ = AprendizajeQ(mundo, 0.8)

print 'Comienza entrenamiento'

# Entreno
rQ = algoritmoQ.entrenar(5)

for i in range(sizeMundo):
	for j in range(sizeMundo):
		c = rQ.getCasilla(i,j)
		print 'Casilla (' + str(i) + ',' + str(j) +'):'
		print '\t Direccion: ' + str(c.maximaDireccionPosible())