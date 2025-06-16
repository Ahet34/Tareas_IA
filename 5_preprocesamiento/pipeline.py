import pandas as pd
import numpy as np
from sklearn.pipeline import Pipeline
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import OrdinalEncoder
from sklearn.compose import ColumnTransformer

# Datos de ejemplo con nuevos nombres “quemados”
df = pd.DataFrame({
    'nombre': ['sofía', 'mateo', 'valentina', 'diego', 'isabela'],
    'edad':   [27,       np.nan, 31,          24,      np.nan],
    'genero': ['f',      'm',    'f',         'm',     'f']
})

print("Datos originales:")
print(df)

# ¿Qué columnas procesar?
num_cols = ['edad']
cat_cols = ['genero']

# Pipeline para valores numéricos: imputar media
num_pipe = Pipeline([
    ('imputer', SimpleImputer(strategy='mean'))
])

# Pipeline para categóricos: encoder ordinal
cat_pipe = Pipeline([
    ('encoder', OrdinalEncoder())
])

# Unir ambos pipelines
preprocessor = ColumnTransformer([
    ('nums', num_pipe, num_cols),
    ('cats', cat_pipe, cat_cols)
])

# Aplicar todo de una vez
transformed = preprocessor.fit_transform(df)

# Reconstruir DataFrame con etiquetas claras
df_proc = pd.DataFrame(
    transformed,
    columns=['edad_imputada', 'genero_codificado']
)

# Juntar con la columna de nombres original
df_final = pd.concat([df[['nombre']], df_proc], axis=1)

print("\nDatos tras el pipeline:")
print(df_final)
