import pandas as pd

df = pd.read_csv('listado_cheques.csv', encoding='latin-1', delimiter=',')

df
# def mostrar_en_columnas(df):
#     column_names = df.columns.tolist()

#     # Máxima longitud de caracteres en cada columna
#     column_widths = [max(df[column].astype(str).apply(len)) for column in column_names]

#     for i in range(len(column_names)):
#         print('{:{}}'.format(column_names[i], column_widths[i]), '|', end=' ')
#     print('')

#     # Imprime una línea horizontal que separa los nombres de los datos
#     for width in column_widths:
#         print('-' * width, '|', end=' ')
#     print('')

#     # Imprime los datos separados por '|'
#     for index, row in df.iterrows():
#         for i in range(len(column_names)):
#             print(f"{row[column_names[i]]:<{column_widths[i]}} |", end=' ')
#         print('')

def segunDni(dni):
    booleanito = df['DNI'] == dni
    if booleanito.any():
        registros = [df.loc[df['DNI'] ==  dni]]
        return registros
    else:
        return "El DNI no esta en la base de datos."
print(segunDni(111))

def salidaUsuario():
    eleccion = input("Elige si quieres ver los registros en un csv o en la consola: ")
    if eleccion == 'csv':
        df.to_csv('D:/Users/Admin/Downloads/listado_cheques_filtrado.csv', encoding='latin-1', delimiter=',')
    elif eleccion == 'consola':
        mostrar_en_columnas(df)
    else: pass

def estadoCheque():
    tipo = input("Ingrese si quiere ver los cheques en estado PENDIENTE, APROBADO o RECHAZADO: ")
    if tipo.upper() == 'PENDIENTE':
        registros = df.loc[df['Estado'] ==  tipo.lower()]
        return registros
    elif tipo.upper == 'APROBADO':
        registros = df.loc[df['Estado'] ==  tipo.lower]
        return registros
    elif tipo.upper == 'RECHAZADO':
        registros = df.loc[df['Estado'] ==  tipo.lower]
        return registros
print(estadoCheque())
# mostrar_en_columnas(df)