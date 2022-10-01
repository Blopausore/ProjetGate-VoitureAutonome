import random, numpy as np


def distance(pointA,pointB):
    return ((pointA[0]-pointB[0])**2+(pointA[1]-pointB[1])**2)**0.5

def distance_min(point, liste_points):
    dmin = float("inf")
    for pt in liste_points:
        d = distance(point,pt)
        if d<dmin:
            dmin = d
    return dmin


def generation():
    """renvoie la liste des points avec le cercle qui les entoure sous
    la forme l = [ [np.array([x,y]),rayon], ... ]"""

    N = 100
    #taille du plateau

    nb_pts_par_region = 2
    #2 points par région
    #4 régions
    #donc 8 points au total

    espacement = N/4
    #distance minimale autorisée entre 2 points

    liste_points = []

    for decalage_x in (0,N/2):
        for decalage_y in (0,N/2):
            for p in range(nb_pts_par_region):
                initialisation = True
                while initialisation or distance_min(point, liste_points) < espacement:
                    initialisation = False
                    x = random.uniform(decalage_x,decalage_x + N/2)
                    y = random.uniform(decalage_y,decalage_y + N/2)
                    point = (x,y)
                liste_points.append(point)

    for i in range(len(liste_points)):
        rayon = random.uniform(espacement/4,espacement/2)
        liste_points[i] = [np.array(liste_points[i]), rayon]

    return liste_points
