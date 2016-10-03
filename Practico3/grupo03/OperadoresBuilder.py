class OperadoresBuilder:

    @staticmethod
    def multiple(operadores, fn, atributos, valoresPosibles = None):
        for a in atributos:
            if valoresPosibles is None:
                operadores[a] = fn()
            else:
                valoresPosiblesNum = [int(v) for v in valoresPosibles[a]]
                operadores[a] = fn(valoresPosiblesNum)

    @staticmethod
    def hamming():
        return lambda x,y: 1 if x != y else 0

    @staticmethod
    def rango(valoresPosibles):
        return lambda x,y: float(abs(int(x)-int(y)))/(max(valoresPosibles) - min(valoresPosibles))

