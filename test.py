import pygame

pygame.init()
screen = pygame.display.set_mode((200, 200))
img = pygame.image.load("BAT.jpg")
clock = pygame.time.Clock()
game_running = True
c = 1
while game_running:
    c += 1
    # evaluate the pygame event
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game_running = False  # or anything else to quit the main loop

    screen.fill((0, 0, 0))
    if 10 < c < 100:
        screen.blit(img, (0, 0))
    pygame.display.flip()
    clock.tick(60)