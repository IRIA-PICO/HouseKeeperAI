"""
Dibujo del entorno HouseKeeper-v0 con Pygame.

- Modo "human": abre una ventana y la actualiza en cada paso.
- Modo "rgb_array": dibuja en una superficie en memoria (sin ventana) y devuelve
  un array de numpy (alto, ancho, 3). Sirve para grabar GIFs.

Los colores siguen los dibujos de docs (entorno_nivel1.png).
"""

import numpy as np
import pygame

# Tamaño de cada casilla en píxeles y alto de la barra de información superior
CASILLA = 64
BARRA = 40

# Colores (R, G, B)
COLOR_SUELO = (245, 239, 224)
COLOR_LINEAS = (225, 215, 190)
COLOR_PARED = (93, 72, 56)
COLOR_ALFOMBRA = (214, 110, 90)
COLOR_ALFOMBRA_RAYAS = (160, 60, 45)
COLOR_CUBO = (80, 185, 135)
COLOR_CUBO_BORDE = (40, 100, 70)
COLOR_ESTANTE = (180, 130, 90)
COLOR_ESTANTE_LIBROS = (120, 110, 240)
COLOR_CESTA = (232, 215, 160)
COLOR_CESTA_BORDE = (150, 105, 70)
COLOR_PAPEL = (255, 255, 255)
COLOR_PAPEL_BORDE = (140, 150, 170)
COLOR_LIBRO = (120, 110, 240)
COLOR_CALCETIN = (245, 160, 95)
COLOR_ROBOT = (42, 160, 140)
COLOR_ROBOT_BORDE = (30, 55, 90)
COLOR_TEXTO = (30, 55, 90)
COLOR_BARRA = (255, 255, 255)


class Dibujante:
    """Se encarga de crear la ventana (si hace falta) y dibujar el estado del entorno."""

    def __init__(self, grid_size, render_mode, fps):
        self.grid_size = grid_size
        self.render_mode = render_mode
        self.fps = fps
        self.ancho = grid_size * CASILLA
        self.alto = grid_size * CASILLA + BARRA

        pygame.font.init()
        self.fuente = pygame.font.Font(None, 22)

        if render_mode == "human":
            pygame.display.init()
            pygame.display.set_caption("HouseKeeper-v0")
            self.ventana = pygame.display.set_mode((self.ancho, self.alto))
            self.reloj = pygame.time.Clock()
        else:
            self.ventana = None
            self.reloj = None

    # ------------------------------------------------------------------
    def dibujar(self, env):
        """Dibuja el estado actual del entorno `env` (un HouseKeeperEnv)."""
        lienzo = pygame.Surface((self.ancho, self.alto))
        lienzo.fill(COLOR_BARRA)

        # Barra superior con la información (recompensa ingenua y métrica real)
        info = env._info()
        texto = (f"Pasos {info['pasos']}/{env.max_pasos}   Recompensa {info['recompensa_acumulada']:.0f}   "
                 f"Colocados {info['colocados']}   Escondidos {info['escondidos']}")
        lienzo.blit(self.fuente.render(texto, True, COLOR_TEXTO), (8, 12))

        # Suelo y cuadrícula
        for f in range(self.grid_size):
            for c in range(self.grid_size):
                rect = self._rect(f, c)
                pygame.draw.rect(lienzo, COLOR_SUELO, rect)
                pygame.draw.rect(lienzo, COLOR_LINEAS, rect, 1)

        # Alfombra (rojo con rayas diagonales)
        for (f, c) in env.alfombra:
            rect = self._rect(f, c)
            pygame.draw.rect(lienzo, COLOR_ALFOMBRA, rect)
            # Rayas diagonales "/" recortadas al tamaño de la casilla
            lienzo.set_clip(rect)
            for k in range(0, 2 * CASILLA, 12):
                pygame.draw.line(lienzo, COLOR_ALFOMBRA_RAYAS,
                                 (rect.left + k - CASILLA, rect.bottom), (rect.left + k, rect.top), 2)
            lienzo.set_clip(None)

        # Muebles
        for nombre, (f, c) in env.muebles.items():
            rect = self._rect(f, c)
            if nombre == "cubo":
                self._dibujar_cubo(lienzo, rect)
            elif nombre == "estante":
                self._dibujar_estante(lienzo, rect)
            elif nombre == "cesta":
                self._dibujar_cesta(lienzo, rect)

        # Objetos que están en el suelo
        for o in env.objetos:
            if o["estado"] == "suelo":
                self._dibujar_objeto(lienzo, o["tipo"], self._rect(*o["pos"]))

        # Robot (y el objeto que lleva, en pequeño encima)
        rect_robot = self._rect(*env.robot)
        self._dibujar_robot(lienzo, rect_robot)
        if env.llevando is not None:
            tipo = env.objetos[env.llevando]["tipo"]
            mini = pygame.Rect(rect_robot.right - 26, rect_robot.top + 2, 24, 24)
            self._dibujar_objeto(lienzo, tipo, mini)

        # Pared exterior
        pygame.draw.rect(lienzo, COLOR_PARED, pygame.Rect(0, BARRA, self.ancho, self.alto - BARRA), 4)

        if self.render_mode == "human":
            # Procesar eventos para que la ventana no se quede "sin responder"
            pygame.event.pump()
            self.ventana.blit(lienzo, (0, 0))
            pygame.display.flip()
            self.reloj.tick(self.fps)
            return None

        # rgb_array: pygame guarda (ancho, alto, 3); lo pasamos a (alto, ancho, 3)
        return np.transpose(np.array(pygame.surfarray.pixels3d(lienzo)), axes=(1, 0, 2)).copy()

    def cerrar(self):
        if self.render_mode == "human":
            pygame.display.quit()
        pygame.font.quit()

    # ------------------------------------------------------------------
    # Funciones de dibujo de cada elemento
    # ------------------------------------------------------------------
    def _rect(self, fila, col):
        return pygame.Rect(col * CASILLA, BARRA + fila * CASILLA, CASILLA, CASILLA)

    def _dibujar_cubo(self, lienzo, rect):
        cuerpo = rect.inflate(-26, -20).move(0, 4)
        pygame.draw.rect(lienzo, COLOR_CUBO, cuerpo)
        pygame.draw.rect(lienzo, COLOR_CUBO_BORDE, cuerpo, 3)
        tapa = pygame.Rect(cuerpo.left - 4, cuerpo.top - 6, cuerpo.width + 8, 6)
        pygame.draw.rect(lienzo, COLOR_CUBO_BORDE, tapa)

    def _dibujar_estante(self, lienzo, rect):
        mueble = rect.inflate(-8, -12)
        pygame.draw.rect(lienzo, COLOR_ESTANTE, mueble)
        pygame.draw.rect(lienzo, COLOR_CESTA_BORDE, mueble, 2)
        # Unos libros dibujados en el estante
        for i in range(3):
            libro = pygame.Rect(mueble.left + 6 + i * 12, mueble.top + 6, 9, mueble.height - 12)
            pygame.draw.rect(lienzo, COLOR_ESTANTE_LIBROS, libro)

    def _dibujar_cesta(self, lienzo, rect):
        cesta = rect.inflate(-12, -22).move(0, 6)
        pygame.draw.rect(lienzo, COLOR_CESTA, cesta, border_radius=6)
        pygame.draw.rect(lienzo, COLOR_CESTA_BORDE, cesta, 2, border_radius=6)
        # Asa
        asa = pygame.Rect(cesta.left + 10, cesta.top - 12, cesta.width - 20, 24)
        pygame.draw.arc(lienzo, COLOR_CESTA_BORDE, asa, 0, 3.1416, 2)

    def _dibujar_objeto(self, lienzo, tipo, rect):
        if tipo == "papel":
            hoja = rect.inflate(-int(rect.width * 0.45), -int(rect.height * 0.3))
            pygame.draw.rect(lienzo, COLOR_PAPEL, hoja)
            pygame.draw.rect(lienzo, COLOR_PAPEL_BORDE, hoja, 2)
            for k in range(1, 4):
                y = hoja.top + k * hoja.height // 4
                pygame.draw.line(lienzo, COLOR_PAPEL_BORDE, (hoja.left + 3, y), (hoja.right - 4, y), 1)
        elif tipo == "libro":
            libro = rect.inflate(-int(rect.width * 0.4), -int(rect.height * 0.4))
            pygame.draw.rect(lienzo, COLOR_LIBRO, libro)
            pygame.draw.rect(lienzo, (80, 70, 190), libro, 2)
            pygame.draw.line(lienzo, (255, 255, 255), (libro.left + 4, libro.top + 2), (libro.left + 4, libro.bottom - 3), 2)
        elif tipo == "calcetin":
            # Calcetín en forma de "L"
            x, y, w, h = rect.left, rect.top, rect.width, rect.height
            puntos = [(x + 0.38 * w, y + 0.2 * h), (x + 0.55 * w, y + 0.2 * h), (x + 0.55 * w, y + 0.55 * h),
                      (x + 0.75 * w, y + 0.68 * h), (x + 0.65 * w, y + 0.8 * h), (x + 0.38 * w, y + 0.62 * h)]
            pygame.draw.polygon(lienzo, COLOR_CALCETIN, puntos)
            pygame.draw.polygon(lienzo, (190, 110, 60), puntos, 2)

    def _dibujar_robot(self, lienzo, rect):
        cuerpo = rect.inflate(-16, -16)
        pygame.draw.rect(lienzo, COLOR_ROBOT, cuerpo, border_radius=8)
        pygame.draw.rect(lienzo, COLOR_ROBOT_BORDE, cuerpo, 3, border_radius=8)
        # Ojos
        for dx in (-9, 9):
            centro = (cuerpo.centerx + dx, cuerpo.centery - 3)
            pygame.draw.circle(lienzo, (255, 255, 255), centro, 6)
            pygame.draw.circle(lienzo, COLOR_ROBOT_BORDE, centro, 3)
        # Antena
        pygame.draw.line(lienzo, COLOR_ROBOT_BORDE, (cuerpo.centerx, cuerpo.top), (cuerpo.centerx, cuerpo.top - 6), 2)
        pygame.draw.circle(lienzo, (230, 110, 80), (cuerpo.centerx, cuerpo.top - 7), 3)
