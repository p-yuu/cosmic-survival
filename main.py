import pygame

#variable
FPS = 60
WHITE = (255,255,255)
GREEN = (0,255,0)
WIDTH = 500
HEIGHT = 600

#initialize
pygame.init()
screen = pygame.display.set_mode((WIDTH,HEIGHT))
pygame.display.set_caption("cosmic survival")
clock = pygame.time.Clock() #限定while迴圈跑的速度，使程式不因電腦性能差異而速度不同

#sprite
class Player(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((50,40))
        self.image.fill(GREEN)
        self.rect = self.image.get_rect()
        self.rect.centerx = WIDTH/2
        self.rect.bottom = HEIGHT - 10
        self.speedx = 8

    def update(self):
        key_pressed = pygame.key.get_pressed()
        if key_pressed[pygame.K_RIGHT]:
            self.rect.x += self.speedx
        if key_pressed[pygame.K_LEFT]:
            self.rect.x -= self.speedx
        if self.rect.right > WIDTH:
            self.rect.right = WIDTH
        if self.rect.left < 0:
            self.rect.left = 0
        

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