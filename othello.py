from juegos_simplificado import ModeloJuegoZT2
from juegos_simplificado import juega_dos_jugadores
from minimax import jugador_negamax
from minimax import minimax_iterativo
from juegos_simplificado import minimax

class othello(ModeloJuegoZT2):
    """
    Juego de Othello.

    Se tendra una tabla de 8x8 donde, inicialmente, los
    espacios [4:4] y [5:5] estan ocupados por el jugador
    blanco y los espacios [5:4] y [4:5] por el jugador
    negro. El objetivo es que un jugador tenga mas piezas
    que el otro hasta que ya no se puedan poner mas.

    Cada jugador puede poner una pieza donde se encuentre
    una suya y alla al menos una pieza adyacente del jugador
    opuesto para que el jugador actual pueda colocar su pieza
    al otro lado de esta, convirtiendo todas las piezas del
    jugador opuesto.

    El juego termina cuando ya no sea posible poner mas piezas.
    
    Jugador 1: Negro (Jugador Inicial)
    Jugador 2: Blanco

    Estado Inicial:
       1  2  3  4  5  6  7  8
    1 [ ][ ][ ][ ][ ][ ][ ][ ]
    2 [ ][ ][ ][ ][ ][ ][ ][ ]
    3 [ ][ ][ ][ ][ ][ ][ ][ ]
    4 [ ][ ][ ][B][N][ ][ ][ ]
    5 [ ][ ][ ][N][B][ ][ ][ ]
    6 [ ][ ][ ][ ][ ][ ][ ][ ]
    7 [ ][ ][ ][ ][ ][ ][ ][ ]
    8 [ ][ ][ ][ ][ ][ ][ ][ ]
    """

    def inicializa(self):
        """
        Inicializa el juego de Othello.
        """
        self.tablero = [[0] * 8 for _ in range(8)]  # Inicializa un tablero vacío de 8x8
        # Coloca las fichas iniciales
        self.tablero[3][3], self.tablero[4][4] = 1, 1  # Blancas
        self.tablero[3][4], self.tablero[4][3] = -1, -1  # Negras

        self.turno = 1

        # Se retorna el estado inicial como una tupla inmutable
        return tuple(tuple(fila) for fila in self.tablero), self.turno
    
    def jugadas_legales(self, s, j):
        """
        Devuelve una lista con las jugadas legales para el jugador j en el estado s.
        """
        direcciones = [(-1, -1), (-1, 0), (-1, 1),
                    (0, -1),        (0, 1),
                    (1, -1), (1, 0), (1, 1)]

        oponente = 1 if j == 2 else 2
        jugadas_validas = []

        for fila in range(8):
            for columna in range(8):
                if s[fila][columna] != 0:  # Se ignoran las casillas ocupadas
                    continue

                for dx, dy in direcciones:
                    x, y = fila + dx, columna + dy
                    fichas_a_voltear = []

                    while 0 <= x < 8 and 0 <= y < 8 and s[x][y] == oponente:
                        fichas_a_voltear.append((x, y))
                        x += dx
                        y += dy
                    
                    # Si encontramos una ficha del mismo jugador, es una jugada válida
                    if fichas_a_voltear and 0 <= x < 8 and 0 <= y < 8 and s[x][y] == j:
                        jugadas_validas.append((fila, columna))
                        break

        return jugadas_validas
    
    def realiza_jugada(self, tablero, jugador, jugada):
        """
        Aplica la jugada al tablero y voltea las fichas correspondientes.
        """
        direcciones = [(-1, -1), (-1, 0), (-1, 1),
                    (0, -1),        (0, 1),
                    (1, -1), (1, 0), (1, 1)]

        fila, columna = jugada
        tablero = list(map(list, tablero))  # Convierte cada fila en una lista
        oponente = 1 if jugador == 2 else 2

        for dx, dy in direcciones:
            x, y = fila + dx, columna + dy
            fichas_a_voltear = []

            while 0 <= x < 8 and 0 <= y < 8 and tablero[x][y] == oponente:
                fichas_a_voltear.append((x, y))
                x += dx
                y += dy
            
            # Si al final hay una ficha del mismo jugador, se voltean las fichas atrapadas
            if fichas_a_voltear and 0 <= x < 8 and 0 <= y < 8 and tablero[x][y] == jugador:
                for fx, fy in fichas_a_voltear:
                    tablero[fx][fy] = jugador

        return tablero

    
    def transicion(self, s, a, j):
        """
        Devuelve el estado que resulta de realizar la jugada a en el estado s
        para el jugador j.
        
        Parámetros:
        - s: Estado actual del tablero (matriz 8x8 como lista de listas).
        - a: Tupla (fila, columna) con la jugada elegida.
        - j: Jugador actual (1 = Blanco, 2 = Negro).
        """
        # Copia profunda del estado para evitar modificar el original
        nuevo_estado = [fila[:] for fila in s]

        # Aplica la jugada y voltea fichas
        nuevo_estado = self.realiza_jugada(nuevo_estado, j, a)

        # Convertir a tupla de tuplas para inmutabilidad
        return tuple(tuple(fila) for fila in nuevo_estado)

    def terminal(self, s):
        """
        Devuelve True si el estado s es terminal (ningún jugador puede jugar).
        """
        return not self.jugadas_legales(s, 1) and not self.jugadas_legales(s, 2)

    def ganancia(self, s):
        """
        Devuelve la diferencia de fichas entre los jugadores al finalizar el juego.
        Un valor positivo favorece a las blancas, un valor negativo a las negras.
        """
        blancas = sum(fila.count(1) for fila in s)
        negras = sum(fila.count(2) for fila in s)
        
        return blancas - negras  # Se usa para que jugador 1 (Blanco) busque maximizar


    def muestra_tablero(self):
        """
        Muestra el tablero de forma legible en la consola.
        """
        simbolos = {0: '·', 1: 'B', 2: 'N', -1: 'N'}  # Agregar -1 como 'N' (Negro)
        print("  1 2 3 4 5 6 7 8")
        for i, fila in enumerate(self.tablero):
            print(i + 1, " ".join(simbolos[c] for c in fila))

if __name__ == "__main__":
    juego = othello()

    resultado, estado_final = juega_dos_jugadores(
        juego,
        lambda juego, estado, jugador: minimax(juego, estado, jugador), 
        lambda juego, estado, jugador: minimax_iterativo(juego, estado, jugador, tiempo=2)
    )

    juego.muestra_tablero()
    print(f"Resultado final: {'Empate' if resultado == 0 else 'Gana Blanco' if resultado > 0 else 'Gana Negro'}")
