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
    
    Jugador 1: Negro
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

        # Jugador inicial (Negro comienza en Othello)
        self.turno = 1