from mundo import Mundo, setCasilla
from casilla import Casilla

# CREO EL MUNDO DEL PROBLEMA
# --------------------------

# Mundo por defecto de tamano 6*6
mundo = Mundo(6)
# Transiciones con valores especiales
mundo.setCasilla(1, 1, Casilla(izquierda=0, derecha=-20, arriba=0, abajo=0))
mundo.setCasilla(1, 2, Casilla(izquierda=0, derecha=0, arriba=0, abajo=80))
mundo.setCasilla(1, 3, Casilla(izquierda=0, derecha=0, arriba=0, abajo=80))
mundo.setCasilla(1, 4, Casilla(izquierda=-20, derecha=0, arriba=0, abajo=0))
mundo.setCasilla(4, 2, Casilla(izquierda=0, derecha=0, arriba=20, abajo=0))
mundo.setCasilla(4, 3, Casilla(izquierda=0, derecha=0, arriba=20, abajo=0))
# Las casillas del Goal no tienen transiciones hacia afuera
mundo.setCasilla(2, 2, Casilla(izquierda=None, derecha=None, arriba=None, abajo=None))
mundo.setCasilla(2, 3, Casilla(izquierda=None, derecha=None, arriba=None, abajo=None))
mundo.setCasilla(3, 2, Casilla(izquierda=None, derecha=None, arriba=None, abajo=None))
mundo.setCasilla(3, 3, Casilla(izquierda=None, derecha=None, arriba=None, abajo=None))

