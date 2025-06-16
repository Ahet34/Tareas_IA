import tkinter as tk
from tkinter import messagebox
from juego import TresEnRaya  # Clase del juego
from RedNeuronalManual import RedNeuronalManual  # Clase de la red neuronal
import os

class Interfaz3EnRaya:
    def __init__(self, raiz, juego, red_neuronal):
        self.jugadas_ia = []  # Almacena las jugadas de la IA durante la partida
        self.raiz = raiz
        self.juego = juego
        self.red_neuronal = red_neuronal
        self.turno_humano = True  # Comienza el jugador humano
        self.botones = []  # Lista de botones del tablero

        # Crear el tablero gráfico (3x3 botones)
        for fila in range(3):
            fila_botones = []
            for col in range(3):
                boton = tk.Button(
                    raiz, text="", font=("Arial", 24), width=5, height=2,
                    command=lambda f=fila, c=col: self.jugar_turno(f, c)
                )
                boton.grid(row=fila, column=col)
                fila_botones.append(boton)
            self.botones.append(fila_botones)

        # Etiqueta para mostrar mensajes
        self.etiqueta_mensaje = tk.Label(raiz, text="Tu turno (Jugador Humano - X)", font=("Arial", 14))
        self.etiqueta_mensaje.grid(row=3, column=0, columnspan=3)

    def jugar_turno(self, fila, col):
        """
        Maneja el turno actual (humano o IA) basado en la celda seleccionada.
        """
        posicion = fila * 3 + col
        if self.juego.tablero[posicion] != 0:
            messagebox.showwarning("Movimiento inválido", "Esa posición ya está ocupada. Intenta de nuevo.")
            return

        # Turno del humano
        if self.turno_humano:
            self.juego.realizar_movimiento(posicion, 1)
            self.actualizar_tablero()
            resultado = self.juego.comprobar_victoria()
            if self.manejar_resultado(resultado):
                return
            self.turno_humano = False
            self.etiqueta_mensaje.config(text="Turno de la IA (O)")
            self.raiz.after(500, self.turno_ia)  # Esperar 500 ms antes de que juegue la IA

    def turno_ia(self):
        """
        Turno de la IA: Calcula y realiza su movimiento.
        """
        # 1. Detectar si puede ganar
        movimiento_ia = self.juego.detectar_jugada_critica(-1)
        if movimiento_ia is not None:
            self.juego.realizar_movimiento(movimiento_ia, -1)
            self.actualizar_tablero()
            resultado = self.juego.verificar_ganador()
            if self.manejar_resultado(resultado):
                return
            self.turno_humano = True
            self.etiqueta_mensaje.config(text="Tu turno (Jugador Humano - X)")
            return

        # 2. Detectar si necesita bloquear al humano
        movimiento_bloqueo = self.juego.detectar_jugada_critica(1)
        if movimiento_bloqueo is not None:
            self.juego.realizar_movimiento(movimiento_bloqueo, -1)
            self.actualizar_tablero()
            resultado = self.juego.verificar_ganador()
            if self.manejar_resultado(resultado):
                return
            self.turno_humano = True
            self.etiqueta_mensaje.config(text="Tu turno (Jugador Humano - X)")
            return

        # 3. Usar la red neuronal para decidir
        tablero_normalizado = [x / 1.0 for x in self.juego.tablero]
        predicciones = self.red_neuronal.adelante(tablero_normalizado)
        movimiento_ia = max(
            [(indice, valor) for indice, valor in enumerate(predicciones) if self.juego.tablero[indice] == 0],
            key=lambda x: x[1]
        )[0]
        self.juego.realizar_movimiento(movimiento_ia, -1)
        self.actualizar_tablero()

        resultado = self.juego.verificar_ganador()
        if self.manejar_resultado(resultado):
            return

        self.turno_humano = True
        self.etiqueta_mensaje.config(text="Tu turno (Jugador Humano - X)")

        # Código existente para el turno de la IA
        self.jugadas_ia.append((self.juego.tablero[:], movimiento_ia))
        self.actualizar_tablero()
        if self.juego.verificar_ganador():
            self.finalizar_partida(self.juego.verificar_ganador())

    def actualizar_tablero(self):
        """
        Actualiza los botones gráficos para reflejar el estado actual del tablero.
        """
        simbolos = {0: "", 1: "X", -1: "O"}
        for fila in range(3):
            for col in range(3):
                posicion = fila * 3 + col
                self.botones[fila][col].config(text=simbolos[self.juego.tablero[posicion]])

        # Mostrar el tablero en consola
        self.mostrar_tablero_consola()

    def mostrar_tablero_consola(self):
        """
        Muestra el estado actual del tablero en la consola.
        """
        simbolos = {0: ".", 1: "X", -1: "O"}
        print("Tablero actual:")
        for i in range(3):
            print(" | ".join([simbolos[self.juego.tablero[i * 3 + j]] for j in range(3)]))
            if i < 2:
                print("---------")
        print()  # Línea vacía

    def manejar_resultado(self, resultado):
        """
        Maneja el resultado del juego (victoria, empate o continuar).
        """
        if resultado == 1:
            messagebox.showinfo("¡Ganaste!", "¡Felicidades, has ganado!")
            self.reiniciar_juego()
            return True
        elif resultado == -1:
            messagebox.showinfo("Derrota", "La IA ha ganado. Mejor suerte la próxima vez.")
            self.reiniciar_juego()
            return True
        elif resultado == 2:
            messagebox.showinfo("Empate", "Es un empate.")
            self.reiniciar_juego()
            return True
        return False

    def reiniciar_juego(self):
        """
        Reinicia el tablero y el turno para comenzar una nueva partida.
        """
        self.juego = TresEnRaya()
        self.turno_humano = True
        self.etiqueta_mensaje.config(text="Tu turno (Jugador Humano - X)")
        self.actualizar_tablero()

    def finalizar_partida(self, ganador):
        if ganador == 1:
            print("¡La IA ganó!")

        elif ganador == -1:
            print("¡Tú ganaste!")
            
        else:
            print("¡Empate!")


        
        self.reiniciar_juego()  # Reinicia el juego para una nueva partida


# Ejecución del juego con la interfaz gráfica
if __name__ == "__main__":
    from tkinter import Tk

    # Crear las instancias necesarias
    juego = TresEnRaya()
    red_neuronal = RedNeuronalManual()
    
    # Entrenamiento inicial de la red neuronal
    print("Entrenando la red neuronal...")
    datos_entrenamiento = [
    # Jugada inicial, IA juega en el centro
    ([0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 1, 0, 0, 0, 0]), 
    
    ([0, 0, 0, 0, 1, 0, 0, 0, 0], [1, 0, 0, 0, 0, 0, 0, 0, 0]), ]

    #Entrenamiento
    red_neuronal.entrenar(datos_entrenamiento, tasa_aprendizaje=0.1, epocas=1000)
    salida = red_neuronal.adelante([0, 0, 0, 0, 1, 0, 0, 0, 0])
    
    #Ejemplo de salida
    salida_formateada = "\n".join(str(x) for x in salida)
    print("Salida para [0, 0, 0, 0, 1, 0, 0, 0, 0]:")
    print(salida_formateada)
    print("Entrenamiento completado.")
    
    #Juego
    raiz = Tk()
    raiz.title("3 en Raya - Gráfico y Comandos")
    # Iniciar la interfaz gráfica
    interfaz = Interfaz3EnRaya(raiz, juego, red_neuronal)
    raiz.mainloop()
