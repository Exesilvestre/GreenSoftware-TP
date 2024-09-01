class BusquedaBinaria:
    def buscar(self, lista, objetivo):
        bajo, alto = 0, len(lista) - 1
        while bajo <= alto:
            medio = (bajo + alto) // 2
            if lista[medio] == objetivo:
                return medio
            elif lista[medio] < objetivo:
                bajo = medio + 1
            else:
                alto = medio - 1
        return -1
