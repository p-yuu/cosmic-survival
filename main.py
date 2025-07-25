import pygame

FPS = 60
WHITE = (255,255,255)
GREEN = (0,255,0)
WIDTH = 500
HEIGHT = 600

pygame.init()
screen = pygame.display.set_mode((WIDTH,HEIGHT))
pygame.display.set_caption("cosmic survival")
clock = pygame.time.Clock() #限定while迴圈跑的速度，使程式不因電腦性能差異而速度不同

class Player(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((50,40))
        self.image.fill(GREEN)
        self.rect = self.image.get_rect()
        self.rect.center = (WIDTH/2, HEIGHT/2)

    def update(self):
        self.rect.x += 2
        if self.rect.left > WIDTH:
            self.rect.right = 0

all_sprite = pygame.sprite.Group()
player = Player()
all_sprite.add(player)

running = True
while running:
    clock.tick(FPS) # while一秒最多只能執行n次

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    all_sprite.update()

    screen.fill(WHITE)
    all_sprite.draw(screen)
    pygame.display.update()

pygame.quit()