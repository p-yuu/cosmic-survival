import pygame

FPS = 60
WHITE = (255,255,255)
WIDTH = 500
HEIGHT = 600

pygame.init()
screen = pygame.display.set_mode((WIDTH,HEIGHT))
clock = pygame.time.Clock() #限定while迴圈跑的速度，使程式不因電腦性能差異而速度不同

running = True
while running:
    clock.tick(FPS) # while一秒最多只能執行n次

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill(WHITE)
    pygame.display.update()

pygame.quit()