import argparse
import datetime
import sys
import csv

def main():
    parser = argparse.ArgumentParser(description='Procesar y consultar cheques bancarios.')
    parser.add_argument('archivo_csv', help='Nombre del archivo CSV')
    parser.add_argument('dni_cliente', help='DNI del cliente')
    parser.add_argument('--salida', choices=['PANTALLA', 'CSV'], default='PANTALLA', help='Salida de datos')
    parser.add_argument('--tipo_cheque', choices=['EMITIDO', 'DEPOSITADO'], required=True, help='Tipo de cheque')
    parser.add_argument('--estado_cheque', choices=['pendiente', 'aprobado', 'rechazado'], help='Estado del cheque')
    parser.add_argument('--fecha_inicio', help='Fecha de inicio (opcional)')
    parser.add_argument('--fecha_fin', help='Fecha de fin (opcional)')
    
    args = parser.parse_args()
    
    # Leer datos desde el archivo CSV
    notas = []
    try:
        with open(args.archivo_csv, 'r', newline='') as f:
            datos = csv.DictReader(f, delimiter=',')
            for fila in datos:
                notas.append(fila)
    except FileNotFoundError:
        print(f"Error: El archivo '{args.archivo_csv}' no existe.")
        sys.exit(1)
    
    def mostrar_en_columnas(notas):
        if not notas:
            print("No hay datos para mostrar.")
            return

        # Obtener los nombres de las columnas
        nombres_columnas = list(notas[0].keys())

        # Inicializar los anchos de las columnas con el longitud de los nombres de las columnas
        anchos_columnas = {columna: len(columna) for columna in nombres_columnas}

        # Calcular los anchos máximos de las columnas
        for fila in notas:
            for columna, valor in fila.items():
                anchos_columnas[columna] = max(anchos_columnas[columna], len(str(valor)))

        # Asegurarse de que las columnas de fecha tengan un ancho mínimo
        for columna in nombres_columnas:
            if columna in ['FechaOrigen', 'FechaPago']:
                anchos_columnas[columna] = max(anchos_columnas[columna], 19)  # Ancho mínimo para fechas con hora y minutos

        # Imprimir los nombres de las columnas
        for columna in nombres_columnas:
            print('{:{width}}'.format(columna, width=anchos_columnas[columna]), '|', end=' ')
        print('')

    # Imprimir una línea horizontal para separar los nombres de las columnas de los datos
        for columna in nombres_columnas:
            print('-' * anchos_columnas[columna], '|', end=' ')
        print('')

        # Imprimir las filas de datos
        for fila in notas:
            for columna in nombres_columnas:
                valor = fila[columna]
            
                # Verificar si la columna es una fecha y formatearla en el formato deseado
                if columna in ['FechaOrigen', 'FechaPago']:
                    fecha_timestamp = int(valor)
                    fecha_formateada = datetime.datetime.fromtimestamp(fecha_timestamp).strftime('%Y-%m-%d %H:%M:%S')
                    valor = fecha_formateada
            
                print('{:{width}}'.format(valor, width=anchos_columnas[columna]), '|', end=' ')
            print('')

    # Validación de DNI
    if not args.dni_cliente.isdigit() or len(args.dni_cliente) != 8:
        print("Error: El DNI del cliente debe ser un número de 8 dígitos.")
        sys.exit(1)
    # Filtrar por DNI del cliente
    if not any(fila['DNI'] == args.dni_cliente for fila in notas):
        print("El DNI no está en la base de datos.")
        return sys.exit(1)

    #VERIFICAR CHEQUES REPETIDOS PARA UN MISMO DNI
    numeros_cheque_cuenta = {}  
    for fila in notas:
        numero_cheque = fila['NroCheque']
        cuenta = fila['NumeroCuentaOrigen'] if args.tipo_cheque == 'EMITIDO' else fila['NumeroCuentaDestino']
        if cuenta not in numeros_cheque_cuenta:
            numeros_cheque_cuenta[cuenta] = set()
        if numero_cheque in numeros_cheque_cuenta[cuenta]:
            print(f"Error: Número de cheque repetido ({numero_cheque}) en la cuenta {cuenta} para el DNI {args.dni_cliente}.")
            sys.exit(1)
        numeros_cheque_cuenta[cuenta].add(numero_cheque) 

    # Validación de Tipo de Cheque
    if args.tipo_cheque not in ['EMITIDO', 'DEPOSITADO']:
        print("Error: El tipo de cheque debe ser 'EMITIDO' o 'DEPOSITADO'.")
        sys.exit(1)
    # Filtrar por tipo de cheque (EMITIDO o DEPOSITADO)
    if args.tipo_cheque == 'EMITIDO':
        notas = [fila for fila in notas if fila['NumeroCuentaOrigen'] == args.dni_cliente]
    else:
        notas = [fila for fila in notas if fila['NumeroCuentaDestino'] == args.dni_cliente]


    # FILTRAR Y VALIDAR 
    if args.estado_cheque:
        if args.estado_cheque not in ['pendiente', 'aprobado', 'rechazado']:
            print("Error: El estado del cheque debe ser 'pendiente', 'aprobado' o 'rechazado'.")
            sys.exit(1)
        else: notas = [fila for fila in notas if fila['Estado'] == args.estado_cheque]


    # Filtrar por rango de fechas (opcional)
    if args.fecha_inicio and args.fecha_fin:
        notas = [fila for fila in notas if fila['FechaOrigen'] >= args.fecha_inicio and fila['FechaPago'] >= args.fecha_fin]           


    # Mostrar o exportar resultados
    if args.salida == 'CSV':
        nombre_archivo = f"{args.dni_cliente}_{datetime.datetime.now().strftime('%Y-%m-%d')}.csv"
        with open(f'{nombre_archivo}', 'w', newline='') as f:
            writer = csv.DictWriter(f, fieldnames=notas[0].keys(), delimiter=',')
            writer.writeheader()
            for fila in notas:
                # Convierto el valor de la fecha en un objeto datetime
                fecha_origen = datetime.datetime.fromtimestamp(int(fila['FechaOrigen']))
                fecha_pago = datetime.datetime.fromtimestamp(int(fila['FechaPago']))

                # Escribo en el csv el objeto datetime de la forma AÑO-MES-DIA HORA-MINUTOS
                fila['FechaOrigen'] = fecha_origen.strftime('%Y-%m-%d %H:%M:%S')
                fila['FechaPago'] = fecha_pago.strftime('%Y-%m-%d %H:%M:%S')

                writer.writerow(fila)
                
        print(f"Se ha guardado el archivo {nombre_archivo}")

    else:
        print(mostrar_en_columnas(notas))

if __name__ == "__main__":
    main()



#COMO EJECUTAR:
#python listado_cheques.py listado_cheques.csv 12345678 --salida CSV --tipo_cheque EMITIDO --estado_cheque aprobado
