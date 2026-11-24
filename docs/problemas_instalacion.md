# Problemas de instalación y versiones

Registro de cada problema que aparece al instalar o probar el proyecto. Sirve para la
guía de instalación de la memoria (10% de la nota). Se añade una entrada por problema.

## Versiones que funcionan (Fase 1)

Probado el 24/11/2026 en Linux (contenedor en la nube), con un entorno virtual nuevo.
**Falta confirmarlo en Windows** en el ordenador de cada integrante.

| Paquete | Versión |
|---|---|
| Python | 3.11.18 |
| gymnasium | 1.4.0 |
| numpy | 2.4.6 |
| pygame | 2.6.1 |
| stable-baselines3 | 2.9.2 |
| torch | 2.15.0 (la instala stable-baselines3 como dependencia) |
| cloudpickle | 3.1.3 (dependencia) |
| Farama-Notifications | 0.0.6 (dependencia) |

`tensorboard` y `matplotlib` no se han instalado todavía porque la Fase 1 no los usa.

Con estas versiones pasan `check_env` de Gymnasium y de Stable-Baselines3 (sin avisos) y
PPO y DQN arrancan con el entorno (prueba de humo de unos pocos miles de pasos, sin
entrenar de verdad).

Pasos usados (en Windows sería `py -3.11 -m venv .venv` y `.venv\Scripts\activate`):

```bash
python3.11 -m venv .venv
source .venv/bin/activate
pip install gymnasium pygame stable-baselines3 numpy
python probar_entorno.py
```

## Problemas encontrados

### 1. El ejemplo de clase (Entorno1.rar) usa librerías antiguas

- **Qué pasa:** el `pip freeze` del README de `Entorno1.rar` fija `gym==0.20.0`, `gym-unity`,
  `mlagents`, `tensorflow==2.11`, `numpy==1.21.2` y `stable-baselines3==2.0.0`. Es la API
  antigua de `gym` (`step` devuelve `done`) y es para un entorno de Unity.
- **Por qué es un problema:** nuestro entorno usa `gymnasium` (`step` devuelve
  `terminated` y `truncated`). Mezclar `gym` y `gymnasium` en el mismo entorno virtual
  produce errores de API, y esas versiones de numpy/tensorflow no se instalan en Python 3.11.
- **Solución:** no instalar ese `pip freeze`. Usar solo las librerías de la tabla de arriba.

### 2. Python demasiado nuevo en el `.venv` antiguo

- **Qué pasa:** la guía del proyecto indica que el `.venv` que había en la carpeta usaba
  Python 3.14, demasiado nuevo para Stable-Baselines3 y PyTorch en muchos casos.
- **Solución:** crear un entorno virtual nuevo con Python 3.11.

### 3. La instalación de stable-baselines3 descarga PyTorch (muy pesado)

- **Qué pasa:** `pip install stable-baselines3` instala `torch` como dependencia. En Linux
  descarga además las librerías de CUDA (varios GB) y tardó varios minutos.
- **Solución recomendada:** si no hay GPU NVIDIA, instalar antes la versión de CPU de PyTorch,
  que es mucho más ligera y suficiente para este proyecto:
  `pip install torch --index-url https://download.pytorch.org/whl/cpu`
  y después `pip install stable-baselines3`.

### 4. Probar Pygame sin pantalla

- **Qué pasa:** en un servidor sin pantalla (como el contenedor donde se hicieron las pruebas)
  Pygame no puede abrir ventana.
- **Solución:** para las pruebas sin ventana se usa la variable `SDL_VIDEODRIVER=dummy`
  (`SDL_VIDEODRIVER=dummy python probar_entorno.py`). En Windows con pantalla no hace falta.
  El modo `rgb_array` no abre ventana y funciona siempre.

### 5. Aviso de pip desactualizado

- **Qué pasa:** al instalar sale `[notice] A new release of pip is available: 24.0 -> 26.3`.
- **Solución:** es solo un aviso, no impide nada. Opcional: `python -m pip install --upgrade pip`.

### 6. Extraer `Entorno1.rar`

- **Qué pasa:** `7z` (p7zip) no pudo extraer el archivo: `ERROR: Unsupported Method`
  (es formato RAR5).
- **Solución:** usar WinRAR o 7-Zip actualizado en Windows; en Linux, `bsdtar -xf Entorno1.rar`.
