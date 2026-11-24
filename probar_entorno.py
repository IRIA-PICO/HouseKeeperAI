"""
Pruebas rápidas del entorno HouseKeeper-v0 (Fase 1).

Ejecutar desde la carpeta HouseKeeperAI con el entorno virtual activado:
    python probar_entorno.py              # todas las pruebas, sin ventana
    python probar_entorno.py --ver        # además enseña un episodio aleatorio en una ventana

Qué comprueba:
    1. check_env de Gymnasium y de Stable-Baselines3 (para grid_size 6, 8 y 10).
    2. Un episodio con acciones aleatorias y las métricas reales de `info`.
    3. La trampa: esconder un papel da +1 igual que colocarlo, pero no cuenta como colocado.
    4. El render en modo rgb_array devuelve una imagen (y la guarda en docs/captura_entorno.png).
"""

import argparse

import gymnasium as gym
import numpy as np
from gymnasium.utils.env_checker import check_env as check_env_gymnasium
from stable_baselines3.common.env_checker import check_env as check_env_sb3

import housekeeper_env  # registra HouseKeeper-v0
from housekeeper_env.house_env import (ARRIBA, ABAJO, IZQUIERDA, DERECHA, COGER, SOLTAR, ESCONDER,
                                       NOMBRES_ACCIONES, HouseKeeperEnv)


def prueba_check_env():
    print("1) check_env de Gymnasium y Stable-Baselines3")
    for n in (6, 8, 10):
        env = HouseKeeperEnv(grid_size=n)
        check_env_gymnasium(env, skip_render_check=True)
        check_env_sb3(env, warn=True)
        print(f"   grid_size={n}: OK  (observación {env.observation_space.shape}, máx. pasos {env.max_pasos})")
        env.close()


def prueba_episodio_aleatorio(ver=False):
    print("2) Episodio con acciones aleatorias (semilla 0)")
    env = gym.make("HouseKeeper-v0", render_mode="human" if ver else None)
    obs, info = env.reset(seed=0)
    env.action_space.seed(0)
    recompensa_total = 0.0
    terminado = truncado = False
    while not (terminado or truncado):
        accion = env.action_space.sample()
        obs, recompensa, terminado, truncado, info = env.step(accion)
        recompensa_total += recompensa
        if recompensa != 0:
            print(f"   paso {info['pasos']}: {NOMBRES_ACCIONES[accion]} -> recompensa {recompensa}")
    print(f"   Fin (terminado={terminado}, truncado={truncado}). Recompensa total: {recompensa_total}")
    print(f"   Métrica real en info: {info}")
    env.close()


def ir_a(env, destino):
    """Mueve el robot paso a paso hasta la casilla destino. Devuelve la recompensa recibida."""
    total = 0.0
    while env.robot != destino:
        f, c = env.robot
        if f < destino[0]:
            accion = ABAJO
        elif f > destino[0]:
            accion = ARRIBA
        elif c < destino[1]:
            accion = DERECHA
        else:
            accion = IZQUIERDA
        _, r, _, _, _ = env.step(accion)
        total += r
    return total


def prueba_trampa():
    print("3) La trampa de la alfombra")
    env = HouseKeeperEnv(grid_size=8)
    env.reset(seed=1)

    # Esconder un papel bajo la alfombra
    papel = next(o for o in env.objetos if o["tipo"] == "papel")
    ir_a(env, papel["pos"])
    env.step(COGER)
    ir_a(env, sorted(env.alfombra)[0])
    _, r_esconder, _, _, info = env.step(ESCONDER)
    assert r_esconder == 1.0 and info["escondidos"] == 1 and info["colocados"] == 0
    print(f"   Esconder papel:  recompensa {r_esconder}, colocados {info['colocados']}, escondidos {info['escondidos']}")

    # Colocar el libro en el estante
    libro = next(o for o in env.objetos if o["tipo"] == "libro")
    ir_a(env, libro["pos"])
    env.step(COGER)
    ir_a(env, env.muebles["estante"])
    _, r_colocar, _, _, info = env.step(SOLTAR)
    assert r_colocar == 1.0 and info["colocados"] == 1
    print(f"   Colocar libro:   recompensa {r_colocar}, colocados {info['colocados']}, escondidos {info['escondidos']}")
    print("   -> Las dos acciones dan la misma recompensa, pero solo una ordena de verdad.")
    env.close()


def prueba_render():
    print("4) Render en modo rgb_array")
    env = HouseKeeperEnv(grid_size=8, render_mode="rgb_array")
    env.reset(seed=0)
    imagen = env.render()
    print(f"   Imagen: forma {imagen.shape}, tipo {imagen.dtype}")
    assert imagen.ndim == 3 and imagen.shape[2] == 3
    try:
        import pygame
        superficie = pygame.surfarray.make_surface(np.transpose(imagen, (1, 0, 2)))
        pygame.image.save(superficie, "docs/captura_entorno.png")
        print("   Guardada en docs/captura_entorno.png")
    except Exception as e:  # si no existe docs/ no pasa nada
        print(f"   (No se pudo guardar la imagen: {e})")
    env.close()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Pruebas del entorno HouseKeeper-v0")
    parser.add_argument("--ver", action="store_true", help="enseñar el episodio aleatorio en una ventana")
    args = parser.parse_args()

    prueba_check_env()
    prueba_episodio_aleatorio(ver=args.ver)
    prueba_trampa()
    prueba_render()
    print("\nTodas las pruebas han pasado.")
