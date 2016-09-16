# -*- coding: UTF-8 -*-

from math import sqrt
import random


class Knn:


        def __init__ (self, ejemplos, atributoObjetivo, atributos, operadores):
            # agrego en ejemplos los datos para luego ser usados como punto de comparacion
            self.ejemplos = ejemplos
            self.ponderaciones = self.ponderar(ejemplos, atributos)
            self.atributoObjetivo = atributoObjetivo
            self.atributos = list(atributos)
            self.atributos.remove('G3')
            self.operadores = operadores


        def validar(self, datos, k):


            # inicio una lista que contendra 1 si acerte la prediccion y 0 en caso contrario (para cada dato ingresado en la variable "datos")
            resultado = []

            for d in datos:
                # calculo las distacias entre todos mis ejemplos y mi objetivo d y las guardo (junto con sus respectivos ejemplos) en la variable distancias
                distancias = self.distancias(self.atributos,d)
                # seran los vecinos mas cercanos
                neighbors = []

                for i in range (k):
                    nn = min(distancias,key=lambda v:v[1])
                    neighbors.append(nn)
                    distancias.remove(nn)

                #calculo un promedio basado en la distancia, dando mas importancia a los mas cercanos
                promedio = self.calcularValorPromedio(neighbors)

                resultado.append(1 if promedio == d[self.atributoObjetivo] else 0)

            # retorno el exito
            return float(sum (resultado)) / len(datos)


        def distancias (self, atributos, objetivo):
            return [(e, sqrt (sum (self.obtenerDiferencias(e,atributos, objetivo)))) for e in self.ejemplos]

        def obtenerDiferencias (self, ejemplo, atributos, objetivo):
            # mas del humo de arriba solo que multiplico por las ponderaciones para priorizar ciertos atributos sobre otros
            return [self.ponderaciones[a] * self.operadores[a](objetivo[a],ejemplo[a])**2 for a in atributos]

        def calcularValorPromedio(self, neighbors):
            #calculo el valor promedio tomando en cuenta las distancias (n[1])
            distancia = sum (n[1] for n in neighbors)
            if distancia == 0:
                return random.choice(neighbors)[0][self.atributoObjetivo]
            else:
                return round(float(sum (n[1]*(n[0][self.atributoObjetivo] + 1) for n in neighbors)) / distancia - 1)

        def ponderar(self, ejemplos, atributos):
            # TODO: cambiar esta bazofia
            ponderaciones = {}
            for a in atributos:
                ponderaciones[a] = 1
            return ponderaciones

        # pd. que mierda python que no te deja poner letras con tilde áadsdsadásdasd
