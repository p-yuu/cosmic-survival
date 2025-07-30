import pygame
import random
import os

#variable
FPS = 60
WHITE = (255,255,255)
GREEN = (0,255,0)
RED = (255,0,0)
YELLOW = (255,255,0)
BLACK = (0,0,0)
WIDTH = 500
HEIGHT = 600

#initialize
pygame.init()
screen = pygame.display.set_mode((WIDTH,HEIGHT))
pygame.display.set_caption("cosmic survival")
clock = pygame.time.Clock() #限定while迴圈跑的速度，使程式不因電腦性能差異而速度不同

#pictures
background_img = pygame.image.load(os.path.join("img", "background.png")).convert() #convert:把圖片轉換成pygame容易讀取的格式
player_img = pygame.image.load(os.path.join("img", "player.png")).convert()
#stone_img = pygame.image.load(os.path.join("img", "rock.png")).convert() 
bullet_img = pygame.image.load(os.path.join("img", "bullet.png")).convert() 
stone_imgs = []
for i in range(7):
    stone_imgs.append(pygame.image.load(os.path.join("img", f"rock{i}.png")).convert())

#sprite
class Player(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.transform.scale(player_img, (50, 23)) #transform:改變圖片大小
        self.image.set_colorkey(BLACK) #去除黑色外框
        self.rect = self.image.get_rect()
        self.radius = 20 #設定stone半徑，做圓形碰撞用
        #pygame.draw.circle(self.image, RED, self.rect.center, self.radius) #輔助觀察圓的大小
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
    
    def shoot(self):
        bullet = Bullet(self.rect.centerx, self.rect.top)
        all_sprite.add(bullet)
        bullets.add(bullet)
        
class Stone(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image_ori = random.choice(stone_imgs) #儲存未失貞原始圖片(因旋轉圖片)
        self.image_ori.set_colorkey(BLACK)
        self.image = self.image_ori.copy()
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.radius = self.rect.width * 0.85 / 2 #設定stone半徑，做圓形碰撞用
        #pygame.draw.circle(self.image, RED, self.rect.center, self.radius) #輔助觀察圓的大小
        self.rect.x = random.randrange(0, WIDTH - self.rect.width)
        self.rect.y = random.randrange(-180,-100)
        self.speedy = random.randrange(2,10)
        self.speedx = random.randrange(-3,3)
        self.total_degree = 0
        self.rot_degree = 3 #紀錄旋轉角度

    def rotate(self):
        self.total_degree += self.rot_degree
        self.total_degree = self.total_degree % 360 #限定最多只轉360度
        self.image = pygame.transform.rotate(self.image_ori, self.total_degree) #用靜止圖片轉動防止失貞累加
        center = self.rect.center
        self.rect = self.image.get_rect() #捕捉到轉動過有位移的圖片
        self.rect.center = center

    def update(self):
        self.rotate()
        self.rect.y += self.speedy
        self.rect.x += self.speedx
        if self.rect.top > HEIGHT or self.rect.left > WIDTH or self.rect.right < 0:
            self.rect.x = random.randrange(0, WIDTH - self.rect.width)
            self.rect.y = random.randrange(-100,-40)
            self.speedy = random.randrange(2,10)
            self.speedx = random.randrange(-3,3)

class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = bullet_img
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.bottom = y
        self.speedy = -10

    def update(self):
        self.rect.y += self.speedy
        if self.rect.bottom < 0:
            self.kill()

all_sprite = pygame.sprite.Group()
stones = pygame.sprite.Group()
bullets = pygame.sprite.Group()
player = Player()
all_sprite.add(player)
for i in range(8):
    stone = Stone()
    all_sprite.add(stone)
    stones.add(stone)

running = True
while running:
    clock.tick(FPS) # while一秒最多只能執行n次

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                player.shoot()

    #子彈v.s石頭
    all_sprite.update()
    hits = pygame.sprite.groupcollide(stones, bullets, True, True)
    for hit in hits:
        stone = Stone()
        all_sprite.add(stone)
        stones.add(stone)

    #石頭v.s玩家
    hits = pygame.sprite.spritecollide(player, stones, False, pygame.sprite.collide_circle)
    if hits:
        running = False

    screen.fill(WHITE)
    screen.blit(background_img, (0,0))
    all_sprite.draw(screen)
    pygame.display.update()

pygame.quit()