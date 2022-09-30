
##Entree : listes de points [(x,y)] 
#%%
import numpy as np




a=np.array([2.,3.])
b=np.array([5.,4.])
c=np.array([5.,1.])
d=np.array([1.,1.])


points=[[a,0.5],[b,0.2],[c,0.5],[d,0.1]]



def N(v):
    return np.sqrt(sum([c**2 for c in v]))

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

def alpha(v1,v2):
    return np.arccos(np.dot(v1,v2)/(N(v1)*N(v2)))

def points_vers_circuit(points:list):
    if len(points) < 3 :
        print("Erreur : nombre de point insuffisant")
        exit()

    circuit=[alpha(points[1][0]-points[0][0],np.array([1,0]))]

    def update_circuit(a,b,c,r):
        alpha,h=virage(a,b,c,r)
        circuit.append(N(b-a)-h)
        circuit.append((r,alpha))

    for i in range(len(points)-2):  
        c,b,a=[c for c,_ in points[i:i+3]]
        r=points[i+1][1]
        update_circuit(a,b,c,r)
    #Debut bouclage
    a,b,c=points[-2][0],points[-1][0],points[0][0]
    r=points[-1][1] 
    update_circuit(a,b,c,r)
    #Fin bouclage
    a,b,c=points[-1][0],points[0][0],points[1][0]
    r=points[0][1]
    update_circuit(a,b,c,r)

    return circuit


# %%
