
##Entree : listes de points [(x,y)] 
#%%
import numpy as np



##
#%%
a=np.array([2.,3.])
b=np.array([5.,4.])
c=np.array([5.,1.])
d=np.array([1.,1.5])
e=np.array([1.,1.])


points=[[a,1],[b,0.5],[c,1.5],[d,1],[e,0.5]]


##
#%%
def N(v):
    return sum([c for c in v])/len(v)

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

def init_alpha(a,b):#Retourne l'angle initial de la course
    v=b-a
    return np.arccos(v[0]/N(v))


def points_vers_circuit(points:list):
    if len(points) < 3 :
        print("Erreur : nombre de point insuffisant")
        exit()
    alpha0=init_alpha(points[0][0],points[1][0])
    point0=points[0]
    point1=points[1]
    circuit=[alpha0]
    for _ in range(len(points)):  
        if len(points) == 2:
            a,b,c=[c for c,_ in points[-2:]],point0[0]
            r=points[-2][1] 
        elif len(points)==1:
            a,b,c=points[-1][0],point0[0],point1[0]
            r=point0[1]
        else :
            a,b,c=[c for c,_ in points[-3:]]
            r=points[-2][1]
        alpha,h=virage(a,b,c,r)
        circuit.append(N(b-a)-h)
        circuit.append((r,alpha))
        points.pop()


    

    return circuit


# %%
