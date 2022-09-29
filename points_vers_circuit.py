#Entree : listes de points [(x,y)] 
import numpy as np

a=np.array([2.,3.])
b=np.array([5.,4.])
c=np.array([5.,1.])

def N(v):
    return sum([c for c in v])

def rad_to_deg(r):
    return r*180/np.pi

def virage(a,b,c,r): 
    """
    ENTREE :
        a,b,c : numpy array
            Trois poins qui composent un virage
        r : int
            Rayon du cercle
        
    SORTIE :
        alpha : int
            Angle effectuer durant le virage
        h : int
            Distance avant b a laquelle le virage debute
    """
    v1,v2=b-a,c-b
    cos_alpha=np.dot(v1,v2)/(N(v1)*N(v2))
    alpha=np.arccos(cos_alpha)
    h = r*np.tan(alpha/2)
    return alpha,h


alpha,h=virage(a,b,c,1)
print(h,rad_to_deg(alpha))


def points_vers_circuit(points:list):
    if len(points) < 3 :
        print("Erreur : nombre de point insuffisant")
        exit()
    a,b,c=point[:2]
    alpha=np.arccos()




