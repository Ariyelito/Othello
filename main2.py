
from msilib.schema import Font
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
    
    boardImage = pygame.image.load('board.png')
    boardImage = pygame.transform.smoothscale(boardImage, (8 * 50, 8 * 50))

    boardImageRect = boardImage.get_rect()
    boardImageRect.topleft = (120, 120)
    
    BGIMAGE = pygame.transform.smoothscale(BGIMAGE, (640, 640))
    BGIMAGE.blit(boardImage, boardImageRect)

    while True:
        if Jouerjeu() == False:
            break


def Jouerjeu():

    global tour
    tableauPrincipal = getNouveauTableau()    
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
            
            faireMouvement(tableauPrincipal, tuileJoueur, movexy[0], movexy[1], True)
            if getMouvementValide(tableauPrincipal, tuileOrdi) != []:
                tour = 'ordi'


    dessinerTableau(tableauPrincipal)
    scores = scoreTableau(tableauPrincipal)

    if scores[tuileJoueur] > scores[tuileOrdi]:
        text = 'vous avez battu lordinatueur par %s points! Félicitation!' % \
               (scores[tuileJoueur] - scores[tuileOrdi])
    elif scores[tuileJoueur] < scores[tuileOrdi]:
        text = 'Vous avez perdu. lordinateur vous a battu par %s points.' % \
               (scores[tuileOrdi] - scores[tuileJoueur])
    else:
        text = 'Partie Nul'

    textSurf = FONT.render(text, True, BLANC, VERT)
    textRect = textSurf.get_rect()
    textRect.center = (int(640 / 2), int(640 / 2))
    ecran.blit(textSurf, textRect)

    text2Surf = Font.render('Jouer encore', True, BLANC, VERT)
    text2Rect = text2Surf.get_rect()
    text2Rect.center = (int(640 / 2), int(640 / 2) + 50)

    yesSurf = Font.render('oui', True, BLANC, VERT)
    yesRect = yesSurf.get_rect()
    yesRect.center = (int(640 / 2) - 60, int(640 / 2) + 90)

    noSurf = Font.render('non', True, BLANC, VERT)
    noRect = noSurf.get_rect()
    noRect.center = (int(640 / 2) + 60, int(640 / 2) + 90)

    while True:
        checkForQuit()
        for event in pygame.event.get():
            if event.type == MOUSEBUTTONUP:
                mousex, mousey = event.pos
                if yesRect.collidepoint( (mousex, mousey) ):
                    return True
                elif noRect.collidepoint( (mousex, mousey) ):
                    return False
        ecran.blit(textSurf, textRect)
        ecran.blit(text2Surf, text2Rect)
        ecran.blit(yesSurf, yesRect)
        ecran.blit(noSurf, noRect)
        pygame.display.update()
        MAINCLOCK.tick(60)


def scoreTableau(grille):
    xscore = 0
    oscore = 0
    for x in range(8):
        for y in range(8):
            if grille[x][y] == TUILE_BLANCHE:
                xscore += 1
            if grille[x][y] == TUILE_NOIRE:
                oscore += 1
    return {TUILE_BLANCHE:xscore, TUILE_NOIRE:oscore}


def faireMouvement(grille, tuile, x, y, mouvement=False):
   
    tilesToFlip = isValidMove(grille, tuile, x, y)

    if tilesToFlip == False:
        return False

    grille[x][y] = tuile

    if mouvement:
        animationChangementTuile(tilesToFlip, tuile, (x, y))

    for x, y in tilesToFlip:
        grille[x][y] = tuile
    return True


def animationChangementTuile(tuileFlip, tuileCouleur, autreTuile):

    if tuileCouleur == TUILE_BLANCHE:
        additionalTileColor = BLANC
    else:
        additionalTileColor = NOIR
    additionalTileX, additionalTileY = 120 + autreTuile[0] * 50 + int(50 / 2), 120 + autreTuile[1] * 50 + int(50 / 2)
    pygame.draw.circle(ecran, additionalTileColor, (additionalTileX, additionalTileY), int(50 / 2) - 4)
    pygame.display.update()

    for rgbValues in range(0, 255, int(25 * 2.55)):
        if rgbValues > 255:
            rgbValues = 255
        elif rgbValues < 0:
            rgbValues = 0

        if tuileCouleur == TUILE_BLANCHE:
            color = tuple([rgbValues] * 3)
        elif tuileCouleur == TUILE_NOIRE:
            color = tuple([255 - rgbValues] * 3)

        for x, y in tuileFlip:
            centerx, centery = 120 + x * 50 + int(50 / 2), 120 + y * 50 + int(50 / 2)
            pygame.draw.circle(ecran, color, (centerx, centery), int(50 / 2) - 4)
        pygame.display.update()
        MAINCLOCK.tick(60)
        checkForQuit()


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

        print(tour)
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