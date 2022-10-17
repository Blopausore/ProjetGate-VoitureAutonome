"""fichier à placer dans highway-env-master\highway_env\envs, il définit le chemin, les caractérisques de l'apprentissage, ses mouvements, et le nom de la course

À FAIRE : rajouter: 'from highway_env.envs.course import *' dans highway-env-master\highway_env\envs\__init__.py
À FAIRE : rajouter: 'from highway_env.envs.course import *' dans highway-env-master\highway_env\envs\__init__.py
À FAIRE : rajouter: 'from highway_env.envs.course import *' dans highway-env-master\highway_env\envs\__init__.py
À FAIRE : rajouter: 'from highway_env.envs.course import *' dans highway-env-master\highway_env\envs\__init__.py
À FAIRE : rajouter: 'from highway_env.envs.course import *' dans highway-env-master\highway_env\envs\__init__.py
(déso pr le spam mais sinon ça marche pas)
"""



import numpy as np
from gym.envs.registration import register

from highway_env import utils
from highway_env.envs.common.abstract import AbstractEnv
from highway_env.envs.common.action import Action
from highway_env.road.road import Road, RoadNetwork
from highway_env.utils import near_split
from highway_env.vehicle.controller import ControlledVehicle
from highway_env.vehicle.kinematics import Vehicle


from itertools import repeat, product
from typing import Tuple, Dict, Text



from highway_env.road.lane import LineType, StraightLane, CircularLane, SineLane

from highway_env.vehicle.behavior import IDMVehicle


Observation = np.ndarray


class course(AbstractEnv):

    """
    A continuous control environment.

    The agent needs to learn two skills:
    - follow the tracks
    - avoid collisions with other vehicles

    Credits and many thanks to @supperted825 for the idea and initial implementation.
    See https://github.com/eleurent/highway-env/issues/231
    """

    @classmethod
    def default_config(cls) -> dict:       #définit toutes les variables régissant l'environement (tout est détaillé sur https://highway-env.readthedocs.io/en/latest/quickstart.html)
        config = super().default_config()
        config.update({#gère les caractéristiques, hors chemin, du circuit (les noms des variables sont assez explicites)
            "observation": {
                "type": "OccupancyGrid",
                "features": ['presence', 'on_road'],
                "grid_size": [[-18, 18], [-18, 18]],
                "grid_step": [3, 3],
                "as_image": False,
                "align_to_vehicle_axes": True
            },
            "action": {
                "type": "ContinuousAction",#classe qui gère les mvts dans le fichier highway-env-master\highway_env\envs\common\action.py
                "longitudinal": False,
                "lateral": True,
                "target_speeds": [0, 5, 10]
            },
            "simulation_frequency": 15,
            "policy_frequency": 5,
            "duration": 300,
            "collision_reward": -1,
            "lane_centering_cost": 4,
            "lane_centering_reward": 1,
            "action_reward": -0.3,
            "controlled_vehicles": 1,
            "other_vehicles": 1,
            "screen_width": 600,
            "screen_height": 600,
            "centering_position": [0.5, 0.5],
        })
        return config

    def _reward(self, action: np.ndarray) -> float:
        rewards = self._rewards(action)
        reward = sum(self.config.get(name, 0) * reward for name, reward in rewards.items())
        reward = utils.lmap(reward, [self.config["collision_reward"], 1], [0, 1])
        reward *= rewards["on_road_reward"]
        return reward

    def _rewards(self, action: np.ndarray) -> Dict[Text, float]:
        _, lateral = self.vehicle.lane.local_coordinates(self.vehicle.position)
        return {
            "lane_centering_reward": 1/(1+self.config["lane_centering_cost"]*lateral**2),
            "action_reward": np.linalg.norm(action),
            "collision_reward": self.vehicle.crashed,
            "on_road_reward": self.vehicle.on_road,
        }

    def _is_terminated(self) -> bool:               #arrete la simul si le véhicule en heurte un autre
        return self.vehicle.crashed

    def _is_truncated(self) -> bool:
        return self.time >= self.config["duration"]

    def _reset(self) -> None:       #met à jour la simulation(génère le terrain et les véhicules
        self._make_road()
        self._make_vehicles()

    def _make_road(self) -> None:     #génère la route
        net = RoadNetwork() #annonce la génération d'un réseau de route, initialement vide
        speedlimits = [None,10,10,10] #définit la vitesse max dans chaque section (je pense qu'on pourra mettre un très grand nombre après un minimum d'entrainement de l'ia)

        #premier demi cercle
        center1 = [100, -20]
        radii1 = 20
        net.add_lane("a", "b",
                     CircularLane(center1, radii1, np.deg2rad(90), np.deg2rad(-270), width=5,
                                  clockwise=False, line_types=(LineType.CONTINUOUS, LineType.NONE),
                                  speed_limit=speedlimits[1]))
                                  #definit 2 arc de cercle de centre center1, de radian radii1 +- width, qui va de l'angle 90° (pointe vers le bas) à -270° ATTENTION l'angle 1 doit toujours être supérieur à celui de gauche, witdh est la largeur de la route (si je comprend bien ça s'ajoute/soustrait au radian), clockwise indique le sens dans lequel on considère les angles, on choisit des lignes continues pour faire les bords, la limite sur ce tronçon est dans la variable "speedlimits"
                                  #"a" et "b" sont les indices des points de départ est d'arrivé. on ne peut, à priorit, pas les remplacer par des indices numériques
        net.add_lane("a", "b",
                     CircularLane(center1, radii1+5, np.deg2rad(90), np.deg2rad(-270), width=5,
                                  clockwise=False, line_types=(LineType.STRIPED, LineType.CONTINUOUS),
                                  speed_limit=speedlimits[1]))
                                  #definit la ligne en pointillé au centre(que l'on va surement supprimer) de la même manière



        #2eme demi cercle
        #cette section n'a rien de nouveau, n'est pas très utile, mais est OBLIGATOIRE si on ne veut pas de bug : on fait comprendre au programe que l'on ferme le circuit. Les indices de ce circuit doivent donc être "dernier_indice", "a". Par contre le chemin en lui même peut ne pas du tout rejoindre ces 2 points
        center5 = [100, -20]
        radii5 = 20
        net.add_lane("b", "a",
                     CircularLane(center5, radii5+5, np.deg2rad(90), np.deg2rad(-271), width=5,
                                  clockwise=True, line_types=(LineType.CONTINUOUS, LineType.STRIPED),
                                  speed_limit=speedlimits[2]))
        net.add_lane("b", "a",
                     CircularLane(center5, radii5, np.deg2rad(90), np.deg2rad(-271), width=5,
                                  clockwise=True, line_types=(LineType.NONE, LineType.CONTINUOUS),
                                  speed_limit=speedlimits[2]))






        road = Road(network=net, np_random=self.np_random, record_history=self.config["show_trajectories"])
        self.road = road #applique la création de la route

    def _make_vehicles(self) -> None:
        """
        Populate a road with several vehicles on the highway and on the merging lane, as well as an ego-vehicle.
        """
        rng = self.np_random

        # Controlled vehicles
        #seul ce véhicule, géré par renforcement learning, nous interesse pour l'instant
        self.controlled_vehicles = []
        for i in range(self.config["controlled_vehicles"]):
            lane_index = ("a", "b", rng.integers(2)) if i == 0  else \
                self.road.network.random_lane_index(rng) #pose le premier véhicule sur le tronçon "a","b". Si il y a d'autres véhicules ils sont sur d'autres sections randoms (pourra être interressant pour simuler une "vrai" course

            controlled_vehicle = self.action_type.vehicle_class.make_on_lane(self.road, lane_index, speed=None,
                                                                             longitudinal=rng.uniform(20, 50)) #donne les actions au véhicule

            self.controlled_vehicles.append(controlled_vehicle) #applique la crétion du véhicule
            self.road.vehicles.append(controlled_vehicle)

        """véhicules rajoutable, à voir une fois qu'on a un peu entrainné l'ia"""
        # Front vehicle
        # vehicle = IDMVehicle.make_on_lane(self.road, ("a", "b", lane_index[-1]),
        #                                   longitudinal=rng.uniform(
        #                                       low=0,
        #                                       high=self.road.network.get_lane(("a", "b", 0)).length
        #                                   ),
        #                                   speed=6+rng.uniform(high=3))
        # self.road.vehicles.append(vehicle)

        # Other vehicles
        # for i in range(rng.integers(self.config["other_vehicles"])):
        #     random_lane_index = self.road.network.random_lane_index(rng)
        #     vehicle = IDMVehicle.make_on_lane(self.road, random_lane_index,
        #                                       longitudinal=rng.uniform(
        #                                           low=0,
        #                                           high=self.road.network.get_lane(random_lane_index).length
        #                                       ),
        #                                       speed=6+rng.uniform(high=3))
        #     # Prevent early collisions
        #     for v in self.road.vehicles:
        #         if np.linalg.norm(vehicle.position - v.position) < 20:
        #             break
        #     else:
        #         self.road.vehicles.append(vehicle)













# très important: donne l'adresse de la course pour qu'on puisse l'appeller avec le module gym
register(
    id='course-v0',
    entry_point='highway_env.envs:course',
)

















