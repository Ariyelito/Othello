import pygame
pygame.init()

BLEU = (0, 0, 255)
BLANC = (255, 255, 255)
ROUGE = (255, 0, 0)

screen = pygame.display.set_mode([500, 500])

# Charger la police de caractère
sysfont = pygame.font.get_default_font()
font = pygame.font.SysFont(None, 48)

running = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    screen.fill(BLANC)

    img = font.render("Bonjour!", True, ROUGE)
    screen.blit(img, (20, 20))

    pygame.display.flip()

pygame.quit()
