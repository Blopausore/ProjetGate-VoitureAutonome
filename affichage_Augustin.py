##
#%%

import pygame


h = 1000
w = 1000
pygame.init()
fenetre = pygame.display.set_mode((w, h)) #Le (0,0) se situe en haut à gauche
fenetre.fill((255,255,255)) #Couleur fond de la fenetre

import numpy as np
N = lambda v: np.sqrt(sum([c**2 for c in v]))
Z=np.array([0,0,1])

A=np.array([150.,50.,0])
X=np.array([200,200,0])

U=X-A
Ex=np.array([1.,0.,0.])
alpha=np.arccos( (U @ Ex)/N(U) )


def arc(X,alpha,rayon,beta):
    Xe = np.array([X[0],X[1],0.])
    U = np.array([np.cos(alpha),-np.sin(alpha),0.])
    Y = rayon*np.cross(U,Z)
    C = Xe + Y
    pygame.draw.line(fenetre,(255,0,255),X[:2],C[:2])
arc(X,alpha,10,100)

Y=np.cross(U,Z)

pygame.draw.line(fenetre, (0, 0, 255), X[:2], A[:2])
#pygame.draw.line(fenetre, (0, 0, 255), X[:2], X[:2]+Y[:2])


rectangle=pygame.Rect((200,200),(500,500))
pygame.draw.arc(fenetre,(255, 0, 255), rectangle, 0,np.pi/2)
pygame.display.update()


# %%

import numpy as np
import pygame

pygame.init()


h = 1000
w = 2000
fenetre = pygame.display.set_mode((w, h)) #Le (0,0) se situe en haut à gauche
fenetre.fill((255,255,255)) #Couleur fond de la fenetre

N = lambda v: np.sqrt(sum([c**2 for c in v]))
Z = np.array([0,0,1])

V = lambda angle : np.array([np.cos(angle),-np.sin(angle),0.])

couleur_circuit = (255,0,255)
couleur_construction = (0,0,255)

signe=lambda x: x/abs(x) if x!=0 else 0

def mod_pi(angle):
    if angle > np.pi :
        return mod_pi(angle-2*np.pi)
    elif angle < -np.pi :
        return mod_pi(angle+2*np.pi)
    else :
        return angle


def arc(X,alpha,rayon,beta):
    Xe = np.array([X[0],X[1],0.])
    U = V(alpha)
    C = Xe + rayon * np.cross(U, Z*signe(beta) )
    T = C[:2] - np.array([rayon,rayon])

    pygame.draw.line(fenetre,couleur_construction,X,C[:2])

    carre_inscrit = pygame.Rect(T,(2*rayon,2*rayon))
    pygame.draw.arc(fenetre,(255,0,255),carre_inscrit,0,2*np.pi)

    alpha = mod_pi(alpha+beta)
    Y = C[:2] + rayon*V(alpha-signe(beta)*np.pi/2)[:2]

    return  Y,alpha


def ligne(X,long,alpha):
    Y=X+long*V(alpha)[:2]
    pygame.draw.line(fenetre,couleur_circuit,X,Y)
    return Y



def TraceDeCircuit(L):
    '''Trace le circuit à partir de la liste fournie'''
    #Création de la fenêtre de taille h * w
    reScale = lambda x,s: x * s
    s=10.
    boucle = True

    while boucle:
        X=np.array([500,500]) #Coords du pointeur au debut
        alpha=L[0]
        for move in L[1:]:
            if type(move) in (int,float):
                X = ligne(X,reScale(move,s),alpha)
            else : 
                rayon,beta = reScale(move[0],s),move[1]
                X,alpha = arc(X,alpha,rayon,beta)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                boucle = False
        pygame.display.update()
    pygame.quit()



if __name__ == "__main__":
    L1=[0.3217505543966423,
    26.14426799751465,
    (2, -1.2490457723982542),
    15.270127655953976,
    (5, -1.3258176636680323),
    12.711646096066232,
    (1, 2.6516353273360647),
    16.155593205617894,
    (1, 0.8621700546672266),
    19.48653129015439,
    (1, 2.356194490192345)]

    TraceDeCircuit(L1)

# %%
