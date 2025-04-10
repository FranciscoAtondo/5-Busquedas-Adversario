from juegos_simplificado import ModeloJuegoZT2
from juegos_simplificado import juega_dos_jugadores
from minimax import jugador_negamax
from minimax import minimax_iterativo
from juegos_simplificado import minimax

class Othello(ModeloJuegoZT2):
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
        """ Inicializa el tablero con la posición inicial de Othello """
        s = [0] * 64
        s[27], s[28], s[35], s[36] = 1, -1, -1, 1  # Configuración inicial
        return tuple(s), 1  # Comienza el jugador 1

    def imprime_estado(self, s):
        """ Imprime el tablero de Othello en formato 8x8 """
        simbolos = {0: '.', 1: 'X', -1: 'O'}
        for i in range(8):
            print(' '.join(simbolos[s[j]] for j in range(i*8, (i+1)*8)))
        print()
    
    def jugadas_legales(self, s, j):
        """ Devuelve la lista de posiciones donde el jugador j puede colocar una ficha """
        direcciones = [-1, 1, -8, 8, -9, 9, -7, 7]  # Movimientos en todas direcciones
        jugadas = set()

        for i in range(64):
            if s[i] != j:
                continue
            for d in direcciones:
                pos = i + d
                if not (0 <= pos < 64):
                    continue
                if s[pos] == -j:  # Hay una ficha del oponente
                    while 0 <= pos < 64 and s[pos] == -j:
                        pos += d
                    if 0 <= pos < 64 and s[pos] == 0:
                        jugadas.add(pos)
        return list(jugadas)

    def transicion(self, s, a, j):
        """ Coloca la ficha en la posición a y cambia las fichas capturadas """
        direcciones = [-1, 1, -8, 8, -9, 9, -7, 7]
        s = list(s)
        s[a] = j  # Coloca la ficha

        for d in direcciones:
            pos = a + d
            capturas = []
            while 0 <= pos < 64 and s[pos] == -j:
                capturas.append(pos)
                pos += d
            if 0 <= pos < 64 and s[pos] == j:
                for p in capturas:
                    s[p] = j  # Captura las fichas del oponente

        return tuple(s)

    def terminal(self, s):
        """ Verifica si el juego ha terminado (no hay jugadas legales para ningún jugador) """
        return not self.jugadas_legales(s, 1) and not self.jugadas_legales(s, -1)

    def ganancia(self, s):
        """ Calcula la ganancia como la diferencia de fichas entre los jugadores """
        return sum(s)

class JugadorNegamaxOthello:
    def __init__(self, nombre="AI", profundidad=4, evalua=None):
        self.nombre = nombre
        self.profundidad = profundidad
        self.evalua = evalua

    def politica(self, juego, estado):
        return jugador_negamax(
            juego=juego, 
            estado=estado[0],  # estado es una tupla (tablero, jugador)
            jugador=estado[1], 
            d=self.profundidad, 
            evalua=self.evalua
        )



class JugadorHumanoOthello:
    def __init__(self, nombre="Humano"):
        self.nombre = nombre
    
    def politica(self, juego, estado):
        juego.imprime_estado(estado[0])
        jugadas = juego.jugadas_legales(estado[0], estado[1])
        if not jugadas:
            print("No hay jugadas disponibles. Turno perdido.")
            return None
        print(f"Jugadas legales: {jugadas}")
        return int(input("Elige una jugada: "))

class PartidaZT2:
    def __init__(self, juego, jugador1, jugador2):
        self.juego = juego
        self.jugadores = {1: jugador1, -1: jugador2}
        self.estado = juego.inicializa()
    
    def jugar(self, verbose=True):
        """Ejecuta el juego hasta el final."""
        while not self.juego.terminal(self.estado[0]):
            jugador = self.jugadores[self.estado[1]]
            jugada = jugador.politica(self.juego, self.estado)
            if jugada is not None:
                self.estado = (self.juego.transicion(self.estado[0], jugada, self.estado[1]), -self.estado[1])
            if verbose:
                self.juego.imprime_estado(self.estado[0])

        print("Juego terminado.")
        resultado = self.juego.ganancia(self.estado[0])
        if resultado > 0:
            print("Gana Jugador 1 (X)")
        elif resultado < 0:
            print("Gana Jugador 2 (O)")
        else:
            print("Empate.")


# Crear instancia del juego
juego = Othello()

# Prueba con jugador humano
jugador1 = JugadorHumanoOthello("Jugador 1")
jugador2 = JugadorNegamaxOthello(nombre="Máquina", profundidad=)

# Ejecutar partida
partida = PartidaZT2(juego, jugador1, jugador2)
partida.jugar(True)
