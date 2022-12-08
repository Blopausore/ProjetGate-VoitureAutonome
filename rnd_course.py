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
import random
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


class rnd_course(AbstractEnv):

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
                "type": "LidarObservation", #LidarObservation Kinematics
                "maximum_range": [50],
                "as_image": False,
                "align_to_vehicle_axes": True,
                "cells": 256
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
            "action_reward": 0,  #-0.3
            "controlled_vehicles": 1,
            "other_vehicles": 1,
            "screen_width": 600,
            "screen_height": 600,
            "centering_position": [0.5, 0.5],
        })
        return config

    def _reward(self, action: np.ndarray) -> float:
        _, lateral = self.vehicle.lane.local_coordinates(self.vehicle.position)
        lane_centering_reward = 1/(1+self.config["lane_centering_cost"]*lateral**2)
        action_reward = self.config["action_reward"]*np.linalg.norm(action)
        reward = lane_centering_reward \
            + action_reward \
            + self.config["collision_reward"] * self.vehicle.crashed
        reward = reward if self.vehicle.on_road else self.config["collision_reward"]
        return utils.lmap(reward, [self.config["collision_reward"], 1], [0, 1])

    def _is_terminal(self) -> bool:
        """The episode is over when a collision occurs or when the access ramp has been passed."""
        return self.vehicle.crashed or self.time >= self.config["duration"]

    def _reset(self) -> None:
        self._make_road()
        self._make_vehicles()
    
    '''
    def _make_road(self) -> None:     #génère la route
        net = RoadNetwork() #annonce la génération d'un réseau de route, initialement vide
        speedlimits = [None,2,2,2] #définit la vitesse max dans chaque section (je pense qu'on pourra mettre un très grand nombre après un minimum d'entrainement de l'ia)
        reScale = lambda x,s: x * s
        def mod_pi(angle):
            if angle > np.pi :
                return mod_pi(angle-2*np.pi)
            elif angle < -np.pi :
                return mod_pi(angle+2*np.pi)
            else :
                return angle
        V = lambda angle : np.array([np.cos(angle),-np.sin(angle),0.])
        signe=lambda x: x/abs(x) if x!=0 else 0
        def ligne(X,long,alpha):
            Y=X+long*V(alpha)[:2]
            return Y

        def arc(X,alpha,rayon,beta):
            Z = np.array([0,0,1])
            Xe = np.array([X[0],X[1],0.])
            U = V(alpha)
            C = Xe + rayon * np.cross(U, Z*signe(beta) )
            T = C[:2] - np.array([rayon,rayon])

            alpha = mod_pi(alpha+beta)
            Y = C[:2] + rayon*V(alpha-signe(beta)*np.pi/2)[:2]

            return  C[:2],Y,alpha

        def cheminroute(self, liste):
            precedent= np.array([0,0])
            alpha=liste[0]
            for i in range(1,len(liste)-1):
                debut,fin = chr(i+96), chr(i+97)
                if type(liste[i]) == float :
                    suivant = ligne(precedent,reScale(liste[i],10.),alpha)
                    net.add_lane(debut, fin, StraightLane(precedent, suivant, line_types=(LineType.CONTINUOUS, LineType.NONE), width=15, speed_limit=speedlimits[1]))
                    net.add_lane(debut, fin, StraightLane(precedent, suivant, line_types=(LineType.STRIPED, LineType.CONTINUOUS), width=15, speed_limit=speedlimits[1]))
                    precedent = suivant
                else:
                    rayon,beta = reScale(liste[i][0],10.),liste[i][1]
                    c,precedent,beta = arc(precedent,alpha,rayon,beta)
                    net.add_lane(debut, fin,
                                CircularLane(c, rayon, alpha, beta, width=15,
                                            clockwise=False, line_types=(LineType.CONTINUOUS, LineType.NONE),
                                            speed_limit=speedlimits[2]))
                    net.add_lane(debut, fin,
                                CircularLane(c, rayon, alpha, beta, width=15,
                                            clockwise=False, line_types=(LineType.STRIPED, LineType.CONTINUOUS),
                                            speed_limit=speedlimits[2]))
                    alpha=beta
            net.add_lane(fin, 'a', StraightLane(suivant, liste[-1], line_types=(LineType.CONTINUOUS, LineType.NONE), width=15, speed_limit=speedlimits[1]))
            net.add_lane(fin, 'a', StraightLane(suivant, liste[-1], line_types=(LineType.STRIPED, LineType.CONTINUOUS), width=15, speed_limit=speedlimits[1]))
            road = Road(network=net, np_random=self.np_random, record_history=self.config["show_trajectories"])
 
            return road #applique la création de la route


        self.road = cheminroute(self,[0.3217505543966423,2.7225148226554414,(0.2, 1.892546881191539),3.5,(0.5, 1.5707963267948966),3.8381966011250106,(0.1, 2.0344439357957027),2.0289611963132423,(0.5, 0.7853981633974484)])
        

        
    '''
    def _make_road(self):
        angltot = 90
        debut = (100, -50)
        precedent,suivant = 96,97
        alpha = 0
        net = RoadNetwork()#annonce la génération d'un réseau de route, initialement vide
        speedlimits = [None,10,10,10] #définit la vitesse max dans chaque section (je pense qu'on pourra mettre un très grand nombre après un minimum d'entrainement de l'ia)
        fin = (0,0)
        correc = True
        while angltot > -180:
            
            
            precedent,suivant=precedent+1,suivant+1
            
            
            if random.random() > 0.5:
                x = int(random.random()*20+5)
                augx,augy = np.cos(angltot*2 * np.pi/360 - np.pi/2) , np.sin(angltot*2*np.pi/360 -np.pi/2)
                fin = (debut[0]+ x*augx,debut[1] + x*augy)
                if fin[1] > -50 :
                    #print("route droite")
                    correc = False
                    break
                    
                else:
                    net.add_lane(chr(precedent), chr(suivant), StraightLane(debut, fin, line_types=(LineType.CONTINUOUS, LineType.NONE), width=10, speed_limit=speedlimits[1]))
                    net.add_lane(chr(precedent), chr(suivant), StraightLane(debut, fin, line_types=(LineType.STRIPED, LineType.CONTINUOUS), width=10, speed_limit=speedlimits[1]))
                    debut= (fin[0] , fin[1] )


            else:
                x = int(random.random()*50+5)
                augx,augy = np.cos(angltot*2 * np.pi/360) , np.sin(angltot*2*np.pi/360)
                c = (debut[0]- x*augx ,debut[1] - x*augy)

                rayon = ((c[0]-debut[0])**2 + (c[1]-debut[1])**2 ) ** 0.5
                beta = - random.random() * (min((270 + angltot), 90))
                verif = (c[0]+np.cos((angltot+beta)*2*np.pi/360)*rayon ,c[1] + np.sin((angltot+beta)*2*np.pi/360)*rayon)
                distdebfin= ((verif[0]- 100)**2 + (verif[1] + 50)**2)**0.5
                correction=np.arccos((verif[1]+50)/distdebfin) *360/(2*np.pi) - angltot-beta -360
                #print("debut: " , debut , "  verif: " , verif)
                #print("correction: " , correction)
                #print(np.arccos((verif[1]+50)/distdebfin) , (verif[1]+50)/distdebfin) 
                #""""((((((((((((((((((((((((((((((()))))))))))))))))))))))))))))))
                if correction > 0:
                    
                    correc = False
                    #print("pb angle")
                    break
                    
                elif verif[1] > -50 : 
                    correc = False
                
                    #print("pb atteindre")
                    break
                else:
                    net.add_lane(chr(precedent), chr(suivant),
                                    CircularLane(c, rayon, np.deg2rad(angltot), np.deg2rad(angltot +beta), width=10,
                                                clockwise=False, line_types=(LineType.CONTINUOUS, LineType.NONE),
                                                speed_limit=speedlimits[2]))
                    net.add_lane(chr(precedent), chr(suivant),
                                    CircularLane(c, rayon, np.deg2rad(angltot), np.deg2rad(angltot+beta), width=10,
                                                clockwise=False, line_types=(LineType.STRIPED, LineType.CONTINUOUS),
                                                speed_limit=speedlimits[2]))
                angltot += beta
                debut = (c[0]+np.cos(angltot*2*np.pi/360)*rayon ,c[1] + np.sin(angltot*2*np.pi/360)*rayon)

        x = int(random.random()*50+5)
        augx,augy = np.cos(angltot*2 * np.pi/360) , np.sin(angltot*2*np.pi/360)
        c = (debut[0]- x*augx ,debut[1] - x*augy)

        rayon = ((c[0]-debut[0])**2 + (c[1]-debut[1])**2 ) ** 0.5
        beta = - random.random() * (min((270 + angltot), 90))
        verif = (c[0]+np.cos((angltot+beta)*2*np.pi/360)*rayon ,c[1] + np.sin((angltot+beta)*2*np.pi/360)*rayon)
        distdebfin= ((verif[0]- 100)**2 + (verif[1] + 50)**2)**0.5
        correction=np.arccos((verif[1]+50)/distdebfin) *360/(2*np.pi) - angltot-beta -360
        yfin = np.sin(angltot*2*np.pi/360 - np.pi/2)* (100 - fin[0])/np.cos(angltot*2*np.pi/360 - np.pi/2) + fin[1]
        c = ( 100, yfin)
        rayon = abs(yfin +50)
                    #print(c , rayon)
                    #dist = ((debut[0]- c[0])**2 + (debut[1] - c[1])**2)**0.5
        fin = ( debut[0] + np.cos(angltot*2 * np.pi/360 - np.pi/2)* (-50 - debut[1])/np.sin(angltot*2 * np.pi/360 - np.pi/2) , -57.5)
                    #print(fin)
        minu,maxu = min(np.deg2rad(angltot) , np.deg2rad(-270)) ,max(np.deg2rad(angltot) , np.deg2rad(-270))
        
        net.add_lane(chr(precedent), chr(suivant), StraightLane(debut, fin, line_types=(LineType.CONTINUOUS, LineType.NONE), width=10, speed_limit=speedlimits[1]))
        net.add_lane(chr(precedent), chr(suivant), StraightLane(debut, fin, line_types=(LineType.STRIPED, LineType.CONTINUOUS), width=10, speed_limit=speedlimits[1]))
        c=(fin[0] - 7.5*augx, fin[1] - 7.5 * augy)
        net.add_lane(chr(suivant), chr(suivant + 1),
                                    CircularLane(c, 7.5, maxu, minu , width=10,
                                                clockwise=False, line_types=(LineType.CONTINUOUS, LineType.NONE),
                                                speed_limit=speedlimits[2]))
        net.add_lane(chr(suivant), chr(suivant + 1),
                                    CircularLane(c, 7.5, maxu , minu , width=10,
                                                clockwise=False, line_types=(LineType.STRIPED, LineType.CONTINUOUS),
                                                speed_limit=speedlimits[2]))
        fin = (c[0] ,c[1] + 7.5)
        net.add_lane(chr(suivant + 1), 'a', StraightLane(fin, (100, -50), line_types=(LineType.CONTINUOUS, LineType.NONE), width=10, speed_limit=speedlimits[1]))
        net.add_lane(chr(suivant + 1), 'a', StraightLane(fin, (100 , -50), line_types=(LineType.STRIPED, LineType.CONTINUOUS), width=10, speed_limit=speedlimits[1]))

        #net.add_lane(chr(suivant), 'a', StraightLane(fin, (100, -50), line_types=(LineType.CONTINUOUS, LineType.NONE), width=15, speed_limit=speedlimits[1]))
        #net.add_lane(chr(suivant), 'a', StraightLane(fin, (100, -50), line_types=(LineType.STRIPED, LineType.CONTINUOUS), width=15, speed_limit=speedlimits[1]))
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
            lane_index = ("a", "b", rng.randint(2)) if i == 0 else \
                self.road.network.random_lane_index(rng)
            controlled_vehicle = self.action_type.vehicle_class.make_on_lane(self.road, lane_index, speed=None,
                                                                             longitudinal=rng.uniform(20, 50))

            self.controlled_vehicles.append(controlled_vehicle)
            self.road.vehicles.append(controlled_vehicle)


        """véhicules rajoutable, à voir une fois qu'on a un peu entrainné l'ia"""
        # Front vehicle
        #vehicle = IDMVehicle.make_on_lane(self.road, ("a", "b", lane_index[-1]),
         #                                  longitudinal=rng.uniform(
          #                                     low=0,
           #                                    high=self.road.network.get_lane(("a", "b", 0)).length
            #                               ),
             #                              speed=6+rng.uniform(high=3))
        #self.road.vehicles.append(vehicle)

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
    id='rnd_course-v0',
    entry_point='highway_env.envs:rnd_course',
)

















