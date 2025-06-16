import numpy as np

# Datos para la operación AND
training_inputs = np.array([
    [0, 0],
    [0, 1],
    [1, 0],
    [1, 1]
])
expected = np.array([0, 0, 0, 1])

# Hiperparámetros
learning_rate = 0.3
epochs = 200

# Pesos iniciales: [bias, w1, w2]
weights = np.array([1.0, 1.0, 1.0])

# Proceso de entrenamiento
for epoch in range(1, epochs + 1):
    print(f"=== Época {epoch} ===")
    for i, sample in enumerate(training_inputs):
        # Insertamos el bias (valor constante 1) al inicio de la entrada
        x = np.insert(sample, 0, 1)
        
        # Activación con función escalón
        net_input = np.dot(weights, x)
        output = 1 if net_input >= 0 else 0
        
        # Cálculo del error y ajuste de pesos
        error = expected[i] - output
        weights += learning_rate * error * x
        
        print(
            f"Entrada: {x}, "
            f"Esperado: {expected[i]}, "
            f"Obtenido: {output}, "
            f"Pesos: {weights}"
        )

print("\n¡Entrenamiento completado!")
print("Pesos finales:", weights)

# Fase de prueba
print("\n-- Pruebas finales --")
for sample in training_inputs:
    x = np.insert(sample, 0, 1)
    y = 1 if np.dot(weights, x) >= 0 else 0
    print(f"{sample} -> {y}")
