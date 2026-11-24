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
├── housekeeper_env/   # entorno Gymnasium (TODO)
├── rlhf/              # preferencias y modelo de recompensa (TODO)
└── docs/              # gráficas, resultados y documentación
```

TODO: completar cuando estén los scripts.

## Integrantes

- Iria Picó
- Lucía Diez
