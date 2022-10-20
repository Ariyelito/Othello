import pygame

pygame.init()

BLANC = (255, 255, 255)

screen = pygame.display.set_mode([500, 500])

running = True

while running:
 for event in pygame.event.get():
     if event.type == pygame.QUIT:
      running = False
     elif event.type == pygame.KEYDOWN:
       if event.key == pygame.K_UP:
           print("Fleche vers le haut")
       elif event.key == pygame.K_a:
        print("La touche a")

screen.fill(BLANC)

pygame.display.flip()

pygame.quit()
