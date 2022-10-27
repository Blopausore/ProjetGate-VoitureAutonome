#https://highway-env.readthedocs.io/en/latest/quickstart.html#training-an-agent


import gym
import highway_env
from stable_baselines3 import DQN

nb_steps = 2000

dossier_sauvegarde = "highway_dqn" + str(nb_steps) + "/"

env = gym.make("highway-fast-v0")
model = DQN('MlpPolicy', env,
              policy_kwargs=dict(net_arch=[256, 256]),
              learning_rate=5e-4,
              buffer_size=15000,
              learning_starts=200,
              batch_size=32,
              gamma=0.8,
              train_freq=1,
              gradient_steps=1,
              target_update_interval=50,
              verbose=1,
              tensorboard_log=dossier_sauvegarde)
model.learn(int(nb_steps))
model.save(dossier_sauvegarde + "model")

# Load and test saved model
model = DQN.load(dossier_sauvegarde + "model")
while True:
  done = truncated = False
  a = env.reset()
  #print("\n\na= ",a)
  obs = a
  while not (done or truncated):
    action, _states = model.predict(obs, deterministic=True)
    #print(action)
    obs, reward, done, info = env.step(int(action))              #,truncated
    env.render()

