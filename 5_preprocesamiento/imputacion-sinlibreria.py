import pandas as pd
import numpy as np

# Creamos el DataFrame con valores faltantes
df = pd.DataFrame({'edad': [25, np.nan, 30, 22, np.nan, 28]})
print("Original:\n", df)

# Extraemos sólo los números válidos y calculamos la media a mano
valores_validos = [x for x in df['edad'] if not pd.isna(x)]
suma = sum(valores_validos)
cuenta = len(valores_validos)
promedio = suma / cuenta
print(f"\nMedia manual calculada: {promedio}")

# Rellenamos los NaN usando comprensión de listas
edades_completas = [
    promedio if pd.isna(x) else x
    for x in df['edad']
]

# Sustituimos la columna original por la lista completada
df['edad'] = edades_completas

print("\nDataFrame tras imputación manual:")
print(df)
