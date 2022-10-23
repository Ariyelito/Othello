from msilib.schema import Font
import random, sys, pygame, time, copy
from pygame.locals import *

tour = ' '
VIDE = "VIDE"
TUILE_NOIRE = "NOIRE"
TUILE_BLANCHE = "BLANCHE"
LARG = 640
HAUT = 640
ecran = pygame.display.set_mode((LARG, HAUT))
BLANC = (255, 255, 255)
NOIR = (0, 0, 0)
VERT = (0, 155, 0)


def main():
    global BACKGROUND, FONT, MAINCLOCK, Font2
    pygame.init()
    MAINCLOCK = pygame.time.Clock()
    BACKGROUND = pygame.image.load('background.png')
    FONT = pygame.font.Font('freesansbold.ttf', 16)
    Font2 = pygame.font.Font('freesansbold.ttf', 32)

    boardImage = pygame.image.load('board.png')
    boardImage = pygame.transform.smoothscale(boardImage, (8 * 50, 8 * 50))

    boardImageRect = boardImage.get_rect()
    boardImageRect.topleft = (120, 120)

    BACKGROUND = pygame.transform.smoothscale(BACKGROUND, (LARG, HAUT))
    BACKGROUND.blit(boardImage, boardImageRect)

    while True:
        if Jouerjeu() == False:
            break


def Jouerjeu():
    global tour
    global tableauPrincipal
    tableauPrincipal = getNouveauTableau()
    razTableau(tableauPrincipal)
    dessinerTableau()
    tuileJoueur, tuileOrdi = qui_commence()
    print('joueur: ' + tuileJoueur)
    print('ordi: ' + tuileOrdi)

    newGameSurf = FONT.render('Nouvelle Partie', True, BLANC, VERT)
    newGameRect = newGameSurf.get_rect()
    newGameRect.topright = (LARG - 8, 10)

    # Loop principale du jeu
    while True:
        # Keep looping for player and computer's turns.
        print('le tour à :')
        print(tour)
        if tour == 'joueur':
            # Player's turn:
            if getMouvementValide(tableauPrincipal, tuileJoueur) == []:
                # If it's the player's turn but they
                # can't move, then end the game.
                print('break while')
                break
            movexy = None
            print('movexy')
            while movexy == None:
                checkForQuit()
                # Keep looping until the player clicks on a valid space.
                for event in pygame.event.get():
                    if event.type == MOUSEBUTTONUP:
                        mousex, mousey = event.pos
                        if newGameRect.collidepoint((mousex, mousey)):
                            return True
                        movexy = getPosition(mousex, mousey)
                        if movexy != None and not movementValide(tableauPrincipal, tuileJoueur, movexy[0], movexy[1]):
                            movexy = None

                dessinerTableau()
                ecran.blit(newGameSurf, newGameRect)
                MAINCLOCK.tick(60)
                pygame.display.update()

            faireMouvement(tableauPrincipal, tuileJoueur, movexy[0], movexy[1], True)
            if getMouvementValide(tableauPrincipal, tuileOrdi) != []:
                tour = 'ordi'
        else:
            if getMouvementValide(tableauPrincipal, tuileOrdi) == []:
                break
            dessinerTableau()
            ecran.blit(newGameSurf, newGameRect)
            pauseUntil = time.time() + random.randint(5, 15) * 0.1
            while time.time() < pauseUntil:
                pygame.display.update()
            x, y = ordiMouvement(tableauPrincipal, tuileOrdi)
            faireMouvement(tableauPrincipal, tuileOrdi, x, y, True)
            if getMouvementValide(tableauPrincipal, tuileJoueur) != []:
                tour = 'joueur'

    dessinerTableau()
    scores = scoreTableau(tableauPrincipal)
    text = ''

    if scores[tuileJoueur] > scores[tuileOrdi]:
        text = 'vous avez battu lordinatueur par %s points! Félicitation!' % \
               (scores[tuileJoueur] - scores[tuileOrdi])
    elif scores[tuileJoueur] < scores[tuileOrdi]:
        text = 'Vous avez perdu. lordinateur vous a battu par %s points.' % \
               (scores[tuileOrdi] - scores[tuileJoueur])
    else:
        text = 'Partie Nul'

    text = FONT.render(text, True, BLANC, VERT)
    textRect = text.get_rect()
    textRect.center = (int(LARG / 2), int(HAUT / 2))
    ecran.blit(text, textRect)

    text2 = Font2.render('Jouer encore', True, BLANC, VERT)
    text2Rect = text2.get_rect()
    text2Rect.center = (int(LARG / 2), int(HAUT / 2) + 50)

    oui = Font2.render('oui', True, BLANC, VERT)
    ouiRect = oui.get_rect()
    ouiRect.center = (int(LARG / 2) - 60, int(HAUT / 2) + 90)

    non = Font2.render('non', True, BLANC, VERT)
    nonRect = non.get_rect()
    nonRect.center = (int(LARG / 2) + 60, int(HAUT / 2) + 90)

    while True:
        checkForQuit()
        for event in pygame.event.get():
            if event.type == MOUSEBUTTONUP:
                mousex, mousey = event.pos
                if ouiRect.collidepoint((mousex, mousey)):
                    return True
                elif nonRect.collidepoint((mousex, mousey)):
                    return False
        ecran.blit(text, textRect)
        ecran.blit(text2, text2Rect)
        ecran.blit(oui, ouiRect)
        ecran.blit(non, nonRect)
        pygame.display.update()
        MAINCLOCK.tick(60)


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


def dessinerTableau():
    ecran.blit(BACKGROUND, BACKGROUND.get_rect())

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
            if tableauPrincipal[x][y] == TUILE_BLANCHE or tableauPrincipal[x][y] == TUILE_NOIRE:
                if tableauPrincipal[x][y] == TUILE_BLANCHE:
                    tileColor = BLANC
                else:
                    tileColor = NOIR
                pygame.draw.circle(ecran, tileColor, (centerx, centery), int(50 / 2) - 4)


def qui_commence():
    global tour
    BIGFONT = pygame.font.Font('freesansbold.ttf', 28)

    textSurf = FONT.render('Voulez-vous commencer?  [Oui : NOIR, Non : BLANC]', True, BLANC, NOIR)
    textRect = textSurf.get_rect()
    textRect.center = (int(LARG / 2), int(HAUT / 2) + 220)

    xSurf = BIGFONT.render('OUI', True, BLANC, NOIR)
    xRect = xSurf.get_rect()
    xRect.center = (int(LARG / 2) - 60, int(HAUT / 2) + 250)

    oSurf = BIGFONT.render('NON', True, BLANC, NOIR)
    oRect = oSurf.get_rect()
    oRect.center = (int(LARG / 2) + 60, int(HAUT / 2) + 250)

    while True:
        # Loop jusqu'à décision du joueur.
        checkForQuit()
        for event in pygame.event.get():
            if event.type == MOUSEBUTTONUP:
                mousex, mousey = event.pos
                if xRect.collidepoint((mousex, mousey)):
                    tour = 'joueur'
                    print('Le joueur commence!')
                    return [TUILE_NOIRE, TUILE_BLANCHE]
                elif oRect.collidepoint((mousex, mousey)):
                    tour = 'ordi'
                    print("L'ordi commence!")
                    return [TUILE_BLANCHE, TUILE_NOIRE]

        # print(tour)
        ecran.blit(textSurf, textRect)
        ecran.blit(xSurf, xRect)
        ecran.blit(oSurf, oRect)
        pygame.display.update()
        MAINCLOCK.tick(60)


def getMouvementValide(grille, tuile):
    validMoves = []
    for x in range(8):
        for y in range(8):
            if movementValide(grille, tuile, x, y) != False:
                validMoves.append((x, y))
    print('moves :')
    print(validMoves)
    return validMoves


def movementValide(grille, tuile, x, y):
    # Returns False if the player's move is invalid. If it is a valid
    # move, returns a list of spaces of the captured pieces.
    if grille[x][y] != VIDE or not dansLeTableau(x, y):
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
        if dansLeTableau(x, y) and grille[x][y] == autreTuile:

            x += xdirection
            y += ydirection
            if not dansLeTableau(x, y):
                continue
            while grille[x][y] == autreTuile:
                x += xdirection
                y += ydirection
                if not dansLeTableau(x, y):
                    break
            if not dansLeTableau(x, y):
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


def dansLeTableau(x, y):
    return x >= 0 and x < 8 and y >= 0 and y < 8


def scoreTableau(grille):
    xscore = 0
    oscore = 0
    for x in range(8):
        for y in range(8):
            if grille[x][y] == TUILE_BLANCHE:
                xscore += 1
            if grille[x][y] == TUILE_NOIRE:
                oscore += 1
    return {TUILE_BLANCHE: xscore, TUILE_NOIRE: oscore}


def faireMouvement(grille, tuile, x, y, mouvement=False):
    tilesToFlip = movementValide(grille, tuile, x, y)

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


def getPosition(mousex, mousey):
    for x in range(8):
        for y in range(8):
            if mousex > x * 50 + 120 and \
                    mousex < (x + 1) * 50 + 120 and \
                    mousey > y * 50 + 120 and \
                    mousey < (y + 1) * 50 + 120:
                return (x, y)
    return None


def ordiMouvement(grille, tuileOrdi):
    possibleMoves = getMouvementValide(grille, tuileOrdi)
    random.shuffle(possibleMoves)

    for x, y in possibleMoves:
        if Corner(x, y):
            return [x, y]

    bestScore = -1
    for x, y in possibleMoves:
        dupeBoard = copy.deepcopy(grille)
        faireMouvement(dupeBoard, tuileOrdi, x, y)
        score = scoreTableau(dupeBoard)[tuileOrdi]
        if score > bestScore:
            bestMove = [x, y]
            bestScore = score
    return bestMove


def Corner(x, y):
    return (x == 0 and y == 0) or \
           (x == 8 and y == 0) or \
           (x == 0 and y == 8) or \
           (x == 8 and y == 8)


def checkForQuit():
    for event in pygame.event.get((QUIT, KEYUP)):
        if event.type == QUIT or (event.type == KEYUP and event.key == K_ESCAPE):
            pygame.quit()
            sys.exit()


if __name__ == '__main__':
    main()
