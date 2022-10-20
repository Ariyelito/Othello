import pygame
import math
pygame.init()

GRIS = (200, 200, 200)
BLANC = (255, 255, 255)
NOIR = (0, 0, 0)
def bouton(screen, pos, texte):
 rayon = 75
 pygame.draw.circle(screen, GRIS, pos, rayon)
 txtBtn = font.render(texte, True, NOIR)
 rectBtn = txtBtn.get_rect()
 rectBtn.center = (pos)
 screen.blit(txtBtn, rectBtn)

def isOverBouton(posBouton, posSouris):
 rayon = 75
 xBouton = posBouton[0]
 yBouton = posBouton[1]
 xSouris = posSouris[0]
 ySouris = posSouris[1]
 absX = (xBouton-xSouris)**2
 absY = (yBouton-ySouris)**2
 return (math.sqrt(absX+absY) < rayon)


sysfont = pygame.font.get_default_font()
font = pygame.font.SysFont(None, 36)

screen = pygame.display.set_mode([500, 500])

running = True

while running:
 for event in pygame.event.get():
    if event.type == pygame.QUIT:
        running = False
    elif event.type == pygame.MOUSEBUTTONDOWN:
        xSouris,ySouris = pygame.mouse.get_pos()
        if isOverBouton((250, 250), (xSouris,ySouris)):
            print("bouton")

 screen.fill(BLANC)

 bouton(screen, (250, 250), "ON/OFF")

 pygame.display.flip()

pygame.quit()