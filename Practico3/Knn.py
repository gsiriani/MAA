from math import sqrt


class Knn:


        def __init__ (self, ejemplos, atributoObjetivo, atributos):
            # agrego en ejemplos los datos para luego ser usados como punto de comparacion
            self.ejemplos = ejemplos
            self.ponderaciones = self.ponderar(ejemplos, atributos)
            self.atributoObjetivo = atributoObjetivo


        def ejecutar (self, datos, atributos, k):
            # inicio una lista que contendra 1 si acerte la prediccion y 0 en caso contrario (para cada dato ingresado en la variable "datos")
            resultado = {}

            for d in datos:
                # calculo las distacias entre todos mis ejemplos y mi objetivo d y las guardo (junto con sus respectivos ejemplos) en la variable distancias
                distancias = self.distancias(atributos,d)
                # seran los vecinos mas cercanos
                neighbors = {}

                for i in range (k):
                    nn = min(distancias,key=lambda item:item[1])
                    neighbors[i] = nn
                    distancias.remove(nn)

                #calculo un promedio basado en la distancia, dando mas importancia a los mas cercanos
                promedio = calcularValorPromedio(neighbors)

                resultado.append(1 if promedio == d[self.atributoObjetivo] else 0)

            # retorno el exito
            return (sum (resultado) / len(datos))


        def distancias (self, atributos, objetivo):
            # esto fue lo que hice y como no se mucho de python seguramente habia formas mas prolijas de hacerlo
            distancias = {}
            elemento = 0
            # para cada elemento calculo la distancia euclidiana como dice en el teorico
            for e in self.ejemplos:
                distancias[elemento] = ( e, sqrt (sum (self.obtenerDiferencias(e,atributos, objetivo))) )
                elemento += 1

            return distancias

        def obtenerDiferencias (self, ejemplo, atributos, objetivo):
            # mas del humo de arriba solo que multiplico por las ponderaciones para priorizar ciertos atributos sobre otros
            diferencias = {}

            for a in atributos:
                diferencias[a[0]] = ( self.ponderaciones[a[0]] * self.diferencia(ejemplo, objetivo, a[0], a[1]))**2

            return diferencias


        def diferencia (self, ejemplo, objetivo, nomAtributo, atributosPosibles):
            #aca es donde revienta todo a la mierda, lo que pretendia es calcular la diferencia entre los indices de los valores de mi ejemplo y los indices de los valores de mi objetivo
            return abs(atributosPosibles.index(ejemplo[nomAtributo]) - atributosPosibles.index(objetivo[nomAtributo])) / len(atributosPosibles)

        def calcularValorPromedio(self, neighbors):
            #calculo el valor promedio tomando en cuenta las distancias (n[1])
            return sum (n[1]*n[0][self.ValorObjetivo] for n in neighbors) / sum (n[1] for n in neighbors)

        def ponderar(self, ejemplos, atributos):
            # TODO: cambiar esta bazofia
            ponderaciones = {}
            for a in atributos:
                ponderaciones[a[0]] = 1
            return ponderaciones

        # pd. que mierda python que no te deja poner letras con tilde
