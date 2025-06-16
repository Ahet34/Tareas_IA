import pandas as pd

# DataFrame de ejemplo
df  = pd.DataFrame({'animal': ['perro', 'gato', 'perro', 'pez', 'gato']})
df1 = pd.DataFrame({'animal': ['perro', 'gato', 'perro', 'pez', 'gato']})

print("Original df:\n", df, "\n")

# Método 1: con pd.factorize (devuelve códigos y etiquetas)
df['animal_encoded'] = pd.factorize(df['animal'])[0]

# Método 2: factorizar directamente en la misma columna
df1['animal'] = pd.factorize(df1['animal'])[0]

print("Resultado df con nueva columna:\n", df, "\n")
print("Resultado df1 sobrescribiendo columna:\n", df1)
