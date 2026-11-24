"""
Paquete del entorno HouseKeeper-v0.

Al importar este paquete se registra el entorno en Gymnasium, así se puede crear con:
    import gymnasium as gym
    import housekeeper_env
    env = gym.make("HouseKeeper-v0", grid_size=8, render_mode="human")
"""

from gymnasium.envs.registration import register

from housekeeper_env.house_env import HouseKeeperEnv

register(
    id="HouseKeeper-v0",
    entry_point="housekeeper_env.house_env:HouseKeeperEnv",
    # No ponemos max_episode_steps: el propio entorno corta por pasos (truncated)
)
