"""
Jugar a mano al entorno HouseKeeper-v0 con el teclado.

Ejecutar desde la carpeta HouseKeeperAI:
    python play_manual.py                  # cuadrícula 8x8
    python play_manual.py --grid 6 --seed 3

Teclas:
    Flechas  -> moverse
    C        -> coger
    S        -> soltar (en el cubo, estante, cesta o en el suelo)
    E        -> esconder bajo la alfombra (la trampa)
    R        -> reiniciar la casa
    Esc      -> salir
"""

import argparse

import pygame

from housekeeper_env.house_env import (ARRIBA, ABAJO, IZQUIERDA, DERECHA, COGER, SOLTAR, ESCONDER,
                                       NOMBRES_ACCIONES, HouseKeeperEnv)

TECLAS = {
    pygame.K_UP: ARRIBA,
    pygame.K_DOWN: ABAJO,
    pygame.K_LEFT: IZQUIERDA,
    pygame.K_RIGHT: DERECHA,
    pygame.K_c: COGER,
    pygame.K_s: SOLTAR,
    pygame.K_e: ESCONDER,
}


def main():
    parser = argparse.ArgumentParser(description="Jugar a HouseKeeper-v0 con el teclado")
    parser.add_argument("--grid", type=int, default=8, choices=[6, 8, 10], help="tamaño de la cuadrícula")
    parser.add_argument("--seed", type=int, default=None, help="semilla para colocar la casa")
    args = parser.parse_args()

    env = HouseKeeperEnv(grid_size=args.grid, render_mode="human")
    env.reset(seed=args.seed)
    print(__doc__)

    jugando = True
    fin_episodio = False  # cuando acaba el episodio se ignoran las acciones hasta pulsar R
    while jugando:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                jugando = False
            elif evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_ESCAPE:
                    jugando = False
                elif evento.key == pygame.K_r:
                    env.reset()
                    fin_episodio = False
                    print("--- Casa reiniciada ---")
                elif evento.key in TECLAS and not fin_episodio:
                    accion = TECLAS[evento.key]
                    _, recompensa, terminado, truncado, info = env.step(accion)
                    print(f"{NOMBRES_ACCIONES[accion]:>9} | recompensa {recompensa:+.0f} | "
                          f"colocados {info['colocados']} | escondidos {info['escondidos']} | "
                          f"inútiles {info['acciones_inutiles']} | pasos {info['pasos']}")
                    if terminado or truncado:
                        fin_episodio = True
                        motivo = "¡suelo vacío!" if terminado else "límite de pasos"
                        print(f"=== Fin del episodio ({motivo}). Métrica real: {info} ===")
                        print("Pulsa R para jugar otra vez o Esc para salir.")
        # Redibujar aunque no se pulse nada (para que la ventana responda)
        env.render()

    env.close()


if __name__ == "__main__":
    main()
