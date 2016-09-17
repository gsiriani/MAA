

class Bayes:
	'''
	Clase que implementa el aprendizaje bayesiano
	''' 

	def __init__(self, atributoObjetivo, atributos, valoresPosibles):
		'''
		La clase se inicializa con el atributo objetivo que sera buscado
		por el algoritmo
		'''

		self.atributoObjetivo = atributoObjetivo
		self.atributos = atributos
		self.valoresPosibles = valoresPosibles

	def entrenar(self, ejemplos, ajuste = 0):
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

		atributos = self.atributos

		valPosibles = self.valoresPosibles[self.atributoObjetivo]
		probabilidades = {}
		probabilidadesCondicionadas = {}

		ajustarCantidad = False

    	# Obtengo cantidad de apariciones de cada valor
		cantidades = {}
		for v in valPosibles:
			cantidadTotal = len([e for e in ejemplos if e[self.atributoObjetivo] == v])
			cantidades[v] = {'total': cantidadTotal, 'totalCondicionada': {}, 'condicionada': {}}
			if cantidadTotal == 0: # No tengo ningun ejemplo que corresponda a algun valor posible del atr. objetivo
				ajustarCantidad = True

			# Obtengo cantidad condicionada
			ajustarCantidadCondicionada = False
			for nomAtributo in self.atributos:
				cantidades[v]['totalCondicionada'][nomAtributo] = cantidadTotal
				cantidades[v]['condicionada'][nomAtributo] = {}
				for p in self.valoresPosibles[nomAtributo]:
					cantCond = len([e for e in ejemplos if e[nomAtributo] == p and e[self.atributoObjetivo] == v])
					cantidades[v]['condicionada'][nomAtributo][p] = cantCond

				# DESCOMENTAR EL SIGUIENTE BLOQUE SI SE DESEA REALIZAR AJUSTE EN LAS CONDICIONADAS
				#---------------------------------------------------------------------------------
					if cantCond == 0:
						ajustarCantidadCondicionada = True
				# Si es necesario, agrego ejemplos condicionados al atributo objetivo
				if ajustarCantidadCondicionada:
					for p in self.valoresPosibles[nomAtributo]:
						cantidades[v]['condicionada'][nomAtributo][p] += ajuste
					cantidades[v]['totalCondicionada'][nomAtributo] += ajuste*len(self.valoresPosibles[nomAtributo])
				# ----------------------------------------------------------------------------------

		cantidadEjemplosAtributo = cantidadEjemplos
		# Si es necesario, agrego ejemplos
		if ajustarCantidad:
			for v in valPosibles:
				cantidades[v]["total"] += ajuste
			cantidadEjemplosAtributo = cantidadEjemplos + ajuste*len(valPosibles)

		# Calculo probabilidades del atributo
		for v in valPosibles:
			probabilidades[v] = float(cantidades[v]["total"])/cantidadEjemplosAtributo
			probabilidadesCondicionadas[v] = {}
			for nomAtributo in self.atributos:
				probabilidadesCondicionadas[v][nomAtributo] = {}
				for p in self.valoresPosibles[nomAtributo]:
					if cantidades[v]['totalCondicionada'][nomAtributo] == 0:
						probabilidadesCondicionadas[v][nomAtributo][p] = 0
					else:
						probabilidadesCondicionadas[v][nomAtributo][p] = float(cantidades[v]['condicionada'][nomAtributo][p]) / cantidades[v]['totalCondicionada'][nomAtributo]

		return (probabilidades, probabilidadesCondicionadas)


	def validarLista(self, lista, probabilidades, probabilidadesCondicionadas):
		'''
		Retorna el promedio de aciertos en la evaluacion de la lista de ejemplos segun
		 las probabilidades calculadas
		'''
		correctos = 0
		for e in lista:
			estimado = self.evaluar(e, probabilidades, probabilidadesCondicionadas)
			if estimado == e[self.atributoObjetivo]:
				correctos += 1
		return float(correctos)/len(lista)


	def evaluar(self, ejemplo, probabilidades, probabilidadesCondicionadas):
		'''
		Retorna el valor mas probable para el atributo objetivo, dadas las probabilidades previamente calculadas
		'''

		p = {} # Diccionario de probabilidades para el ejemplo
		for valor in self.valoresPosibles[self.atributoObjetivo]:
			p[valor] = self.calcularProbabilidad(ejemplo, probabilidades[valor], probabilidadesCondicionadas[valor])

		return max(p.iteritems(), key=lambda (k, v): v)[0]


	def calcularProbabilidad(self, ejemplo, probabilidad, probabilidadesCondicionadas):
		'''
		Calcula la probabilidad de que un ejemplo tenga determinado 'valor' en el atributo objetivo
		basandose en las probabilidades previamente calculadas
		'''
		probCalc = probabilidad

		for (k, v) in ejemplo.iteritems():
			if k in self.atributos:
				probCalc = probCalc*probabilidadesCondicionadas[k][v]

		return probCalc
