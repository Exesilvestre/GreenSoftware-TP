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
    lista_emisiones = []
    for objetivo in objetivos:
        for _ in range(num_pruebas):
            resultado, emisiones = rastrear_emisiones(instancia_busqueda.buscar, lista, objetivo)
            lista_emisiones.append(emisiones)
    emisiones_promedio = sum(lista_emisiones) / len(lista_emisiones)
    return emisiones_promedio

lista_datos = [random.randint(1, 10000) for _ in range(10000)]
objetivos = [5000, 2500, 7500, 6000, 8900, 1890, 4585, 7853, 6900, 9300, 4800, 2900, 6905, 8500, 9200, 8550 ]
lista_datos_ordenada = sorted(lista_datos)

instancia_busqueda_lineal = BusquedaLineal()
instancia_busqueda_binaria = BusquedaBinaria()

emisiones_promedio_lineal = medir_impacto(instancia_busqueda_lineal, lista_datos, objetivos)
emisiones_promedio_binaria = medir_impacto(instancia_busqueda_binaria, lista_datos_ordenada, objetivos)

print("Búsqueda Lineal:")
print(f"CO2eq promedio emitido (búsqueda lineal): {emisiones_promedio_lineal} kg")

print("\nBúsqueda Binaria:")
print(f"CO2eq promedio emitido (búsqueda binaria): {emisiones_promedio_binaria} kg")

# Crear DataFrame con los resultados actuales
resultados = pd.DataFrame({
    'Metodo': ['Busqueda Lineal', 'Busqueda Binaria'],
    'CO2eq promedio emitido (kg)': [emisiones_promedio_lineal, emisiones_promedio_binaria]
})

# Leer el archivo CSV existente si está presente
try:
    resultados_existentes = pd.read_csv('emisiones_resultados.csv')
    numero_ejecuciones = resultados_existentes['Numero de ejecucion'].max() + 1
except FileNotFoundError:
    resultados_existentes = pd.DataFrame(columns=['Numero de ejecucion', 'Méetodo', 'CO2eq promedio emitido (kg)'])
    numero_ejecuciones = 1

# Agregar el número de ejecución y concatenar los resultados
resultados['Numero de ejecucion'] = numero_ejecuciones
resultados = pd.concat([resultados_existentes, resultados], ignore_index=True)

# Reordenar columnas
resultados = resultados[['Numero de ejecucion', 'Metodo', 'CO2eq promedio emitido (kg)']]

# Guardar el DataFrame actualizado en el archivo CSV
resultados.to_csv('emisiones_resultados.csv', index=False, sep=',')

print("\nLos resultados han sido exportados a 'emisiones_resultados.csv'.")
