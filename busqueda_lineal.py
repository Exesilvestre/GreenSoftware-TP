class BusquedaLineal:
    def buscar(self, lista, objetivo):
        for i in range(len(lista)):
            if lista[i] == objetivo:
                return i
        return -1
