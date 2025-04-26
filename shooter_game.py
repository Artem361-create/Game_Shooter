#Создай собственный Шутер!
from pygame import *
from random import randint
import time as tm
init()
lost = 0
count = 0
#* GameSprite - основной класс для спрайтов.
class GameSprite(sprite.Sprite):
    def __init__(self, player_image, player_x, player_y, player_speed, width, height):
        super().__init__()
        self.image = transform.scale(image.load(player_image), (width, height))
        self.speed = player_speed
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y
    def reset(self):
        window.blit(self.image,(self.rect.x, self.rect.y))
# *? Player - класс для игрока
class Player(GameSprite):
    def update(self):
        if keys_pressed[K_LEFT]  and self.rect.x > 2:
            self.rect.x -= self.speed
        if keys_pressed[K_RIGHT]  and self.rect.x < 635:
            self.rect.x += self.speed
    def fire(self):
        global num_fire
        if keys_pressed[K_SPACE]:
            bullet = Bullet('bullet.png', self.rect.centerx, self.rect.top, 10, 10, 20)
            bullets.add(bullet)
            num_fire = num_fire + 1
            fire_sound = mixer.Sound('fire.ogg')
            fire_sound.set_volume(0.09)
            fire_sound.play()
# *! Enemy - класс для врага 
class Enemy(GameSprite):
    def update(self):
        self.rect.y += self.speed
        global lost
        global text_lose
        if self.rect.y > 500:
            self.rect.x = randint(80, 620)
            self.rect.y = 0
            lost = lost + 1 
            text_lose = count_font.render('Пропущено: ' + str(lost), 1, (255, 255, 255))
# TODO: Bullet - класс для пули
class Bullet(GameSprite):
    def update(self):
        self.rect.y -= self.speed
        if self.rect.y  < 0:
            self.kill()

class Asteroids(GameSprite):
    def update(self):
        self.rect.y += self.speed
        if self.rect.y > 500:
            self.rect.x = randint(80, 620)
            self.rect.y = 0

window = display.set_mode((700, 500))
display.set_caption('Шутер')
Background = transform.scale(image.load('galaxy.jpg'), (700, 500))
monsters = sprite.Group()
bullets = sprite.Group()
asteroids = sprite.Group()
hero = Player('rocket.png', 300, 375, 4, 90, 110)
# создание группы врагов
enemy1 = Enemy('ufo.png', randint(10, 490), 0, randint(1, 3), 85, 60)
enemy2 = Enemy('ufo.png', randint(10, 490), 0, randint(1, 4), 85, 60)
enemy3 = Enemy('ufo.png', randint(10, 490), 0, randint(1, 3), 85, 60)
enemy4 = Enemy('ufo.png', randint(10, 490), 0, randint(1, 3), 85, 60)
enemy5 = Enemy('ufo.png', randint(10, 490), 0, randint(1, 3), 85, 60)
monsters.add(enemy1)
monsters.add(enemy2)
monsters.add(enemy3)
monsters.add(enemy4)
monsters.add(enemy5)
# создание группы астероидов 
asteroid1 = Asteroids('asteroid.png', randint(10, 490), 0, randint(1, 3), 80, 80)
asteroid2 = Asteroids('asteroid.png', randint(10, 490), 0, randint(1, 3), 80, 80)
asteroid3 = Asteroids('asteroid.png', randint(10, 490), 0, randint(1, 4), 80, 80)
asteroids.add(asteroid1)
asteroids.add(asteroid2)
asteroids.add(asteroid3)
game = True
finish = False
clock = time.Clock()
FPS = 60
mixer.music.load('space.ogg')
mixer.music.set_volume(0.05)
mixer.music.play()
num_fire = 0
real_time = False
live = 4
count_font = font.SysFont('Comic Sans MS', 27)
play_font = font.SysFont('Comic Sans MS', 65)
reload_font = font.SysFont('Comic Sans MS', 24)
text_lose = count_font.render('Пропущено: ' + str(lost), 1, (255, 255, 255))
text_win = count_font.render('Счёт: ' + str(count), 1, (255, 255, 255))
text_live = count_font.render('Жизни: ' + str(live), 1, (255, 0, 0))
while game == True:
    if finish != True:
        keys_pressed = key.get_pressed()
        window.blit(Background, (0, 0))
        hero.reset()
        hero.update()
        monsters.draw(window)
        monsters.update()
        bullets.draw(window)
        bullets.update()
        print(num_fire)
        if num_fire < 12 and real_time == False:
            hero.fire()
        if num_fire >= 12 and real_time == False:
            real_time = True
            reload_time = tm.time() 
        if real_time == True:
            new_time = tm.time()
            if new_time - reload_time <= 3:
                text_reload = reload_font.render('Выполняется перезарядка: ', 1, (255, 255, 255))
                window.blit(text_reload, (230, 450))
            else:
                real_time = False
                num_fire = 0   
        asteroids.draw(window)
        asteroids.update()
        window.blit(text_lose, (10, 45))
        window.blit(text_win, (10, 15))
        window.blit(text_live, (550, 15))
        sprites_list = sprite.groupcollide(monsters, bullets, True, True)
        if sprites_list:
            new_enemy = Enemy('ufo.png', randint(10, 490), 0, randint(1, 4), 95, 70)
            monsters.add(new_enemy)
            count = count + 1
            text_win = count_font.render('Счёт: ' + str(count), 1, (255, 255, 255))
        collide_list = sprite.spritecollide(hero, monsters, True)
        asteroids_clollide = sprite.spritecollide(hero, asteroids, True)
        if collide_list or asteroids_clollide:
            new_enemy = Enemy('ufo.png', randint(10, 490), 0, randint(1, 4), 95, 70)
            monsters.add(new_enemy)
            live = live - 1
            text_live = count_font.render('Жизни: ' + str(live), 1, (255, 0, 0))           
        if live <= 0:
            finish = True
            lose = play_font.render('You lose ', 1, (255, 0, 0))
            window.blit(lose, (250, 220))
            mixer.music.stop()
        if count > 10:
            finish = True
            win = play_font.render('You win ', 1, (101, 255, 50))
            window.blit(win, (250, 220))
            mixer.music.stop()
        if lost > 4: 
            finish = True
            lose = play_font.render('You lose ', 1, (255, 0, 0))
            window.blit(lose, (250, 220))
            mixer.music.stop()
        collide_asteroid = sprite.spritecollide(hero, asteroids, False)
        if collide_asteroid:
            finish = True
            lose = play_font.render('You lose ', 1, (255, 0, 0))
            window.blit(lose, (250, 220))
            mixer.music.stop()
    for e in event.get():
        if e.type == QUIT:
            game = False
    display.update()
    clock.tick(FPS)
