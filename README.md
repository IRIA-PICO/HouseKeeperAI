# HouseKeeperAI

Proyecto final de la asignatura de Reinforcement Learning (Universidad de Deusto).

## Descripción

HouseKeeperAI es un entorno de Gymnasium (`HouseKeeper-v0`) en el que un robot doméstico
tiene que ordenar una casa en 2D representada como una cuadrícula: llevar los papeles al cubo,
los libros al estante y los calcetines a la cesta.

El proyecto estudia el **reward hacking**: con una recompensa ingenua (premiar que los objetos
desaparezcan del suelo), el robot aprende a hacer trampa y **esconder la basura debajo de la
alfombra** en lugar de colocarla en su sitio.

Para corregirlo usamos **RLHF (Reinforcement Learning from Human Feedback)**: entrenamos un
modelo de recompensa **Bradley-Terry** propio en PyTorch a partir de preferencias entre pares de
trayectorias (A vs B) y después entrenamos al agente con **PPO** usando esa recompensa aprendida.

**Pregunta central:** ¿hace trampas el agente con una recompensa mal diseñada, y aprender la
recompensa a partir de preferencias lo corrige?

## Instalación

TODO: versión de Python, pasos para crear el entorno virtual y versiones exactas de las librerías
(se fijarán al instalar).

```bash
# TODO
pip install -r requirements.txt
```

## Probar el entorno (Fase 1)

Desde la carpeta `HouseKeeperAI`, con el entorno virtual activado:

```bash
python probar_entorno.py          # check_env, episodio aleatorio, prueba de la trampa y captura
python probar_entorno.py --ver    # igual, pero enseña el episodio aleatorio en una ventana
python play_manual.py             # jugar con el teclado (flechas, C coger, S soltar, E esconder, R reiniciar)
python play_manual.py --grid 6 --seed 3
```

Uso desde código:

```python
import gymnasium as gym
import housekeeper_env  # registra HouseKeeper-v0

env = gym.make("HouseKeeper-v0", grid_size=8, render_mode="human")
obs, info = env.reset(seed=0)
obs, recompensa, terminado, truncado, info = env.step(env.action_space.sample())
print(info)  # métrica real: colocados, escondidos, pasos, acciones_inutiles...
```

Problemas de instalación y versiones probadas: `docs/problemas_instalacion.md`.

## Cómo entrenar

TODO

## Cómo evaluar

TODO

## Estructura de carpetas

```
HouseKeeperAI/
├── README.md
├── requirements.txt
├── .gitignore
├── play_manual.py     # jugar al entorno con el teclado
├── probar_entorno.py  # pruebas rápidas del entorno (check_env, episodio aleatorio)
├── housekeeper_env/   # entorno Gymnasium HouseKeeper-v0
│   ├── __init__.py    # registra HouseKeeper-v0
│   ├── house_env.py   # lógica del entorno (reset, step, observación, info)
│   ├── rewards.py     # funciones de recompensa (de momento, la ingenua)
│   └── render.py      # dibujo con Pygame (human y rgb_array)
├── rlhf/              # preferencias y modelo de recompensa (TODO)
└── docs/              # gráficas, resultados y documentación
```

TODO: completar cuando estén los scripts.

## Integrantes

- Iria Picó
- Lucía Diez
