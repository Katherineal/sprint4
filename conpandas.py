import csv
import sys

# Leer datos desde el archivo CSV
notas = []
with open('listado_cheques.csv', 'r', newline='') as f:
    datos = csv.DictReader(f, delimiter=',')
    for fila in datos:
        notas.append(fila)

# Funcion para mostrar el csv
def mostrar_en_columnas(data):
    if not data:
        print("No hay datos para mostrar.")
        return
    
    # Obtener los nombres de las columnas
    nombres_columnas = data[0]

    # Inicializar los anchos de las columnas con la longitud de los nombres de las columnas
    anchos_columnas = {columna: len(columna) for columna in nombres_columnas}

    # Calcular los anchos máximos de las columnas
    for fila in data:
        for columna, valor in fila.items():
            anchos_columnas[columna] = max(anchos_columnas[columna], len(str(valor)))

    # Imprimir los nombres de las columnas
    for columna in nombres_columnas:
        print('{:{width}}'.format(columna, width=anchos_columnas[columna]), '|', end=' ')
    print('')

    # Imprimir una línea horizontal para separar los nombres de las columnas de los datos
    for columna in nombres_columnas:
        print('-' * anchos_columnas[columna], '|', end=' ')
    print('')

    # Imprimir las filas de datos
    for fila in data:
        for columna, valor in fila.items():
            print('{:{width}}'.format(valor, width=anchos_columnas[columna]), '|', end=' ')
        print('')

# Filtrar cheques por estado
def filtrar_por_estado(data, estado_filtrar=None):
    if estado_filtrar is not None:
        resultados_filtrados = [fila for fila in data if fila['Estado'] == estado_filtrar]
        if resultados_filtrados:
            mostrar_en_columnas(resultados_filtrados)
        else:
            mostrar_en_columnas(data)
    else:
        mostrar_en_columnas(data)

# Filtrar cheques por DNI
def segunDni(dni, data):
    cliente = [fila for fila in data if fila['DNI'] == dni]
    if cliente:
        return cliente
    else:
        return "El DNI no está en la base de datos."

# Funcion ver cheques en consola o csv
def salidaUsuario():
    while True:
        eleccion = input("Elige si quieres ver los cheques en un csv o en la consola: ").lower()
        if eleccion == 'csv':
            with open('listado_cheques_filtrado.csv', 'w', newline='') as f:
                writer = csv.DictWriter(f, fieldnames=notas[0].keys(), delimiter=';')
                writer.writeheader()
                writer.writerows(notas)
            print("Se ha guardado el archivo 'listado_cheques_filtrado.csv'.")
            break   
        elif eleccion == 'consola':
            mostrar_en_columnas(notas)
            break  
        else:
            print("Opción no válida. Por favor, selecciona 'csv' o 'consola'.")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Uso: python script.py <DNI>")
        sys.exit(1)

    elegirDni = sys.argv[1]
    resultados = segunDni(elegirDni, notas)

    if resultados == "El DNI no está en la base de datos.":
        print(resultados)
    else:
        mostrar_en_columnas(resultados)
        
        # Preguntar por el estado de los cheques a mostrar
        estado_filtrar = input("¿Qué tipo de cheques desea ver (APROBADO, RECHAZADO, PENDIENTE)? ").upper()

        while estado_filtrar not in ['APROBADO', 'RECHAZADO', 'PENDIENTE']:
            print("Estado no válido. Por favor, seleccione APROBADO, RECHAZADO o PENDIENTE.")
            estado_filtrar = input("¿Qué tipo de cheques desea ver (APROBADO, RECHAZADO, PENDIENTE)? ").upper()
            
        if estado_filtrar in ['APROBADO', 'RECHAZADO', 'PENDIENTE']:
            notas_filtradas = filtrar_por_estado(resultados, estado_filtrar)
            salidaUsuario()  # Llama a la función para que el usuario elija la salida
