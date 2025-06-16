import pandas as pd
from sklearn.preprocessing import OneHotEncoder

# Montamos un DataFrame de ejemplo
df = pd.DataFrame({
    'animal': ['perro', 'gato', 'perro', 'pez', 'gato']
})
print("DataFrame original:")
print(df)

# Configuramos el codificador para que devuelva un array denso
ohe = OneHotEncoder(sparse_output=False)

# En un solo paso aprendemos y transformamos la columna 'animal'
matriz_ohe = ohe.fit_transform(df[['animal']])

# Recuperamos los nombres de las nuevas columnas
nuevas_cols = ohe.get_feature_names_out(['animal'])

# Creamos el DataFrame con los ceros y unos
df_ohe = pd.DataFrame(matriz_ohe, columns=nuevas_cols)

# Concatenamos con el original
df_final = pd.concat([df, df_ohe], axis=1)

print("\nDataFrame tras One-Hot Encoding:")
print(df_final)
