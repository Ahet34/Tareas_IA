import math
import random

# **Función de activación: Sigmoide**
def sigmoide(x):
    return 1 / (1 + math.exp(-x))

# **Derivada de la función sigmoide**
def derivada_sigmoide(x):
    return sigmoide(x) * (1 - sigmoide(x))

# **Clase de la red neuronal con RNN**
class RedNeuronalManual:
    def __init__(self):
        """
        Red neuronal recurrente manual para 3 en raya:
        - 9 neuronas de entrada (tablero).
        - 8 neuronas en la capa oculta.
        - 9 neuronas de salida.
        """
        # Pesos y sesgos entre capa de entrada y capa oculta
        self.pesos_entrada_oculta = [
            [random.uniform(-1, 1) for _ in range(9)],  # Para la 1ª neurona oculta
            [random.uniform(-1, 1) for _ in range(9)],  # Para la 2ª neurona oculta
            [random.uniform(-1, 1) for _ in range(9)],  # Para la 3ª neurona oculta
            [random.uniform(-1, 1) for _ in range(9)],  # Para la 4ª neurona oculta
            [random.uniform(-1, 1) for _ in range(9)],  # Para la 5ª neurona oculta
            [random.uniform(-1, 1) for _ in range(9)],  # Para la 6ª neurona oculta
            [random.uniform(-1, 1) for _ in range(9)],  # Para la 7ª neurona oculta
            [random.uniform(-1, 1) for _ in range(9)],  # Para la 8ª neurona oculta
        ]
        self.sesgo_oculto = [random.uniform(-1, 1) for _ in range(8)]

        # Pesos y sesgos entre capa oculta y capa de salida
        self.pesos_oculta_salida = [
            [random.uniform(-1, 1) for _ in range(8)],  # Para la 1ª neurona de salida
            [random.uniform(-1, 1) for _ in range(8)],  # Para la 2ª neurona de salida
            [random.uniform(-1, 1) for _ in range(8)],  # Para la 3ª neurona de salida
            [random.uniform(-1, 1) for _ in range(8)],  # Para la 4ª neurona de salida
            [random.uniform(-1, 1) for _ in range(8)],  # Para la 5ª neurona de salida
            [random.uniform(-1, 1) for _ in range(8)],  # Para la 6ª neurona de salida
            [random.uniform(-1, 1) for _ in range(8)],  # Para la 7ª neurona de salida
            [random.uniform(-1, 1) for _ in range(8)],  # Para la 8ª neurona de salida
            [random.uniform(-1, 1) for _ in range(8)],  # Para la 9ª neurona de salida
        ]
        self.sesgo_salida = [random.uniform(-1, 1) for _ in range(9)]

        # Estado oculto inicial (memoria de la red)
        self.estado_oculto = [0] * 8

    # **Propagación hacia adelante con RNN**
    def adelante(self, entradas):
        """
        Calcula las salidas de la red, tomando en cuenta la memoria recurrente.
        """
        # 1. Calcular la salida de la capa oculta (incluyendo memoria)
        self.salida_oculta = []
        for i in range(8):
            # Calcular suma ponderada: z = w1*x1 + w2*x2 + ... + w9*x9 + b
            z_oculta = sum(self.pesos_entrada_oculta[i][j] * entradas[j] for j in range(9)) + self.sesgo_oculto[i]
            self.salida_oculta.append(sigmoide(z_oculta)) # Aplicar la función de activación

        # 2. Calcular la salida de la capa de salida
        self.salidas = []
        for i in range(9):
            # Calcular suma ponderada: z = w1*h1 + w2*h2 + ... + w8*h8 + b
            z_salida = sum(self.pesos_oculta_salida[i][j] * self.salida_oculta[j] for j in range(8)) + self.sesgo_salida[i]
            self.salidas.append(sigmoide(z_salida)) # Aplicar la función de activación


        return self.salidas

    # **Entrenamiento (Retropropagación) con RNN**
    def retropropagar(self, entradas, salidas_esperadas, tasa_aprendizaje):
        """
        Ajusta los pesos y sesgos para reducir el error utilizando el algoritmo de retropropagación.
        """
        # 1. Calcular errores en la capa de salida
        errores_salida = [salida_esperada - salida for salida_esperada, salida in zip(salidas_esperadas, self.salidas)]
        gradientes_salida = [error * derivada_sigmoide(salida) for error, salida in zip(errores_salida, self.salidas)]

        # 2. Ajustar pesos y sesgos entre capa oculta y capa de salida
        for i in range(9):  # Para cada neurona de salida
            for j in range(8):  # Para cada conexión desde la capa oculta
                self.pesos_oculta_salida[i][j] += tasa_aprendizaje * gradientes_salida[i] * self.salida_oculta[j]
            self.sesgo_salida[i] += tasa_aprendizaje * gradientes_salida[i]

        # 3. Calcular errores en la capa oculta (incluso considerando memoria)
        errores_ocultas = [0] * 8
        for j in range(8):
            errores_ocultas[j] = sum(gradientes_salida[i] * self.pesos_oculta_salida[i][j] for i in range(9))
        gradientes_ocultos = [error * derivada_sigmoide(salida_oculta) for error, salida_oculta in zip(errores_ocultas, self.salida_oculta)]

        # 4. Ajustar pesos y sesgos entre capa de entrada y capa oculta
        for i in range(8):  # Para cada neurona oculta
            for j in range(9):  # Para cada conexión desde la capa de entrada
                self.pesos_entrada_oculta[i][j] += tasa_aprendizaje * gradientes_ocultos[i] * entradas[j]
            self.sesgo_oculto[i] += tasa_aprendizaje * gradientes_ocultos[i]


    # **Entrenamiento completo 
    def entrenar(self, datos_entrenamiento, tasa_aprendizaje, epocas):
        for epoca in range(epocas):
            error_total = 0
            for entradas, salidas_esperadas in datos_entrenamiento:
                self.adelante(entradas)  # Propagación hacia adelante
                self.retropropagar(entradas, salidas_esperadas, tasa_aprendizaje)  # Retropropagación
                error_total += sum((salida_esperada - salida) ** 2 for salida_esperada, salida in zip(salidas_esperadas, self.salidas))
            print(f"Época {epoca + 1}/{epocas}, Error Total: {error_total:.20f}")

# **Prueba de la red neuronal**
if __name__ == "__main__":
    red = RedNeuronalManual()
    # Datos de entrenamiento: Tableros y movimientos esperados
    #datos_entrenamiento = [ ] 
    
    #red.entrenar(datos_entrenamiento, tasa_aprendizaje=0.01, epocas=2000)
    
    # Prueba con un caso no entrenado
    #salida = red.adelante([1, 0, 1, 0, 0, 0, 1, 0, 0])
    
    #print("Salida para [1, 1, 0, 0, 0, 0, 0, 0, 0]:", salida)