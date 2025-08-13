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
pygame.mixer.init()
screen = pygame.display.set_mode((WIDTH,HEIGHT))
pygame.display.set_caption("cosmic survival")
clock = pygame.time.Clock() #限定while迴圈跑的速度，使程式不因電腦性能差異而速度不同

#pictures
background_img = pygame.image.load(os.path.join("img", "background.png")).convert() #convert:把圖片轉換成pygame容易讀取的格式
player_img = pygame.image.load(os.path.join("img", "player.png")).convert()
player_mini_img = pygame.transform.scale(player_img, (25,19))
player_mini_img.set_colorkey(BLACK)
bullet_img = pygame.image.load(os.path.join("img", "bullet.png")).convert() 
stone_imgs = []
for i in range(7):
    stone_imgs.append(pygame.image.load(os.path.join("img", f"rock{i}.png")).convert())
expl_anim = {}
expl_anim['lg'] = []
expl_anim['sm'] = []
expl_anim['player'] = []
for i in range(9):
    expl_img = pygame.image.load(os.path.join("img", f"expl{i}.png")).convert()
    expl_img.set_colorkey(BLACK)
    expl_anim['lg'].append(pygame.transform.scale(expl_img, (75,75)))
    expl_anim['sm'].append(pygame.transform.scale(expl_img, (30,30)))
    player_expl_img = pygame.image.load(os.path.join("img", f"player_expl{i}.png")).convert()
    player_expl_img.set_colorkey(BLACK)
    expl_anim['player'].append(player_expl_img)

#music
shoot_sound = pygame.mixer.Sound(os.path.join("sound", "shoot.wav"))
die_sound = pygame.mixer.Sound(os.path.join("sound", "rumble.ogg"))
expl_sound = [
    pygame.mixer.Sound(os.path.join("sound", "expl0.wav")),
    pygame.mixer.Sound(os.path.join("sound", "expl1.wav"))
]
pygame.mixer.music.load(os.path.join("sound", "background.ogg"))
pygame.mixer.music.set_volume(0.4) #數字表聲音大小(0~1)

#text
font_name = pygame.font.match_font('arial')
def draw_text(surf, text, size, x, y):
    font = pygame.font.Font(font_name, size)
    text_surface = font.render(text, True, WHITE) #True: 文字反鋸齒
    text_rect = text_surface.get_rect()
    text_rect.centerx = x
    text_rect.top = y
    surf.blit(text_surface, text_rect)

def new_stone():
    stone = Stone()
    all_sprite.add(stone)
    stones.add(stone)

def draw_health(surf, hp, x, y):
    if hp < 0:
        hp = 0
    BAR_LENGTH = 100
    BAR_HEIGHT = 10
    fill = (hp / 100) * BAR_LENGTH
    outline_rect = pygame.Rect(x, y, BAR_LENGTH, BAR_HEIGHT)
    fill_rect = pygame.Rect(x, y, fill, BAR_HEIGHT)
    pygame.draw.rect(surf, GREEN, fill_rect)
    pygame.draw.rect(surf, WHITE, outline_rect, 2)

def draw_lives(surf, lives, img, x, y):
    for i in range(lives):
        img_rect = img.get_rect()
        img_rect.x = x + 32 * i
        img_rect.y = y
        surf.blit(img, img_rect)

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
        self.health = 100
        self.lives = 3
        self.hidden = False
        self.hide_time = 0

    def update(self):
        if self.hidden and pygame.time.get_ticks() - self.hide_time > 1000:
            self.hidden = False
            self.rect.centerx = WIDTH / 2
            self.rect.bottom = HEIGHT - 10

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
        if not(self.hidden):
            bullet = Bullet(self.rect.centerx, self.rect.top)
            all_sprite.add(bullet)
            bullets.add(bullet)
            shoot_sound.play()

    def hide(self):
        self.hidden = True
        self.hide_time = pygame.time.get_ticks()
        self.rect.center = (WIDTH / 2, HEIGHT + 500)
        
class Stone(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image_ori = random.choice(stone_imgs) #儲存未失貞原始圖片(因旋轉圖片)
        self.image_ori.set_colorkey(BLACK)
        self.image = self.image_ori.copy()
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.radius = int(self.rect.width * 0.85 / 2) #設定stone半徑，做圓形碰撞用
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

class Explosion(pygame.sprite.Sprite):
    def __init__(self, center, size):
        pygame.sprite.Sprite.__init__(self)
        self.size = size
        self.image = expl_anim[self.size][0]
        self.rect = self.image.get_rect()
        self.rect.center = center
        self.frame = 0
        self.last_update = pygame.time.get_ticks() #回傳從開始到現在的毫秒數
        self.frame_rate = 50 #避免圖片更新過快

    def update(self):
        now = pygame.time.get_ticks()
        if now - self.last_update > self.frame_rate:
            self.last_update = now
            self.frame += 1
            if self.frame == len(expl_anim[self.size]):
                self.kill()
            else:
                self.image = expl_anim[self.size][self.frame]
                center = self.rect.center
                self.rect = self.image.get_rect()
                self.rect.center = center

all_sprite = pygame.sprite.Group()
stones = pygame.sprite.Group()
bullets = pygame.sprite.Group()
player = Player()
all_sprite.add(player)
for i in range(8):
    new_stone()
score = 0
pygame.mixer.music.play(-1) #-1:無限重複撥放

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
        random.choice(expl_sound).play()
        score += hit.radius
        expl = Explosion(hit.rect.center, 'lg')
        all_sprite.add(expl)
        new_stone()

    #石頭v.s玩家
    hits = pygame.sprite.spritecollide(player, stones, True, pygame.sprite.collide_circle)
    for hit in hits:
        new_stone()
        expl = Explosion(hit.rect.center, 'sm')
        all_sprite.add(expl)
        player.health -= hit.radius
        if player.health <= 0:
            death_expl = Explosion(player.rect.center, 'player')
            all_sprite.add(death_expl)
            die_sound.play()
            player.lives -= 1
            player.health = 100
            player.hide()

    if player.lives == 0 and not(death_expl.alive()):
        running = False

    screen.fill(WHITE)
    screen.blit(background_img, (0,0))
    all_sprite.draw(screen)
    draw_text(screen, str(score), 18, WIDTH / 2, 10)
    draw_health(screen, player.health, 5, 15)
    draw_lives(screen, player.lives, player_mini_img, WIDTH - 100, 15)
    pygame.display.update()

pygame.quit()