import copy

import networkx as nx
from database.DAO import DAO


class Model:
    def __init__(self):
        self._nodes = []
        self._edges = []
        self._edgesMaggiori = []
        self._idMap = {}
        self._graph = nx.DiGraph()
        self._bestPath = []
        self._bestWeight = 0

    def bestWeight(self, soglia):
        self._bestPath = []
        self._bestWeight = 0
        self.getEdgesMaggiori(soglia)
        for e in self._edgesMaggiori:
            parziale = [e]
            self._ricorsione(parziale)
            parziale.pop()
        return self._bestPath, self._bestWeight

    def _ricorsione(self, parziale):
        if self._calcolaPeso(parziale) > self._bestWeight:
            self._bestPath = parziale
            self.bestPath = copy.deepcopy(parziale)

        for n in self._graph.successors(parziale[-1][1]):
            if self._graph.has_edge(parziale[-1][1], n) and (parziale[-1][1], n) in self._edgesMaggiori:
                parziale.append(parziale[-1][1],n)
                print(parziale)
                self._ricorsione(parziale)
                parziale.pop()

    def buildGraph(self):
        self._graph.clear()
        self._idMap = {}
        self._nodes = DAO.getAllChromosomes()
        for n in self._nodes:
            self._idMap[n.chr] = n
        self.addAllEdges()
        return self._graph


    def addAllEdges(self):
        self._edges = DAO.getEdges()
        for e in self._edges:
            u = self._idMap[e.chr1]
            v = self._idMap[e.chr2]
            self._graph.add_edge(u, v, weight=e.peso)

    def getGraphDetails(self):
        nNodes = self._graph.number_of_nodes()
        nEdges = self._graph.number_of_edges()
        return nNodes, nEdges

    def getMinMax(self):
        min = float("inf")
        max = 0
        for e in self._edges:
            if e.peso < min:
                min = e.peso
            elif e.peso > max:
                max = e.peso

        return min, max

    def getNumEdgesSoglia(self, soglia):
        nEdgesMin = 0
        nEdgesMax = 0

        for e in self._edges:
            if e.peso > soglia:
                nEdgesMax += 1
            elif e.peso < soglia:
                nEdgesMin += 1

        return nEdgesMin, nEdgesMax

    def getEdgesMaggiori(self, soglia):
        self._edgesMaggiori = []
        print(self._edges)
        for e in self._edges:
            if e.peso > soglia:
                self._edgesMaggiori.append(e)
        return self._edgesMaggiori

    def _calcolaPeso(self, listOfEdges):
        pesoParziale = 0
        for e in listOfEdges:
            nodo1 = self._idMap[e.chr1]
            nodo2 = self._idMap[e.chr2]
            pesoParziale += self._graph[nodo1][nodo2]["weight"]
            print(f"Tentativo accesso a: {nodo1}, {nodo2}")
            print(f"Nodi nel grafo: {list(self._graph.nodes)}")
        return pesoParziale