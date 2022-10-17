""" fichier à placer à la racine (dans highway-env-master), c'est celui que l'on doit executer. """



import gym
import highway_env
from matplotlib import pyplot as plt


env = gym.make('course-v0') #on indique au programme le projet que l'on veut lancer : 'course-v0' est une référence au fichier course qui définit le chemin
env.reset() #met à jour le fichier (dans course, les variable qui gèrent l'IA sont mises à jour)

for _ in range(15): #boucle qui va définir la durée de la simulation (lorsqu'on fera de vrai simulation on mettra surement un while true, ou une durée plus précise

    action = env.action_space.sample() #définit les mouvements que la voiture pourra effectuer (définies dans highway-env-master\highway_env\envs\common\action.py) j'ai fait le choix d'utiliser la classe "continuous action" car je pense que c'est le plus adapté (car il permet de s'orienter librement dans n'importe quel direction)
    obs, reward, done, truncated, info = env.step(action) #je ne l'ai pas encore étudié, mais il semble permettre de gérer les données qui permettrons d'améliorer l'IA en plus de faire avancer le véhicule
    env.render() #affiche/ actualise la simulation
