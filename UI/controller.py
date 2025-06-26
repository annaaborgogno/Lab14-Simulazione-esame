import flet as ft


class Controller:
    def __init__(self, view, model):
        # the view, with the graphical elements of the UI
        self._view = view
        # the model, which implements the logic of the program and holds the data
        self._model = model

    def handle_graph(self, e):
        self._view.txt_result.controls.clear()
        self._model.buildGraph()
        nNodes, nEdges = self._model.getGraphDetails()
        self._view.txt_result.controls.append(ft.Text(f"Grafo correttamente creato!", color="green"))
        self._view.txt_result.controls.append(ft.Text(f"Il grafo ha {nNodes} nodi e {nEdges} archi"))
        min, max = self._model.getMinMax()
        self._view.txt_result.controls.append(ft.Text(f"Il peso minimo è {min} mentre quello massimo è {max}"))
        self._view.update_page()


    def handle_countedges(self, e):
        sInput = self._view.txt_name.value

        if sInput == "":
            self._view.txt_result2.controls.clear()
            self._view.txt_result2.controls.append(ft.Text(f"Inserire un numero!", color="red"))
            self._view.update_page()
            return

        try:
            s = float(sInput)
        except ValueError:
            self._view.txt_result2.controls.clear()
            self._view.txt_result2.controls.append(ft.Text(f"Inserire un valore numerico!", color="red"))
            self._view.update_page()
            return

        minVal, maxVal = self._model.getMinMax()
        if s > maxVal or s < minVal:
            self._view.txt_result2.controls.clear()
            self._view.txt_result2.controls.append(ft.Text(f"Il valore non è nel range dei pesi!", color="red"))
            self._view.update_page()
            return

        nEdgesMin, nEdgesMax = self._model.getNumEdgesSoglia(s)
        self._view.txt_result2.controls.clear()
        self._view.txt_result2.controls.append(ft.Text(f"Gli archi con peso minore della soglia sono {nEdgesMin}, quelli maggiori {nEdgesMax}"))
        self._view.update_page()

    def handle_search(self, e):
        sInput = self._view.txt_name.value

        if sInput == "":
            self._view.txt_result2.controls.clear()
            self._view.txt_result2.controls.append(ft.Text(f"Inserire un numero!", color="red"))
            self._view.update_page()
            return

        try:
            s = float(sInput)
        except ValueError:
            self._view.txt_result3.controls.clear()
            self._view.txt_result2.controls.append(ft.Text(f"Inserire un valore numerico!", color="red"))
            self._view.update_page()
            return

        minVal, maxVal = self._model.getMinMax()
        if s > maxVal or s < minVal:
            self._view.txt_result3.controls.clear()
            self._view.txt_result3.controls.append(ft.Text(f"Il valore non è nel range dei pesi!", color="red"))
            self._view.update_page()
            return

        bestPath, bestWeight = self._model.bestWeight(s)
        self._view.txt_result3.controls.clear()
        self._view.txt_result3.controls.append(ft.Text(f"Il cammino trovato ha peso {bestWeight}"))
        for n in bestPath:
            self._view.txt_result3.controls.append(ft.Text(n))
        self._view.update_page()
