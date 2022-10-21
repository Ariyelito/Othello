
import random, sys, pygame, time, copy
from pygame.locals import *

VIDE = "VIDE"
TUILE_NOIRE = "NOIRE"
TUILE_BLANCHE = "BLANCHE"
ecran = pygame.display.set_mode((640, 640))

BLANC     = (255, 255, 255)
NOIR      = (  0,   0,   0)
VERT      = (  0, 155,   0)

def main():
    global BGIMAGE
    BGIMAGE = pygame.image.load('background.png')

    #while True:
        #if Jouerjeu() == False:
            #break
    Jouerjeu()


def Jouerjeu():

    global tour
    tableauPrincipal = getNouveauTableau()
    print(tableauPrincipal)
    

    running = True
    while running:
        # Lorsque l'utilisateur click sur le X de la fenêtre, quitter le programme
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        ecran.fill(VERT)
        razTableau(tableauPrincipal)
        dessinerTableau(tableauPrincipal)

        pygame.display.flip()
    pygame.quit()


def getNouveauTableau():
    tableau = []
    for i in range(8):
        tableau.append([VIDE] * 8)
    return tableau


def razTableau(grille):

    for x in range(8):
        for y in range(8):
            grille[x][y] = VIDE

    grille[3][3] = TUILE_BLANCHE
    grille[3][4] = TUILE_NOIRE
    grille[4][3] = TUILE_NOIRE
    grille[4][4] = TUILE_BLANCHE


def dessinerTableau(grille):



    for x in range(8):
        for y in range(8):
            centerx, centery = int(x + 50 / 2), int(y + 50 / 2)
            if grille[x][y] == TUILE_BLANCHE or grille[x][y] == TUILE_NOIRE:
                if grille[x][y] == TUILE_BLANCHE:
                    tileColor = BLANC
                else:
                    tileColor = NOIR
                pygame.draw.circle(ecran, tileColor, (centerx, centery), int(50 / 2) - 4)
           
    
           

if __name__ == '__main__':
    main()