
import gym
import highway_env
from stable_baselines3 import PPO

env = gym.make("course-v0")

model = PPO.load("courselidar_ppo450000/model")    #mettre le nom du dossier qui contient le modèle

while True:
  done = truncated = False
  
  obs = env.reset()
  
  while not (done or truncated):
    action, _states = model.predict(obs, deterministic=True)
    print(action)
    obs, reward, done, info = env.step(action)        
    #print("Obs =\n",obs)
    env.render()