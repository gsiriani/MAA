

class Bayes:
	'''
	Clase que implementa el aprendizaje bayesiano
	''' 

	def __init__(self, atributoObjetivo, valoresPosibles):
        '''
        La clase se inicializa con el atributo objetivo que sera buscado
        por el algoritmo
        '''
        self.atributoObjetivo = atributoObjetivo
        self.valoresPosibles = valoresPosibles

    def ejecutar(self, ejemplos, atributos, ajuste = 1):
        '''
        Se ejecuta el algoritmo sobre la lista de datos "ejemplos", considerando los
        atributos "atributos".
        El algoritmo calcula la probabilidad de cada valor de cada atributo y la probabilidad condicionada
        de dicho valor en funcion del valor del atributo objetivo.
        El parametro "ajuste" indica la cantidad de ejemplos a agregar para cada valor en caso de que no 
        haya ningun ejemplo para algun valor posible de un atributo.
        '''

        # Calculo cantidad total de ejemplos
        cantidadEjemplos = len(ejemplos)

        # Inicializo el diccionario de probabilidades
        probabilidades = {}
        probabilidadesCondicionadas = {}

        for (nomAtributo, valPosibles) in atributos:
        	probabilidades[nomAtributo] = {}
        	probabilidadesCondicionadas[nomAtributo] = {}

        	ajustarCantidad = False

        	# Obtengo cantidad de apariciones de cada valor
        	cantidades = {}
			for v in valPosibles:
				cantidadTotal = len([e for e in ejemplos if e[nomAtributo] == v])
				cantidades[v] = {'total': cantidadTotal, 'totalCondicionada': cantidadTotal, 'condicionada': {}}
				if cantidadTotal == 0
					ajustarCantidad = True

				# Obtengo cantidad condicionada
				ajustarCantidadCondicionada = False
				for p in self.valoresPosibles:
					cantCond = len([e for e in ejemplos if e[nomAtributo] == v and e[atributoObjetivo] == p])
					cantidades[v]['condicionada'][p] = cantCond
					if cantCond == 0:
						ajustarCantidadCondicionada = True
				# Si es necesario, agrego ejemplos condicionados al atributo objetivo
				if ajustarCantidadCondicionada:
					for p in self.valoresPosibles:
						cantidades[v]['condicionada'][p] += ajuste
					cantidades[v]['totalCondicionada'] += ajuste*len(self.valoresPosibles)

			cantidadEjemplosAtributo = cantidadEjemplos
			# Si es necesario, agrego ejemplos
			if ajustarCantidad:
				for v in valPosibles:
					cantidades[v] += ajuste
				cantidadEjemplosAtributo = cantidadEjemplos + ajuste*len(valPosibles)

			# Calculo probabilidades del atributo
			for v in valPosibles:
				probabilidades[nomAtributo][v] = float(cantidades[v]/cantidadEjemplosAtributo)
				probabilidadesCondicionadas[nomAtributo][v] = {}
				for p in self.valoresPosibles:
					probabilidadesCondicionadas[nomAtributo][v][p] = float(cantidades[v]['condicionada'][p] / cantidades[v]['totalCondicionada'])

		return (probabilidades, probabilidadesCondicionadas)


	def validar(self, ejemplo, probabilidades, probabilidadesCondicionadas):
		'''
		Retorna el valor mas probable para el atributo objetivo, dadas las probabilidades previamente calculadas
		'''

		p = {} # Diccionario de probabilidades para el ejemplo
		for valor in self.valoresPosibles:
			p[valor] = self.calcularProbabilidad(ejemplo, probabilidades, probabilidadesCondicionadas, valor)

		return max(p.iteritems(), key=lambda (k, v): v)[0]


	def calcularProbabilidad(self, ejemplo, probabilidades, probabilidadesCondicionadas, valor):
		'''
		Calcula la probabilidad de que un ejemplo tenga determinado 'valor' en el atributo objetivo
		basandose en las probabilidades previamente calculadas
		'''

		probabilidad = probabilidades[self.atributoObjetivo][valor]

		for (k, v) in ejemplo.iteritems():
			probabilidad = float(probabilidad*probabilidades[k][v]*probabilidadesCondicionadas[k][v][valor])

		return probabilidad
