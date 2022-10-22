
import random, sys, pygame, time, copy
from pygame.locals import *

tour = ' '
VIDE = "VIDE"
TUILE_NOIRE = "NOIRE"
TUILE_BLANCHE = "BLANCHE"

ecran = pygame.display.set_mode((640, 640))

BLANC     = (255, 255, 255)
NOIR      = (  0,   0,   0)
VERT      = (  0, 155,   0)

def main():
    global BGIMAGE,FONT, MAINCLOCK
    pygame.init()
    
    MAINCLOCK = pygame.time.Clock()
    BGIMAGE = pygame.image.load('background.png')
    FONT = pygame.font.Font('freesansbold.ttf', 16)

    while True:
        if Jouerjeu() == False:
            break


def Jouerjeu():

    global tour
    tableauPrincipal = getNouveauTableau()
    print(tableauPrincipal)
    
    razTableau(tableauPrincipal)
    dessinerTableau(tableauPrincipal)
    
    tuileJoueur, tuileOrdi = qui_commence()

    newGameSurf = FONT.render('Nouvelle Partie', True, BLANC, VERT)
    newGameRect = newGameSurf.get_rect()
    newGameRect.topright = (640 - 8, 10)

    while True:
        if tour == 'joueur': 
            if getMouvementValide(tableauPrincipal, tuileJoueur) == []:     
                break
            movexy = None
            while movexy == None:

                boardToDraw = tableauPrincipal
                checkForQuit()
                for event in pygame.event.get(): 
                    if event.type == MOUSEBUTTONUP:
                        mousex, mousey = event.pos
                        if newGameRect.collidepoint( (mousex, mousey) ):
                            return True
                        movexy = getPosition(mousex, mousey)
                        if movexy != None and not isValidMove(tableauPrincipal, tuileJoueur, movexy[0], movexy[1]):
                            movexy = None

                dessinerTableau(tableauPrincipal)
                ecran.blit(newGameSurf, newGameRect)
                MAINCLOCK.tick(60)
                pygame.display.update()
            
            #makeMove(tableauPrincipal, tuileJoueur, movexy[0], movexy[1], True)
            if getMouvementValide(tableauPrincipal, tuileOrdi) != []:
                tour = 'ordi'


def getNouveauTableau():
    tableau = []
    for i in range(8):
        tableau.append([VIDE] * 8)
    return tableau


def getMouvementValide(grille, tuile):
    validMoves = []
    for x in range(8):
        for y in range(8):
            if isValidMove(grille, tuile, x, y) != False:
                validMoves.append((x, y))
    return validMoves


def isValidMove(grille, tuile, x, y):
   
    if grille[x][y] != VIDE or not isOnBoard(x, y):
        return False

    grille[x][y] = tuile 

    if tuile == TUILE_BLANCHE:
        autreTuile = TUILE_NOIRE
    else:
        autreTuile = TUILE_BLANCHE

    tuileAretourner = []
   
    for xdirection, ydirection in [[0, 1], [1, 1], [1, 0], [1, -1], [0, -1], [-1, -1], [-1, 0], [-1, 1]]:
        x, y = x, y
        x += xdirection
        y += ydirection
        if isOnBoard(x, y) and grille[x][y] == autreTuile:
           
            x += xdirection
            y += ydirection
            if not isOnBoard(x, y):
                continue
            while grille[x][y] == autreTuile:
                x += xdirection
                y += ydirection
                if not isOnBoard(x, y):
                    break 
            if not isOnBoard(x, y):
                continue
            if grille[x][y] == tuile:
                
                while True:
                    x -= xdirection
                    y -= ydirection
                    if x == x and y == y:
                        break
                    tuileAretourner.append([x, y])

    grille[x][y] = VIDE 
    if len(tuileAretourner) == 0: 
        return False

    return tuileAretourner


def isOnBoard(x, y):
    return x >= 0 and x < 8 and y >= 0 and y < 8


def razTableau(grille):

    for x in range(8):
        for y in range(8):
            grille[x][y] = VIDE

    grille[3][3] = TUILE_BLANCHE
    grille[3][4] = TUILE_NOIRE
    grille[4][3] = TUILE_NOIRE
    grille[4][4] = TUILE_BLANCHE


def dessinerTableau(grille):

    ecran.blit(BGIMAGE, BGIMAGE.get_rect())

    for x in range(8 + 1):

        startx = (x * 50) + 120
        starty = 120
        endx = (x * 50) + 120
        endy = 120 + (8 * 50)
        pygame.draw.line(ecran, NOIR, (startx, starty), (endx, endy))

    for y in range(8 + 1):

        startx = 120
        starty = (y * 50) + 120
        endx = 120 + (8 * 50)
        endy = (y * 50) + 120
        pygame.draw.line(ecran, NOIR, (startx, starty), (endx, endy))


    for x in range(8):
        for y in range(8):
            centerx, centery = 120 + x * 50 + int(50 / 2), 120 + y * 50 + int(50 / 2)
            if grille[x][y] == TUILE_BLANCHE or grille[x][y] == TUILE_NOIRE:
                if grille[x][y] == TUILE_BLANCHE:
                    tileColor = BLANC
                else:
                    tileColor = NOIR
                pygame.draw.circle(ecran, tileColor, (centerx, centery), int(50 / 2) - 4)
           
def qui_commence():
    global tour
    BIGFONT = pygame.font.Font('freesansbold.ttf', 32)

    textSurf = FONT.render('Voulez-vous commencer?  [Oui : NOIR, Non : BLANC]', True, BLANC, VERT)
    textRect = textSurf.get_rect()
    textRect.center = (int(640 / 2), int(640 / 2))

    xSurf = BIGFONT.render('OUI', True, BLANC, VERT)
    xRect = xSurf.get_rect()
    xRect.center = (int(640 / 2) - 60, int(640 / 2) + 40)

    oSurf = BIGFONT.render('NON', True, BLANC, VERT)
    oRect = oSurf.get_rect()
    oRect.center = (int(640 / 2) + 60, int(640 / 2) + 40)

    while True:
        checkForQuit()
        for event in pygame.event.get(): 
            if event.type == MOUSEBUTTONUP:
                mousex, mousey = event.pos
                if xRect.collidepoint( (mousex, mousey) ):
                    tour = 'joueur'
                    return [TUILE_NOIRE, TUILE_BLANCHE]
                elif oRect.collidepoint( (mousex, mousey) ):
                    tour = 'ordi'
                    return [TUILE_BLANCHE, TUILE_NOIRE]

        ecran.blit(textSurf, textRect)
        ecran.blit(xSurf, xRect)
        ecran.blit(oSurf, oRect)
        pygame.display.update()
        MAINCLOCK.tick(60)


def getPosition(mousex, mousey):
    for x in range(8):
        for y in range(8):
            if mousex > x * 50 + 120 and \
               mousex < (x + 1) * 50 + 120 and \
               mousey > y * 50 + 120 and \
               mousey < (y + 1) * 50 + 120:
                return (x, y)
    return None


def checkForQuit():
    for event in pygame.event.get((QUIT, KEYUP)):
        if event.type == QUIT or (event.type == KEYUP and event.key == K_ESCAPE):
            pygame.quit()
            sys.exit()  


if __name__ == '__main__':
    main()