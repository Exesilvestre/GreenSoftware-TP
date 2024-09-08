import random
import time
import pandas as pd
from codecarbon import EmissionsTracker
from busqueda_lineal import BusquedaLineal
from busqueda_binaria import BusquedaBinaria

def rastrear_emisiones(func, *args, **kwargs):
    rastreador = EmissionsTracker()
    rastreador.start()
    resultado = func(*args, **kwargs)
    emisiones_kg = rastreador.stop()
    emisiones_g = 0
    emisiones_g = emisiones_kg * 1000  # Convertir a gramos
    return resultado, emisiones_g

def medir_impacto(instancia_busqueda, lista, objetivos, num_pruebas=1):
    suma_emisiones = 0
    start_time = time.time()
    for objetivo in objetivos:
        for _ in range(num_pruebas):
            resultado, emisiones = rastrear_emisiones(instancia_busqueda.buscar, lista, objetivo)
            suma_emisiones += emisiones
    tiempo_ejecucion = time.time() - start_time
    return suma_emisiones, tiempo_ejecucion

lista_datos = [random.randint(1, 100000) for _ in range(100000)]
objetivos = [random.randint(1, 100000) for _ in range(10)]
lista_datos_ordenada = sorted(lista_datos)

instancia_busqueda_lineal = BusquedaLineal()
instancia_busqueda_binaria = BusquedaBinaria()

emisiones_total_lineal, tiempo_total_lineal = medir_impacto(instancia_busqueda_lineal, lista_datos_ordenada, objetivos)
emisiones_total_binaria, tiempo_total_binaria = medir_impacto(instancia_busqueda_binaria, lista_datos_ordenada, objetivos)


tiempo_total = tiempo_total_lineal + tiempo_total_binaria

resultados = pd.DataFrame({
    'Metodo': ['Busqueda Lineal', 'Busqueda Binaria'],
    'CO2eq total emitido (g)': [emisiones_total_lineal, emisiones_total_binaria],
    'Tiempo de ejecucion (s)': [tiempo_total_lineal, tiempo_total_binaria]
})


resultados.to_csv('resultados.csv', index=False)
