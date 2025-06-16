class TresEnRaya:
    def __init__(self):
        """
        Inicializa un tablero vacío de 3 en raya.
        El tablero es una lista de 9 posiciones:
        - 0: casilla vacía
        - 1: movimiento del jugador humano
        - -1: movimiento de la IA
        """
        self.tablero = [0] * 9

    def realizar_movimiento(self, posicion, jugador):
        """
        Realiza un movimiento en el tablero.
        :param posicion: Índice de la casilla (0-8)
        :param jugador: 1 para humano, -1 para IA
        """
        if self.tablero[posicion] == 0:
            self.tablero[posicion] = jugador

    def comprobar_victoria(self):
        """
        Comprueba si hay un ganador o un empate.
        :return:
          - 1 si gana el jugador humano
          - -1 si gana la IA
          - 2 si hay empate
          - 0 si el juego continúa
        """
        # Combinaciones ganadoras
        combinaciones = [
            [0, 1, 2], [3, 4, 5], [6, 7, 8],  # Filas
            [0, 3, 6], [1, 4, 7], [2, 5, 8],  # Columnas
            [0, 4, 8], [2, 4, 6],             # Diagonales
        ]

        for combinacion in combinaciones:
            valores = [self.tablero[i] for i in combinacion]
            if valores == [1, 1, 1]:
                return 1  # Gana el humano
            elif valores == [-1, -1, -1]:
                return -1  # Gana la IA

        if all(x != 0 for x in self.tablero):
            return 2  # Empate

        return 0  # El juego continúa
    
    def verificar_ganador(self):
        """
        Método que utiliza 'comprobar_victoria' para verificar el estado del juego.
        """
        return self.comprobar_victoria()
    
    def detectar_jugada_critica(self, jugador):
        """
        Detecta si hay una jugada crítica para ganar o bloquear.
        :param jugador: 1 para humano (bloquear), -1 para IA (ganar)
        :return: Índice de la casilla crítica (0-8) o None si no hay jugada crítica
        """
        combinaciones = [
            [0, 1, 2], [3, 4, 5], [6, 7, 8],  # Filas
            [0, 3, 6], [1, 4, 7], [2, 5, 8],  # Columnas
            [0, 4, 8], [2, 4, 6],             # Diagonales
        ]

        for combinacion in combinaciones:
            valores = [self.tablero[i] for i in combinacion]
            if valores.count(jugador) == 2 and valores.count(0) == 1:
                return combinacion[valores.index(0)]  # Casilla crítica

        return None
