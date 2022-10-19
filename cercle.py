import pygame

pygame.init()
# Définir les couleurs (RGB)
BLUE = (0, 0, 255)
BLANC = (255, 255, 255)

# Définir la taille de la fenêtre
screen = pygame.display.set_mode([500, 500])
running = True
while running:
    # Lorsque l'utilisateur click sur le X de la fenêtre, quitter le programme
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Définir l'arriere-plan
    screen.fill(BLANC)

    # Dessiner un cercle bleu au centre de la fenetre
    pygame.draw.circle(screen, BLUE, (250, 250), 75, 2)

    # Mettre à jour l'affichage
    pygame.display.flip()

# Quitter correctement le programme
pygame.quit()