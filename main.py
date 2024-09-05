import logging
import random
import pandas as pd
from codecarbon import EmissionsTracker
from busqueda_lineal import BusquedaLineal
from busqueda_binaria import BusquedaBinaria

def rastrear_emisiones(func, *args, **kwargs):
    rastreador = EmissionsTracker()
    rastreador.start()
    resultado = func(*args, **kwargs)
    emisiones = rastreador.stop()
    return resultado, emisiones

def medir_impacto(instancia_busqueda, lista, objetivos, num_pruebas=1):
    suma_emisiones = 0
    for objetivo in objetivos:
        for _ in range(num_pruebas):
            resultado, emisiones = rastrear_emisiones(instancia_busqueda.buscar, lista, objetivo)
            suma_emisiones += emisiones
    return suma_emisiones

lista_datos = [random.randint(1, 100000) for _ in range(100000)]
objetivos = [random.randint(1, 100000) for _ in range(20)]
lista_datos_ordenada = sorted(lista_datos)

instancia_busqueda_lineal = BusquedaLineal()
instancia_busqueda_binaria = BusquedaBinaria()

emisiones_total_lineal = medir_impacto(instancia_busqueda_lineal, lista_datos_ordenada, objetivos)
emisiones_total_binaria = medir_impacto(instancia_busqueda_binaria, lista_datos_ordenada, objetivos)

# Crear DataFrame con los resultados actuales
resultados = pd.DataFrame({
    'Metodo': ['Busqueda Lineal', 'Busqueda Binaria'],
    'CO2eq total emitido (kg)': [emisiones_total_lineal, emisiones_total_binaria]
})

# Leer el archivo CSV existente si está presente
try:
    resultados_existentes = pd.read_csv('emisiones_resultados.csv')
    numero_ejecuciones = resultados_existentes['Numero de ejecucion'].max() + 1
except FileNotFoundError:
    resultados_existentes = pd.DataFrame(columns=['Numero de ejecucion', 'Méetodo', 'CO2eq total emitido (kg)'])
    numero_ejecuciones = 1

# Agregar el número de ejecución y concatenar los resultados
resultados['Numero de ejecucion'] = numero_ejecuciones
resultados = pd.concat([resultados_existentes, resultados], ignore_index=True)

# Reordenar columnas
resultados = resultados[['Numero de ejecucion', 'Metodo', 'CO2eq total emitido (kg)']]

# Guardar el DataFrame actualizado en el archivo CSV
resultados.to_csv('emisiones_resultados.csv', index=False, sep=',')

print("\nLos resultados han sido exportados a 'emisiones_resultados.csv'.")
