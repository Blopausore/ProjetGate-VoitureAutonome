# Créé par TCONTRI, le 12/10/2022 en Python 3.7
import pygame
import math

pygame.init()

#Création de la fenêtre de taille h * w
h = 750
w = 750
fenetre = pygame.display.set_mode((w, h)) #Le (0,0) se situe en haut à gauche
fenetre.fill((255,255,255)) #Couleur fond de la fenetre
#Nom de la fenetre
pygame.display.set_caption('Projet_GATE Voitures_Automes Générations_Circuits')
boucle = True
L=[1.5,50.0,(20,-1.5),20.0,(30,-1),50.0,(20,-0.5),20.0,(30,-0.5)] #Liste représentant le circuit courant
###Pour la version finale la liste ci-dessus devra être initialisée comme étant vide###
while boucle :
    #Police du texte
    police = pygame.font.SysFont("monospace", 20)
    #Bouton de génération de circuit
    rect_gene = pygame.Rect((50, 650), (150,50))
    pygame.draw.rect(fenetre, (100,100,255), rect_gene)
    txt_gene = police.render("Génération",1,(0,0,0))
    fenetre.blit(txt_gene,(65,665))
    #Bouton de sauvegarde de circuit
    rect_save = pygame.Rect((550, 650), (150,50))
    pygame.draw.rect(fenetre, (100,255,100), rect_save)
    txt_gene = police.render("Sauvegarde",1,(0,0,0))
    fenetre.blit(txt_gene,(565,665))
    #Coordonnées courantes de la souris
    x,y = pygame.mouse.get_pos()
    pygame.display.update()
    for event in pygame.event.get():
        if event.type == pygame.QUIT: #Permet de fermer la fenetre si demandé
            boucle = False
        elif (event.type == pygame.MOUSEBUTTONDOWN) and (50 <= x <= 200) and (650 <= y <= 700) : #Génération + affichage d'un circuit
            '''L = ''' ###Appelle de la fonction d'Augustin pour obtenir la liste représentant le circuit généré###
            print('Génération')
            fenetre.fill((255,255,255)) #Permet de réinitialiser le tracer
            #Ce qui suis correspond à l'affichage du tracé courant
            (x1, y1) = (375,300) #Coordonnées actuelles
            alpha1 = L[0] #Angle actuelle
            for donne in L[1:]:
                if type(donne) == float : #Cas on est sur une portion de ligne droite
                    x2 = x1
                    y2 = y1
                    x2 += float(donne * math.cos(alpha1))
                    y2 -= float(donne * math.sin(alpha1))
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
        elif (event.type == pygame.MOUSEBUTTONDOWN) and (550 <= x <= 700) and (650 <= y <= 700): #Sauvegarde du circuit dans le fichier txt (si possible)
            if L == [] :
                print('Sauvegarde impossible : aucun circuit généré')
            else :
                with open("Circuit_sauvegardés", "a") as f:
                    f.write(str(L) + "\n")
                    L = []
                    fenetre.fill((255,255,255)) #Permet de réinitialiser le tracer
pygame.quit()
