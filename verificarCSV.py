import pandas as pd

# Cargar el archivo CSV en un DataFrame
df = pd.read_csv('primerTest.csv')

# Verificar valores faltantes en cada columna
missing_values = df.isnull().sum()

# Verificar qué filas tienen valores nulos
filas_con_valores_nulos = df[df.isna().any(axis=1)]

# Verificar valores duplicados en todo el DataFrame
duplicates = df.duplicated().sum()

# Identifica filas duplicadas
duplicados = df[df.duplicated()]

# Verificar tipos de datos de las columnas
data_types = df.dtypes

# Verifica si hay filas duplicadas
if duplicados.empty:
    print("No se encontraron filas duplicadas.")
else:
    print("Filas duplicadas encontradas:")
    print(duplicados)

# Opcionalmente, cuenta la cantidad de filas duplicadas
cantidad_duplicados = len(duplicados)
print(f"Total de filas duplicadas: {cantidad_duplicados}")

# Otras verificaciones específicas según tus necesidades
# Por ejemplo, verificar rangos de valores, valores únicos, etc.

# Mostrar los resultados
print("Valores faltantes por columna:")
print(missing_values)

print("\nValores duplicados:")
print(duplicates)

print("\nTipos de datos por columna:")
print(data_types)



# Mostrar las filas con valores nulos
print("Filas con valores nulos:")
print(filas_con_valores_nulos)
print(type(filas_con_valores_nulos))

#Nota se encontro un valor vacio en dentro de la fila 2811 , no hay nombre , que deberia de hacer? 


#Nunca firmes un aval
