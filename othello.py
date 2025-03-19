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
        self.tablero = [[0] * 8 for _ in range(8)]

        self.tablero[3][3] = 1
        self.tablero[3][4] = 2
        self.tablero[4][3] = 2
        self.tablero[4][4] = 1

        self.turno = 1
    
    def jugadas_legales(self, s, j):
        """
        Devuelve una lista con las jugadas legales para el jugador j
        en el estado s (tablero).

        Parámetros:
        - s: Estado actual del tablero (matriz 8x8 como lista de listas).
        - j: Jugador actual (1 = Blanco, 2 = Negro).

        Una jugada es válida si:
        - Se coloca en una casilla vacía.
        - Hay al menos una ficha del oponente adyacente.
        - Se puede capturar al menos una ficha del oponente en alguna dirección.
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
                    
                    # Verifica si hay fichas volteables y termina en una del jugador actual.
                    if fichas_a_voltear and 0 <= x < 8 and 0 <= y < 8 and s[x][y] == j:
                        jugadas_validas.append((fila, columna))
                        break

        return jugadas_validas
    
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

    
    
    def muestra_tablero(self):
        """
        Muestra el tablero de forma legible en la consola.
        """
        simbolos = {0: '·', 1: 'B', 2: 'N'}
        print("  1 2 3 4 5 6 7 8")
        for i, fila in enumerate(self.tablero):
            print(i + 1, " ".join(simbolos[c] for c in fila))