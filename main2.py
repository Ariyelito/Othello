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
    global BACKGROUND, FONT, HORLOGE, Font2
    pygame.init()
    HORLOGE = pygame.time.Clock()
    BACKGROUND = pygame.image.load('background.png')
    FONT = pygame.font.Font('freesansbold.ttf', 16)
    Font2 = pygame.font.Font('freesansbold.ttf', 32)

    grilleImage = pygame.image.load('board.png')
    grilleImage = pygame.transform.smoothscale(grilleImage, (8 * 50, 8 * 50))

    grilleImageRect = grilleImage.get_rect()
    grilleImageRect.topleft = (120, 120)

    BACKGROUND = pygame.transform.smoothscale(BACKGROUND, (LARG, HAUT))
    BACKGROUND.blit(grilleImage, grilleImageRect)

    while True:
        if Jouerjeu() == False:
            break


def Jouerjeu():
    global tour
    tableauPrincipal = getNouveauTableau()
    razTableau(tableauPrincipal)
    dessinerTableau(tableauPrincipal)
    tuileJoueur, tuileOrdi = qui_commence()
    print('joueur: ' + tuileJoueur)
    print('ordi: ' + tuileOrdi)

    nouvellePartie = FONT.render('Nouvelle Partie', True, BLANC, VERT)
    nouvellePartieRect = nouvellePartie.get_rect()
    nouvellePartieRect.topright = (LARG - 8, 10)

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
            mouvementxy = None
            print('movexy')
            while mouvementxy == None:
                verifierQuitter()
                # Keep looping until the player clicks on a valid space.
                for event in pygame.event.get():
                    if event.type == MOUSEBUTTONUP:
                        xSouris, ySouris = event.pos
                        if nouvellePartieRect.collidepoint((xSouris, ySouris)):
                            return True
                        mouvementxy = obtenirPosition(xSouris, ySouris)
                        if mouvementxy != None and not movementValide(tableauPrincipal, tuileJoueur, mouvementxy[0], mouvementxy[1]):
                            mouvementxy = None

                dessinerTableau(tableauPrincipal)
                ecran.blit(nouvellePartie, nouvellePartieRect)
                HORLOGE.tick(60)
                pygame.display.update()

            faireMouvement(tableauPrincipal, tuileJoueur, mouvementxy[0], mouvementxy[1], True)
            if getMouvementValide(tableauPrincipal, tuileOrdi) != []:
                tour = 'ordi'
        else:
            if getMouvementValide(tableauPrincipal, tuileOrdi) == []:
                break
            dessinerTableau(tableauPrincipal)
            ecran.blit(nouvellePartie, nouvellePartieRect)
            pause = time.time() + random.randint(5, 15) * 0.1
            while time.time() < pause:
                pygame.display.update()
            x, y = ordiMouvement(tableauPrincipal, tuileOrdi)
            faireMouvement(tableauPrincipal, tuileOrdi, x, y, True)
            if getMouvementValide(tableauPrincipal, tuileJoueur) != []:
                tour = 'joueur'

    dessinerTableau(tableauPrincipal)
    scores = scoreTableau(tableauPrincipal)
    text = ''

    if scores[tuileJoueur] > scores[tuileOrdi]:
        text = 'vous avez battu lordinatueur par %s points! Félicitations!' % \
               (scores[tuileJoueur] - scores[tuileOrdi])
    elif scores[tuileJoueur] < scores[tuileOrdi]:
        text = 'Vous avez perdu. lordinateur vous a battu par %s points.' % \
               (scores[tuileOrdi] - scores[tuileJoueur])
    else:
        text = 'Partie Nulle'

    text = FONT.render(text, True, BLANC, VERT)
    textRect = text.get_rect()
    textRect.center = (int(LARG / 2), int(HAUT / 2))
    ecran.blit(text, textRect)

    text2 = Font2.render('Jouer encore', True, BLANC, VERT)
    text2Rect = text2.get_rect()
    text2Rect.center = (int(LARG / 2), int(HAUT / 2) + 50)

    oui = Font2.render('Oui', True, BLANC, VERT)
    ouiRect = oui.get_rect()
    ouiRect.center = (int(LARG / 2) - 60, int(HAUT / 2) + 90)

    non = Font2.render('Non', True, BLANC, VERT)
    nonRect = non.get_rect()
    nonRect.center = (int(LARG / 2) + 60, int(HAUT / 2) + 90)

    while True:
        verifierQuitter()
        for event in pygame.event.get():
            if event.type == MOUSEBUTTONUP:
                xSouris, ySouris = event.pos
                if ouiRect.collidepoint((xSouris, ySouris)):
                    return True
                elif nonRect.collidepoint((xSouris, ySouris)):
                    return False
        ecran.blit(text, textRect)
        ecran.blit(text2, text2Rect)
        ecran.blit(oui, ouiRect)
        ecran.blit(non, nonRect)
        pygame.display.update()
        HORLOGE.tick(60)


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
    ecran.blit(BACKGROUND, BACKGROUND.get_rect())

    for x in range(8 + 1):
        xdebut = (x * 50) + 120
        ydebut = 120
        xfin = (x * 50) + 120
        yfin = 120 + (8 * 50)
        pygame.draw.line(ecran, NOIR, (xdebut, ydebut), (xfin, yfin))

    for y in range(8 + 1):
        xdebut = 120
        ydebut = (y * 50) + 120
        xfin = 120 + (8 * 50)
        yfin = (y * 50) + 120
        pygame.draw.line(ecran, NOIR, (xdebut, ydebut), (xfin, yfin))

    for x in range(8):
        for y in range(8):
            centrex, centrey = 120 + x * 50 + int(50 / 2), 120 + y * 50 + int(50 / 2)
            if grille[x][y] == TUILE_BLANCHE or grille[x][y] == TUILE_NOIRE:
                if grille[x][y] == TUILE_BLANCHE:
                    tuileCouleur = BLANC
                else:
                    tuileCouleur = NOIR
                pygame.draw.circle(ecran, tuileCouleur, (centrex, centrey), int(50 / 2) - 4)


def qui_commence():
    global tour
    GECRAN = pygame.font.Font('freesansbold.ttf', 28)

    textCommence = FONT.render('Voulez-vous commencer?  [Oui : NOIR, Non : BLANC]', True, BLANC, NOIR)
    textReponse = textCommence.get_rect()
    textReponse.center = (int(LARG / 2), int(HAUT / 2) + 220)

    oui = GECRAN.render('OUI', True, BLANC, NOIR)
    ouiReponse = oui.get_rect()
    ouiReponse.center = (int(LARG / 2) - 60, int(HAUT / 2) + 250)

    non = GECRAN.render('NON', True, BLANC, NOIR)
    nonReponse = non.get_rect()
    nonReponse.center = (int(LARG / 2) + 60, int(HAUT / 2) + 250)

    while True:
        # Loop jusqu'à décision du joueur.
        verifierQuitter()
        for event in pygame.event.get():
            if event.type == MOUSEBUTTONUP:
                xSouris, ySouris = event.pos
                if ouiReponse.collidepoint((xSouris, ySouris)):
                    tour = 'joueur'
                    print('Le joueur commence!')
                    return [TUILE_NOIRE, TUILE_BLANCHE]
                elif nonReponse.collidepoint((xSouris, ySouris)):
                    tour = 'ordi'
                    print("L'ordi commence!")
                    return [TUILE_BLANCHE, TUILE_NOIRE]

        # print(tour)
        ecran.blit(textCommence, textReponse)
        ecran.blit(oui, ouiReponse)
        ecran.blit(non, nonReponse)
        pygame.display.update()
        HORLOGE.tick(60)


def getMouvementValide(grille, tuile):
    mouvementValides = []
    for x in range(8):
        for y in range(8):
            # print(movementValide(grille, tuile, x, y))
            if movementValide(grille, tuile, x, y) != False:
                print('appending')
                mouvementValides.append((x, y))
    print(mouvementValides)
    return mouvementValides


def movementValide(grille, tuile, xdebut, ydebut):

    if grille[xdebut][ydebut] != VIDE or not dansLeTableau(xdebut, ydebut):
        return False

    grille[xdebut][ydebut] = tuile

   
    if tuile == TUILE_BLANCHE:
        autreTuile = TUILE_NOIRE
    else:
        autreTuile = TUILE_BLANCHE

    tuileAretourner = []

    for xgrille, ygrille in [[0, 1], [1, 1], [1, 0], [1, -1], [0, -1], [-1, -1], [-1, 0], [-1, 1]]:
        x, y = xdebut, ydebut
        x += xgrille
        y += ygrille
        if dansLeTableau(x, y) and grille[x][y] == autreTuile:
            x += xgrille
            y += ygrille
            if not dansLeTableau(x, y):
                continue
            while grille[x][y] == autreTuile:
                x += xgrille
                y += ygrille
                if not dansLeTableau(x, y):
                    break
            if not dansLeTableau(x, y):
                continue
            if grille[x][y] == tuile:
                while True:
                    x -= xgrille
                    y -= ygrille
                    if x == xdebut and y == ydebut:
                        break
                    tuileAretourner.append([x, y])

    grille[xdebut][ydebut] = VIDE
    if len(tuileAretourner) == 0:
        # print('deuxieme false')
        return False

    return tuileAretourner


def dansLeTableau(x, y):
    return x >= 0 and x < 8 and y >= 0 and y < 8


def scoreTableau(grille):
    tuileBlancheScore = 0
    tuileNoireScore = 0
    for x in range(8):
        for y in range(8):
            if grille[x][y] == TUILE_BLANCHE:
                tuileBlancheScore += 1
            if grille[x][y] == TUILE_NOIRE:
                tuileNoireScore += 1
    return {TUILE_BLANCHE: tuileBlancheScore, TUILE_NOIRE: tuileNoireScore}


def faireMouvement(grille, tuile, x, y, mouvement=False):
    tuileAretourner = movementValide(grille, tuile, x, y)

    if tuileAretourner == False:
        return False

    grille[x][y] = tuile

    if mouvement:
        animationChangementTuile(tuileAretourner, tuile, (x, y))

    for x, y in tuileAretourner:
        grille[x][y] = tuile
    return True


def animationChangementTuile(tuileTourne, tuileCouleur, autreTuile):
    if tuileCouleur == TUILE_BLANCHE:
        plusDeCouleur = BLANC
    else:
        plusDeCouleur = NOIR
    plusDeCouleurX, plusDeCouleurY = 120 + autreTuile[0] * 50 + int(50 / 2), 120 + autreTuile[1] * 50 + int(50 / 2)
    pygame.draw.circle(ecran, plusDeCouleur, (plusDeCouleurX, plusDeCouleurY), int(50 / 2) - 4)
    pygame.display.update()

    for valeurCouleur in range(0, 255, int(25 * 2.55)):
        if valeurCouleur > 255:
            valeurCouleur = 255
        elif valeurCouleur < 0:
            valeurCouleur = 0

        if tuileCouleur == TUILE_BLANCHE:
            couleur = tuple([valeurCouleur] * 3)
        elif tuileCouleur == TUILE_NOIRE:
            couleur = tuple([255 - valeurCouleur] * 3)

        for x, y in tuileTourne:
            centreX, centreY = 120 + x * 50 + int(50 / 2), 120 + y * 50 + int(50 / 2)
            pygame.draw.circle(ecran, couleur, (centreX, centreY), int(50 / 2) - 4)
        pygame.display.update()
        HORLOGE.tick(60)
        verifierQuitter()


def obtenirPosition(xSouris, ySouris):
    for x in range(8):
        for y in range(8):
            if xSouris > x * 50 + 120 and \
                    xSouris < (x + 1) * 50 + 120 and \
                    ySouris > y * 50 + 120 and \
                    ySouris < (y + 1) * 50 + 120:
                return (x, y)
    return None


def ordiMouvement(grille, tuileOrdi):
    mouvementPossibles = getMouvementValide(grille, tuileOrdi)
    random.shuffle(mouvementPossibles)

    for x, y in mouvementPossibles:
        if Corner(x, y):
            return [x, y]

    meilleurScore = -1
    for x, y in mouvementPossibles:
        copieGrille = copy.deepcopy(grille)
        faireMouvement(copieGrille, tuileOrdi, x, y)
        score = scoreTableau(copieGrille)[tuileOrdi]
        if score > meilleurScore:
            meilleurMouvement = [x, y]
            meilleurScore = score
    return meilleurMouvement


def Corner(x, y):
    return (x == 0 and y == 0) or \
           (x == 8 and y == 0) or \
           (x == 0 and y == 8) or \
           (x == 8 and y == 8)


def verifierQuitter():
    for event in pygame.event.get((QUIT)):
        if event.type == QUIT :
            pygame.quit()
            sys.exit()


if __name__ == '__main__':
    main()