import csv
import pandas as pd

notes=''
with open('listado_cheques.csv',newline='') as f:
    data=csv.reader(f,delimiter=',')
    notes=list(data)

df = pd.read_csv('listado_cheques.csv', index_col='NroCheque' , delimiter=',')

def motrar_en_columnas(notes):

    #Nombres de las columnas
    column_names=notes[0]

    #Maxima cantidad de filas segun datos 
    column_widths = [max(len(str(row[i])) for row in notes) for i in range(len(column_names))]
    
    #Imprime los campos en cada columna
    for i in range(len(column_names)):
        print('{:{}}'.format(column_names[i],column_widths[i]),'|',end=' ')
    print('')

    #Imprime una linea horizontal que permite separar los nombres de datos
    for width in column_widths:
        print('-'*width,'|', end=' ')
    print('')

    #Imprime los datos separandolos con un '|'
    for i in range(1,len(notes)):
        for j in range(len(column_names)):
            print(f"{notes[i][j]:<{column_widths[j]}} |", end=' ')
        print('')

def salidaUsuario():
    eleccion = input("Elige si quieres ver los registros en un csv o en la consola: ")
    if eleccion == 'csv':
        df.to_csv('listado_cheques_filtrado.csv', encoding='latin-1', sep=';')
    elif eleccion == 'consola':
        motrar_en_columnas(notes)
    else: 
        pass
print(salidaUsuario())

def estadoCheque():
    tipo = input("Ingrese si quiere ver los cheques en estado PENDIENTE, APROBADO o RECHAZADO: ")
    if tipo.upper() == 'PENDIENTE':
        registros = df.loc[df['Estado'] ==  tipo.lower()]
        return registros
    elif tipo.upper() == 'APROBADO':
        registros = df.loc[df['Estado'] ==  tipo.lower()]
        return registros
    elif tipo.upper() == 'RECHAZADO':
        registros = df.loc[df['Estado'] ==  tipo.lower()]
        return registros
print(estadoCheque())

def segunDni(dni):
    booleanito = df['DNI'] == dni
    if booleanito.any():
        registros = [df.loc[df['DNI'] ==  dni]]
        return registros
    else:
        return "El DNI no esta en la base de datos."
elegirDni=int(input("Filtrar segun DNI:"))
print(segunDni(elegirDni))

# def entreFechas():
#     fecha_inicio_str = input("Ingrese la fecha de inicio en formato 'YYYY-MM-DD':")
#     fecha_fin_str = input("Ingrese la fecha de fin en formato 'YYYY-MM-DD':")

#     registros_en_rango = None  # Declarar la variable antes del bloque try

#     try:
#         fecha_inicio = pd.to_datetime(fecha_inicio_str, format='%Y-%m-%d')
#         fecha_fin = pd.to_datetime(fecha_fin_str, format='%Y-%m-%d')

#         # Asegúrate de que las columnas de fecha sean de tipo Timestamp
#         df['FechaOrigen'] = pd.to_datetime(df['FechaOrigen'], format='%Y-%m-%d')
#         df['FechaPago'] = pd.to_datetime(df['FechaPago'], format='%Y-%m-%d')

#         registros_en_rango = df[(df['FechaOrigen'] >= fecha_inicio) & (df['FechaOrigen'] <= fecha_fin)]

#         if registros_en_rango is not None:
#             print("Registros dentro del rango de fechas:")
#             print(registros_en_rango)
#     except ValueError:
#         print("Formato de fecha incorrecto. Use 'YYYY-MM-DD'.")

# # Llama a la función entreFechas
# entreFechas()



def verificarChequeRepetido():
    dni = input("Ingrese el número de DNI: ")
    numero_cheque = input("Ingrese el número de cheque: ")

    resultados = df[(df['DNI'] == dni) & (df['NumeroCheque'] == numero_cheque)]

    if len(resultados) > 1:
        print("¡Error! Se encontraron cheques repetidos en la misma cuenta para el DNI proporcionado.")
    else:
        print("No se encontraron cheques repetidos en la misma cuenta para el DNI proporcionado.")

verificarChequeRepetido() 


