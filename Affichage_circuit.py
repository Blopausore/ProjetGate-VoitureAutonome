import pygame
import math

pygame.init()

L=[1.5,50,(20,-1.5),20,(30,-1),50,(20,-0.5),20,(30,-0.5)] #Liste test

def TraceDeCircuit(L):
    '''Trace le circuit à partir de la liste fournie'''
    #Création de la fenêtre de taille h * w
    h = 1000
    w = 1000
    fenetre = pygame.display.set_mode((w, h)) #Le (0,0) se situe en haut à gauche
    fenetre.fill((255,255,255)) #Couleur fond de la fenetre
    boucle = True
    while boucle :
        (x1, y1) = (500,500) #Coordonnées actuelles
        alpha1 = L[0] #Angle actuelle
        for donne in L[1:]:
            if type(donne) == int : #Cas on est sur une portion de ligne droite
                x2 = x1
                y2 = y1
                x2 += int(donne * math.cos(alpha1))
                y2 -= int(donne * math.sin(alpha1))
                pygame.draw.line(fenetre, (255, 0, 255), (x1, y1), (x2, y2)) #Trace la ligne sur la fenetre entre les coord (x1, y1) et (x2, y2) (couleur en RGB)
                x1 = x2
                y1 = y2
            else : #Cas on est sur un virage
                (r, angle) = donne
                if angle > 0 :
                    direction = 'Gauche' #Direction correspond au sens dans lequel on prend le virage
                else :
                    direction = 'Droite'
                alpha2 = alpha1 + angle
                x0 = x1 - r * (1 - math.cos(math.pi - alpha1))
                y0 = y1 - r * (1 - math.sin(math.pi - alpha1))
                rect = pygame.Rect((x0, y0), (2*r, 2*r)) #Rectangle (carré pour notre cas) dans lequel le cercle du virage sera inscrit (x0, y0) coord en haut gauche r : largeur/hauteur
                if direction == 'Droite' :
                    pygame.draw.arc(fenetre, (255, 0, 255), rect, alpha2, alpha1)
                elif direction == 'Gauche' :
                    pygame.draw.arc(fenetre, (255, 0, 255), rect, alpha1, alpha2)
                alpha1 = alpha2
                x1 = x0 + r + r*math.cos(alpha2)
                y1 = y0 + r - r*math.sin(alpha2)
        #Permet de fermer la fenetre si demandé
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                boucle = False
        pygame.display.update()
    pygame.quit()



