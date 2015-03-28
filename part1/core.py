
from grafo import Grafo
from interface import Interface

class Core:

    def __init__(self):
        self.grafo = Grafo()
        self.interface = Interface()
        self.filename = ''

    def setDataFilename(self, filename):
        self.filename = filename

    def loadData(self):
        if len(self.filename) > 0:
            self.grafo.load(self.filename)

    def getMainMenu(self):
        return self.interface.getMainMenu()

    def setInference(self, rule):
        self.grafo.applyinference(rule)

    def getInferencedData(self, predicate):
        return self.grafo.triples(None,predicate,None)