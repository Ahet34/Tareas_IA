import numpy as np
from sklearn.datasets import load_iris

def dividir_datos(X, y, frac_train=0.8, frac_val=0.1):
    """Baraja y separa en conjuntos de entrenamiento, validación y prueba."""
    n_total = X.shape[0]
    idx = np.arange(n_total)
    np.random.shuffle(idx)

    n_train = int(frac_train * n_total)
    n_val = int(frac_val * n_total)
    # El resto será test
    train_idx = idx[:n_train]
    val_idx = idx[n_train:n_train + n_val]
    test_idx = idx[n_train + n_val:]

    return (
        X[train_idx], y[train_idx],
        X[val_idx], y[val_idx],
        X[test_idx], y[test_idx]
    )

def mostrar_muestra(nombre, datos):
    """Imprime las primeras cinco filas o valores."""
    print(f"{nombre}:")
    print(datos[:5])
    print()  # línea en blanco

def main():
    # Cargamos Iris
    iris = load_iris()
    X, y = iris.data, iris.target

    # Cuántas iteraciones dejar al usuario decidir
    n_iter = int(input("¿Cuántas iteraciones quieres ejecutar? "))

    for i in range(1, n_iter + 1):
        print(f"\n\n--- Iteración #{i} ---\n")
        
        # Dividir el dataset
        X_train, y_train, X_val, y_val, X_test, y_test = dividir_datos(X, y)

        # Mostrar un pequeño vistazo de cada partición
        mostrar_muestra("Entrenamiento (X_train)", X_train)
        mostrar_muestra("Entrenamiento (y_train)", y_train)

        mostrar_muestra("Validación (X_validation)", X_val)
        mostrar_muestra("Validación (y_validation)", y_val)

        mostrar_muestra("Prueba (X_test)", X_test)
        mostrar_muestra("Prueba (y_test)", y_test)

if __name__ == "__main__":
    main()
