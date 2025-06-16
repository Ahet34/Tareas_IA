import pandas as pd
from sklearn.preprocessing import LabelBinarizer

# Creamos el DataFrame de ejemplo
df = pd.DataFrame({'color': ['rojo', 'azul', 'rojo', 'azul', 'rojo']})
print("Antes de codificar:\n", df, "\n")

# Instanciamos el binarizador
lb = LabelBinarizer()

# Ajustamos y transformamos en un solo paso
array_cod = lb.fit_transform(df['color'])

# LabelBinarizer devuelve un array 1D si hay sólo 2 clases, 
# o 2D con tantas columnas como clases si hay más de dos.
if array_cod.ndim == 1:
    array_cod = array_cod.reshape(-1, 1)

# Generamos nombres de columna según el número de columnas resultante
if array_cod.shape[1] == 1:
    col_names = ['color_binario']
else:
    col_names = [f"color_{cat}" for cat in lb.classes_]

# Construimos el DataFrame de ceros y unos y lo concatenamos
df_ohe = pd.DataFrame(array_cod, columns=col_names)
df_final = pd.concat([df, df_ohe], axis=1)

print("Después de codificar:\n", df_final)
