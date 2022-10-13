
##Entree : listes de points [(x,y)] 
#%%
import numpy as np


def N(v):
    return np.sqrt(sum([c**2 for c in v]))

def rad_to_deg(r):
    return r*180/np.pi

signe=lambda x: x/abs(x) if x!=0 else 0


rot90=np.array([[0.,1],[-1.,0]])

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
    sens=signe(np.dot(np.dot(rot90,v1),v2)) #positif <-> gauche ; negatif <-> droite
    alpha=np.arccos(cos_alpha)
    h = r/np.tan(alpha/2)
    return sens*(np.pi-alpha),h


def alpha(v1,v2):
    return np.arccos(np.dot(v1,v2)/(N(v1)*N(v2)))


def points_vers_circuit(points:list):
    if len(points) < 3 :
        print("Erreur : nombre de point insuffisant")
        exit()

    """
    Initialisation du circuit : angle de depart et 0
    Ce 0 sert a la conception de circuit, il permet de retirer une 
    longueur non parcouru par les droites.
    """
    v,e=points[1][0]-points[0][0],np.array([1,0])
    alpha0=np.arccos(np.dot(v,e)/(N(v)*N(e)))
    circuit=[alpha0,0]


    def update_circuit(a,b,c,r):
        beta,h=virage(a,b,c,r)
        circuit.append(max(N(b-a)-h-circuit.pop(),0))
        circuit.append((r,beta))
        circuit.append(h) 

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
    circuit[1]-=circuit.pop()
    return circuit

    

if __name__=="__main__":
    e=10
    
    a=e*np.array([2.,3.])
    b=e*np.array([5.,4.])
    c=e*np.array([5.,1.])
    d=e*np.array([3.,1.5])
    e=e*np.array([1.,1.])


    points=[[a,1],[b,2],[c,5],[d,1],[e,1]]


    alpha,h=virage(a,b,c,1)
    print(h,rad_to_deg(alpha))
    circuit=points_vers_circuit(points)
    for data in circuit:
        if type(data) == tuple:
            if not -np.pi<=data[1]<=np.pi:
                print("ahhhh",data[0])



# %%
