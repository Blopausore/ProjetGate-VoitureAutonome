#Generation de point aleatoires
import numpy as np
import random

"""
Soit d une distance moyenne entre deux points,
on considere alors un circuit place au centre 
d'un terrain de taille 100xd.
"""
def N(v):
    return sum([c for c in v])/len(v)

def generation(nb_points,dist_moy,ecart_dist,ray_moy,ecart_ray):
    points=[]
    rand_coord = lambda : np.random.uniform(0,dist_moy*100)
    rand_ray = lambda : np.random.uniform(ray_moy-ecart_ray,ray_moy+ecart_ray)
    points.append(np.array([rand_coord(),rand_coord()]))
    while len(points) != nb_points:
        point=np.array([rand_coord(),rand_coord()])
        print(points,point)
        v=points[-1]-point
        points.append((point,rand_ray()))
    return points

points=generation(10,4,3,2,1)


