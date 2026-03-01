import pygame
import random
import time

# Configuración de la pantalla
pygame.init()
ANCHO, ALTO = 300, 600
TAM_CELDA = 30
ANCHO_CELDAS, ALTO_CELDAS = ANCHO // TAM_CELDA, ALTO // TAM_CELDA
VENTANA = pygame.display.set_mode((ANCHO, ALTO))
pygame.display.set_caption("Tetris")

# Colores
NEGRO = (0, 0, 0)
BLANCO = (255, 255, 255)
ROJO = (255, 0, 0)
VERDE = (0, 255, 0)
AZUL = (0, 0, 255)
CIAN = (0, 255, 255)
MAGENTA = (255, 0, 255)
AMARILLO = (255, 255, 0)
NARANJA = (255, 165, 0)

# Formas de las piezas
FORMAS = [
    [[1, 1, 1, 1]],  # I
    [[1, 1, 1], [0, 1, 0]],  # T
    [[1, 1, 0], [0, 1, 1]],  # S
    [[0, 1, 1], [1, 1, 0]],  # Z
    [[1, 1, 1], [1, 0, 0]],  # L
    [[1, 1, 1], [0, 0, 1]],  # J
    [[1, 1], [1, 1]]  # O
]

COLORES_FORMAS = [CIAN, MAGENTA, VERDE, ROJO, AZUL, NARANJA, AMARILLO]


class PiezaTetris:
    def __init__(self):
        self.x = ANCHO_CELDAS // 2 - 1
        self.y = 0
        self.forma = random.choice(FORMAS)
        self.color = random.choice(COLORES_FORMAS)

    def rotar(self):
        self.forma = list(zip(*reversed(self.forma)))

    def mover(self, tablero, dx, dy):  # Agregar el argumento 'tablero' aquí
        if self.puede_moverse(tablero, dx, dy):
            self.x += dx
            self.y += dy

    def puede_moverse(self, tablero, dx, dy):  # Agregar el argumento 'tablero' aquí
        for fila in range(len(self.forma)):
            for col in range(len(self.forma[fila])):
                if self.forma[fila][col] == 1:
                    nueva_x = self.x + col + dx
                    nueva_y = self.y + fila + dy
                    if nueva_x < 0 or nueva_x >= ANCHO_CELDAS or nueva_y >= ALTO_CELDAS:
                        return False
                    if nueva_y >= 0 and tablero[nueva_y][nueva_x]:  # Verificar colisión con otras piezas fijas
                        return False
        return True

    def dibujar(self):
        for fila in range(len(self.forma)):
            for col in range(len(self.forma[fila])):
                if self.forma[fila][col] == 1:
                    pygame.draw.rect(VENTANA, self.color, (self.x * TAM_CELDA + col * TAM_CELDA,
                                                          self.y * TAM_CELDA + fila * TAM_CELDA, TAM_CELDA, TAM_CELDA))


def dibujar_rejilla():
    for x in range(0, ANCHO, TAM_CELDA):
        pygame.draw.line(VENTANA, BLANCO, (x, 0), (x, ALTO))
    for y in range(0, ALTO, TAM_CELDA):
        pygame.draw.line(VENTANA, BLANCO, (0, y), (ANCHO, y))


def main():
    reloj = pygame.time.Clock()
    pieza_tetris = PiezaTetris()
    fin_juego = False
    tiempo_caida = 0
    velocidad_caida = 0.5  # Tiempo en segundos entre caídas automáticas de la pieza

    # Creamos una matriz para representar el tablero del juego
    tablero = [[None for _ in range(ANCHO_CELDAS)] for _ in range(ALTO_CELDAS)]

    def movimiento_valido(forma, x, y):
        for fila in range(len(forma)):
            for col in range(len(forma[fila])):
                if forma[fila][col] == 1:
                    nueva_x = x + col
                    nueva_y = y + fila
                    if (
                        nueva_x < 0
                        or nueva_x >= ANCHO_CELDAS
                        or nueva_y >= ALTO_CELDAS
                        or (nueva_y >= 0 and tablero[nueva_y][nueva_x])
                    ):
                        return False
        return True

    def colocar_pieza_en_tablero(forma, x, y, color):
        for fila in range(len(forma)):
            for col in range(len(forma[fila])):
                if forma[fila][col] == 1:
                    fila_tablero = y + fila
                    col_tablero = x + col
                    tablero[fila_tablero][col_tablero] = color

    def eliminar_linea(linea):
        for fila in range(linea, 0, -1):
            tablero[fila] = tablero[fila - 1][:]
        tablero[0] = [None for _ in range(ANCHO_CELDAS)]

    # Sistema de puntaje
    puntaje = 0
    ultimo_tiempo_puntaje = pygame.time.get_ticks()

    while not fin_juego:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                fin_juego = True
            elif evento.type == pygame.KEYDOWN:  # Verificar si el evento es un evento de teclado
                if evento.key == pygame.K_LEFT:
                    pieza_tetris.mover(tablero, -1, 0)  # Pasar 'tablero' y 'dx'
                    if not pieza_tetris.puede_moverse(tablero, 0, 0):
                        pieza_tetris.mover(tablero, 1, 0)  # Pasar 'tablero' y 'dx' para deshacer el movimiento
                elif evento.key == pygame.K_RIGHT:
                    pieza_tetris.mover(tablero, 1, 0)  # Pasar 'tablero' y 'dx'
                    if not pieza_tetris.puede_moverse(tablero, 0, 0):
                        pieza_tetris.mover(tablero, -1, 0)  # Pasar 'tablero' y 'dx' para deshacer el movimiento
                elif evento.key == pygame.K_DOWN:
                    pieza_tetris.mover(tablero, 0, 1)  # Pasar 'tablero' y 'dy'
                    if not pieza_tetris.puede_moverse(tablero, 0, 0):
                        pieza_tetris.mover(tablero, 0, -1)  # Pasar 'tablero' y 'dy' para deshacer el movimiento
                elif evento.key == pygame.K_UP:
                    pieza_tetris.rotar()
                    if not pieza_tetris.puede_moverse(tablero, 0, 0):
                        pieza_tetris.rotar()  # Deshacer la rotación si colisiona

        # Movimiento automático hacia abajo
        tiempo_actual = pygame.time.get_ticks()
        if tiempo_actual - tiempo_caida > velocidad_caida * 1000:
            if pieza_tetris.puede_moverse(tablero, 0, 1):
                pieza_tetris.mover(tablero, 0, 1)  # Pasar 'tablero' y 'dy'
            else:
                colocar_pieza_en_tablero(pieza_tetris.forma, pieza_tetris.x, pieza_tetris.y, pieza_tetris.color)
                pieza_tetris = PiezaTetris()

                
                # Verificar si alguna parte de la nueva pieza está por encima del área visible del tablero
                if pieza_tetris.y < 0:
                    fuente_game_over = pygame.font.SysFont(None, 50)
                    texto_game_over = fuente_game_over.render("Game Over", True, BLANCO)
                    VENTANA.blit(texto_game_over, (ANCHO // 2 - texto_game_over.get_width() // 2, ALTO // 2 - texto_game_over.get_height() // 2))
                    pygame.display.update()
                    time.sleep(2)
                    fin_juego = True

                # Verificar si alguna parte de la pieza actual quedó fijada en la fila de arriba
                for col in range(ANCHO_CELDAS):
                    if tablero[0][col] is not None:
                        fuente_game_over = pygame.font.SysFont(None, 50)
                        texto_game_over = fuente_game_over.render("Game Over", True, BLANCO)
                        VENTANA.blit(texto_game_over, (ANCHO // 2 - texto_game_over.get_width() // 2, ALTO // 2 - texto_game_over.get_height() // 2))
                        pygame.display.update()
                        time.sleep(2)
                        fin_juego = True
                        break

                # Verificar si hay líneas completas y eliminarlas del tablero
                lineas_a_eliminar = []
                for fila in range(ALTO_CELDAS):
                    if all(tablero[fila]):
                        lineas_a_eliminar.append(fila)

                for linea in lineas_a_eliminar:
                    eliminar_linea(linea)
                    puntaje += 10  # Incrementar el puntaje por cada línea completa

                # Verificar si alguna parte de la nueva pieza está por encima del área visible del tablero
                if pieza_tetris.y < 0:
                    fin_juego = True

            tiempo_caida = tiempo_actual

        VENTANA.fill(NEGRO)
        dibujar_rejilla()

        # Dibujar los bloques fijos en el tablero
        for fila in range(ALTO_CELDAS):
            for col in range(ANCHO_CELDAS):
                color = tablero[fila][col]
                if color:
                    pygame.draw.rect(VENTANA, color, (col * TAM_CELDA, fila * TAM_CELDA, TAM_CELDA, TAM_CELDA))

        pieza_tetris.dibujar()
        
        # Mostrar el puntaje en la pantalla
        fuente = pygame.font.SysFont(None, 25)
        texto_puntaje = fuente.render(f"Puntaje: {puntaje}", True, BLANCO)
        VENTANA.blit(texto_puntaje, (10, 10))
        
        pygame.display.update()
        reloj.tick(60)  # 60 FPS

    # Mostrar "Game Over" cuando el juego termine
    fuente = pygame.font.SysFont(None, 50)
    texto_fin_juego = fuente.render("Game Over", True, BLANCO)
    VENTANA.blit(texto_fin_juego, (ANCHO // 2 - texto_fin_juego.get_width() // 2, ALTO // 2 - texto_fin_juego.get_height() // 2))

    # Esperar un poco antes de salir
    pygame.time.delay(2000)

    pygame.quit()

if __name__ == "__main__":
    main()