import pygame

pygame.init()
BLEU = (0, 0, 255)
BLANC = (255, 255, 255)
screen = pygame.display.set_mode([500, 500])
running = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    screen.fill(BLANC)
    pygame.draw.rect(screen, BLEU, (200, 200, 100, 100), 2)
    pygame.display.flip()
pygame.quit()
