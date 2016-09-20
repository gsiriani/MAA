# -*- coding: UTF-8 -*-

from math import sqrt
import random
import math
class Knn:

        def __init__ (self, ejemplos, atributoObjetivo, atributos, operadores, ponderaciones = None):
            # agrego en ejemplos los datos para luego ser usados como punto de comparacion
            self.ejemplos = ejemplos
            self.atributos = list(atributos)
            self.atributos.remove(atributoObjetivo)
            if ponderaciones is None:
                self.ponderaciones = {a:1 for a in self.atributos}
            else:
                self.ponderaciones = ponderaciones
            self.atributoObjetivo = atributoObjetivo
            self.operadores = operadores


        def validar(self, datos, k):


            # inicio una lista que contendra 1 si acerte la prediccion y 0 en caso contrario (para cada dato ingresado en la variable "datos")
            resultado = []

            for d in datos:
                # calculo las distacias entre todos mis ejemplos y mi objetivo d y las guardo (junto con sus respectivos ejemplos) en la variable distancias
                distancias = self.distancias(self.ejemplos, self.atributos,d)
                # seran los vecinos mas cercanos
                neighbors = self.obtenerVecinos(distancias, k)

                #calculo un promedio basado en la distancia, dando mas importancia a los mas cercanos
                promedio = round(self.calcularValorPromedio(neighbors))

                resultado.append(1 if promedio == d[self.atributoObjetivo] else 0)

            # retorno el exito
            return float(sum (resultado)) / len(datos)


        def distancias(self, ejemplos, atributos, objetivo):
            return [(e, self.distanciaEntre(e,objetivo, atributos)) for e in ejemplos]

        def distanciaEntre(self,a, b, atributos):
            return sqrt(sum(self.obtenerDiferencias(a, b, atributos)))

        def obtenerDiferencias (self, ejemplo, objetivo, atributos):
            # mas del humo de arriba solo que multiplico por las ponderaciones para priorizar ciertos atributos sobre otros
            return [self.ponderaciones[a]**2 * self.operadores[a](objetivo[a],ejemplo[a])**2 for a in atributos]

        def calcularValorPromedio(self, neighbors):
            #calculo el valor promedio tomando en cuenta las distancias (n[1])
            vecinosDistanciaCero = [n for n in neighbors if n[1] == 0]

            if len(vecinosDistanciaCero) > 0:
                return random.choice(vecinosDistanciaCero)[0][self.atributoObjetivo]
            else:
                inversoDistanciaTotal = sum(1/n[1] for n in neighbors)
                return sum([n[0][self.atributoObjetivo]*1/n[1] for n in neighbors])/inversoDistanciaTotal

        def entrenarPonderaciones(self, numeroDeBloques, k, factorAprendizaje, cantidadIteraciones):
            ''''
                Se realiza una validacion cruzada, utilizando aprendizaje por gradiente de descenso estocastico
                para aproximar la función de ponderaciones
            '''

            ejemplos = list(self.ejemplos)

            self.ponderaciones = {k:random.uniform(0,0) for k in self.ponderaciones.keys()}

            for i in range(cantidadIteraciones):

                random.shuffle(ejemplos)

                tamanoBloque = len(ejemplos) / numeroDeBloques

                for pos in range(0, len(ejemplos), tamanoBloque):
                    conjuntoEntrenamiento = ejemplos[:pos] + ejemplos[pos+tamanoBloque:]
                    conjuntoValidacion = ejemplos[pos: pos+tamanoBloque]
                    self.entrenar(conjuntoEntrenamiento, conjuntoValidacion, k, factorAprendizaje)

                print(str(i + 1) + " iteraciones")
                print self.ponderaciones

        def obtenerVecinos(self, distancias, k):

            neighbors = []

            for i in range(k):
                nn = min(distancias, key=lambda v: v[1])
                neighbors.append(nn)
                distancias.remove(nn)

            return neighbors

        def entrenar(self, conjuntoEntrenamiento, conjuntoValidacion, k, factorAprendizaje):

            for d in conjuntoValidacion:

                distancias = self.distancias(conjuntoEntrenamiento, self.atributos,d)

                # promedio = self.calcularValorPromedio(self.obtenerVecinos(distancias, 3))

                #if round(promedio) == d[self.atributoObjetivo]:
                #    continue

                distancias.sort(key=lambda n:n[1])
                distancias = distancias[:k]

                for target in distancias:
                    distanciaEntre = self.distanciaEntre(target[0],d,self.atributos)
                    if distanciaEntre != 0:
                        error = (d[self.atributoObjetivo] - target[0][self.atributoObjetivo])**2/distanciaEntre
                    else:
                        error = (d[self.atributoObjetivo] - target[0][self.atributoObjetivo])**2 * 100

                    for key,value in self.ponderaciones.iteritems():
                        diferencia = self.operadores[key](target[0][key], d[key])
                        self.ponderaciones[key] = value + factorAprendizaje * error * diferencia
