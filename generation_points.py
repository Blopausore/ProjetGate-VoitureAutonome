
import random, numpy as np
from matplotlib import pyplot as plt


def distance(pointA,pointB):
    return ((pointA[0]-pointB[0])**2+(pointA[1]-pointB[1])**2)**0.5

def distance_min(point, liste_points):
    dmin = float("inf")
    for pt in liste_points:
        d = distance(point,pt)
        #print("\nfonction, d=",d)
        if d<dmin:
            #print("TESTTTT")
            dmin = d
    return dmin




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
                #print("\ninitialisation=",initialisation)
                initialisation = False
                x = random.uniform(decalage_x,decalage_x + N/2)
                y = random.uniform(decalage_y,decalage_y + N/2)
                point = (x,y)
                #print("\ndistmin=",distance_min(point, liste_points))
            liste_points.append(point)
    
print(liste_points)
print("\n\n",len(liste_points))


plt.figure(figsize=(N,N)) #taille du graphique


figure, axes = plt.subplots() 

for pt in liste_points:
    plt.plot(pt[0],pt[1],marker="o", color="red") #afficher le point

    rayon = random.uniform(espacement/4,espacement/2)

    cc = plt.Circle((pt[0],pt[1]), rayon ) #afficher le cercle
    axes.add_artist( cc )
 
axes.set_aspect( 1 ) 
plt.show()