# -*- coding: UTF-8 -*-

from math import sqrt
import random

class Knn:

        def __init__ (self, ejemplos, atributoObjetivo, atributos, operadores):
            # agrego en ejemplos los datos para luego ser usados como punto de comparacion
            self.ejemplos = ejemplos
            self.ponderaciones = {a:1 for a in atributos}
            self.atributoObjetivo = atributoObjetivo
            self.atributos = list(atributos)
            self.atributos.remove('G3')
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


        def distancias (self, ejemplos, atributos, objetivo):
            return [(e, sqrt (sum (self.obtenerDiferencias(e,atributos, objetivo)))) for e in ejemplos]

        def obtenerDiferencias (self, ejemplo, atributos, objetivo):
            # mas del humo de arriba solo que multiplico por las ponderaciones para priorizar ciertos atributos sobre otros
            return [1 / self.ponderaciones[a] * self.operadores[a](objetivo[a],ejemplo[a])**2 for a in atributos]

        def calcularValorPromedio(self, neighbors):
            #calculo el valor promedio tomando en cuenta las distancias (n[1])
            vecinosDistanciaCero = [n for n in neighbors if n[1] == 0]

            if len(vecinosDistanciaCero) > 0:
                return random.choice(vecinosDistanciaCero)[0][self.atributoObjetivo]
            else:
                distanciaTotal = sum(n[1] for n in neighbors)
                return sum([n[0][self.atributoObjetivo] * distanciaTotal/n[1] for n in neighbors])

        def entrenarPonderaciones(self, numeroDeBloques, k, factorAprendizaje, cantidadIteraciones):
            ''''
                Se realiza una validacion cruzada, utilizando aprendizaje por gradiente de descenso estocastico
                para aproximar la función de ponderaciones
            '''

            ejemplos = list(self.ejemplos)

            self.ponderaciones = {k:random.uniform(0,1) for k in self.ponderaciones.keys()}

            for i in range(cantidadIteraciones):

                random.shuffle(ejemplos)

                tamanoBloque = len(ejemplos) / numeroDeBloques

                for pos in range(0, len(ejemplos), tamanoBloque):
                    conjuntoEntrenamiento = ejemplos[:pos] + ejemplos[pos+tamanoBloque:]
                    conjuntoValidacion = ejemplos[pos: pos+tamanoBloque]
                    self.entrenar(conjuntoEntrenamiento, conjuntoValidacion, k, factorAprendizaje)

                print(str(i + 1) + " iteraciones")

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

                neighbors = self.obtenerVecinos(distancias, k)

                promedio = self.calcularValorPromedio(neighbors)

                error = d[self.atributoObjetivo] - promedio

                for key,value in self.ponderaciones.iteritems():
                    self.ponderaciones[key] = max(0,value + factorAprendizaje * error * d[key])


