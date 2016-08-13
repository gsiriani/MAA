import Tkinter as tk
from ajedrez import Casilla, Tablero

class Application():

    CASILLA_TAMANO = 64

    def __init__(self):
        self.root = tk.Tk()
        self.entry = tk.Entry(self.root)
        self.createWidgets()

    def createWidgets(self):
        self.tablero = tk.Canvas(bg='dark goldenrod',height=self.CASILLA_TAMANO*8, width=self.CASILLA_TAMANO*8)
        self.tablero.grid()

    def run(self):
        self.root.mainloop()

    def draw(self, t):
        for fila in range(0, 8):
            for columna in range(0, 8):

                y0 = fila * self.CASILLA_TAMANO
                x0 = columna * self.CASILLA_TAMANO

                if (fila + columna) % 2 == 0:
                    self.tablero.create_rectangle(x0,y0,x0+self.CASILLA_TAMANO,y0+self.CASILLA_TAMANO,fill='goldenrod')

                color = ''

                if t.tablero[fila][columna] == Casilla.BLANCA:
                    color = 'white'
                elif t.tablero[fila][columna] == Casilla.NEGRA:
                    color = 'gray11'

                if color != '':
                    self.tablero.create_oval(x0 + 5, y0 + 5, x0 + self.CASILLA_TAMANO - 5, y0 + self.CASILLA_TAMANO - 5, fill=color)

app = Application()
tablero = Tablero()
tablero.iniciar_tablero()
tablero.tablero_base()
app.draw(tablero)
app.run()