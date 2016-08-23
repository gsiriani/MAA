# -*- coding: UTF-8 -*-

import Tkinter as tk
import time
import sys
import json
from damas import Casilla, Damas, Movimiento, Turno
from maquina import Maquina
from maquinaAzar import MaquinaAzar
from representacion import Representacion

class Estado():
    ORIGEN = 0
    DESTINO = 1

class Application():

    CASILLA_TAMANO = 64
    movimiento = None

    contrincanteBlancas = None
    contrincanteNegras = None

    def __init__(self, damas):
        self.root = tk.Tk()
        self.entry = tk.Entry(self.root)
        self.createWidgets()
        self.estado = Estado.ORIGEN
        self.damas = damas
        self.obtenerContrincantes()
        self.siguienteTurno()

    def createWidgets(self):
        self.tablero = tk.Canvas(bg='dark goldenrod',height=self.CASILLA_TAMANO*8, width=self.CASILLA_TAMANO*8)
        self.tablero.grid(row=0,column=0)
        self.tablero.bind("<Button-1>", self.onClick)
        self.root.bind("<Return>", self.onEnter)
        self.labelString = tk.StringVar()
        self.label = tk.Label(textvariable=self.labelString)
        self.label.grid(row=1,column=0)

    def obtenerContrincantes(self):

        if len(sys.argv) != 2:
            return

        file = open(sys.argv[1])

        config = json.load(file)

        if 'blancas' in config:
            if config['blancas']['tipo'] == 'azar':
                self.contrincanteBlancas = MaquinaAzar(Representacion())
            else:
                self.contrincanteBlancas = Maquina(Representacion())

            if 'pesos' in config['blancas']:
                self.contrincanteBlancas.weights = tuple(config['blancas']['pesos'])

        if 'negras' in config:
            if config['negras']['tipo'] == 'azar':
                self.contrincanteNegras = MaquinaAzar(Representacion())
            else:
                self.contrincanteNegras = Maquina(Representacion())

            if 'pesos' in config['negras']:
                self.contrincanteNegras.weights = tuple(config['negras']['pesos'])

        file.close()

    def onClick(self, event):

        clickX = event.x
        clickY = event.y

        x = clickY / self.CASILLA_TAMANO
        y = clickX / self.CASILLA_TAMANO

        if self.damas.tablero[x][y] == self.damas.turno:
            self.movimiento = Movimiento((x,y),[])
            self.estado = Estado.DESTINO
        elif self.estado == Estado.DESTINO and self.damas.tablero[x][y] == Casilla.VACIA:
            movimiento = Movimiento(self.movimiento.origen,self.movimiento.destino + [(x,y)])

            movimientosParciales = [m for m in self.damas.movimientosValidosCalculados if m.esParcial(movimiento)]

            if len(movimientosParciales) > 0:
                self.movimiento = movimiento
            else:
                self.resetearTurno()
        else:
            self.resetearTurno()

        self.dibujarTablero()

    def resetearTurno(self):

        self.movimiento = None
        self.estado = Estado.ORIGEN

    def siguienteTurno(self):

        if self.damas.turno == Turno.BLANCA and self.contrincanteBlancas is not None:
            contrincante = self.contrincanteBlancas
        elif self.damas.turno == Turno.NEGRA and self.contrincanteNegras is not None:
            contrincante = self.contrincanteNegras
        else:
            return

        decision = contrincante.decidirProximaJugada(self.damas)
        self.damas = decision.estadoResultante

        self.resetearTurno()
        self.dibujarTablero()

        self.root.after(1000,self.siguienteTurno)

    def onEnter(self,event):

        if self.movimiento is not None and len(self.movimiento.destino) > 0 :
            self.damas = self.damas.obtenerTableroResultante(self.movimiento)
            self.estado = Estado.ORIGEN

        self.resetearTurno()
        self.dibujarTablero()

        self.siguienteTurno()

    def run(self):
        self.root.mainloop()

    def dibujarMarca(self, pos, padding, color):

        y0 = pos[0] * self.CASILLA_TAMANO
        x0 = pos[1] * self.CASILLA_TAMANO

        self.tablero.create_oval(x0 + padding, y0 + padding, x0 + self.CASILLA_TAMANO - padding,
                                 y0 + self.CASILLA_TAMANO - padding, fill=color)

    def dibujarTablero(self):

        for fila in range(0, 8):
            for columna in range(0, 8):

                y0 = fila * self.CASILLA_TAMANO
                x0 = columna * self.CASILLA_TAMANO

                if (fila + columna) % 2 == 0:
                    self.tablero.create_rectangle(x0, y0, x0 + self.CASILLA_TAMANO, y0 + self.CASILLA_TAMANO,
                                                  fill='goldenrod')

                color = ''

                if self.damas.tablero[fila][columna] == Casilla.BLANCA:
                    color = 'white'
                elif self.damas.tablero[fila][columna] == Casilla.NEGRA:
                    color = 'gray11'

                if color != '':
                    self.dibujarMarca((fila, columna), 5, color)

        self.labelString.set(str(len(self.damas.movimientosValidosCalculados)) + " movimientos válidos")

        if self.movimiento is not None:
            movimientosValidos = self.damas.movimientosValidosDePieza(self.movimiento.origen[0],self.movimiento.origen[1])

            for movimiento in movimientosValidos:

                for x,y in movimiento.destino:
                    self.dibujarMarca((x, y), 25, 'yellow')

            self.dibujarMarca((self.movimiento.origen[0], self.movimiento.origen[1]), 25, 'red')

            for destino in self.movimiento.destino:
                self.dibujarMarca((destino[0], destino[1]), 25, 'red')

damas = Damas(Damas.tablero_base())

app = Application(damas)

app.dibujarTablero()
app.run()