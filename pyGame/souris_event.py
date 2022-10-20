import pygame

pygame.init()

BLANC = (255, 255, 255)

screen = pygame.display.set_mode([500, 500])

running = True

while running:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            xSouris, ySouris = pygame.mouse.get_pos()
            print("Clic souris (" + str(xSouris) + ", " + str(ySouris) + ")")

    screen.fill(BLANC)

    pygame.display.flip()

pygame.quit()
