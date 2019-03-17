# -*- coding:utf-8 -*-

import pygame
from pygame.locals import *
import time
import random

class Base(object):
    def __init__(self, screen_temp, x, y, image_name):
        self.x = x
        self.y = y
        self.screen = screen_temp
        self.image = pygame.image.load(image_name)

class BasePlane(Base):
    def __init__(self, screen_temp, x, y, image_name):
        Base.__init__(self, screen_temp, x, y, image_name)
        self.bullet_list = []#存储发射出去的子弹对象引用

    def display(self):
        self.screen.blit(self.image, (self.x, self.y))
        
        for bullet in self.bullet_list:
            bullet.display()
            bullet.move()
            if bullet.judge():#判断子弹是否越界
                self.bullet_list.remove(bullet)

class HeroPlane(BasePlane):
    def __init__(self, screen_temp):
        BasePlane.__init__(self, screen_temp, 210, 450, "./aircraft_pic/hero1.png") #super().__init__()
        # 爆炸效果用的如下属性
        self.hit = False  # 表示是否要爆炸
        self.bomb_list = []  # 用来存储爆炸时需要的图片
        self.__crate_images()  # 调用这个方法向bomb_list中添加图片
        self.image_num = 0  # 用来记录while True的次数,当次数达到一定值时才显示一张爆炸的图,然后清空,,当这个次数再次达到时,再显示下一个爆炸效果的图片
        self.image_index = 0  # 用来记录当前要显示的爆炸效果的图片的序号

    def __crate_images(self):
        self.bomb_list.append(pygame.image.load("./aircraft_pic/hero_blowup_n1.png"))
        self.bomb_list.append(pygame.image.load("./aircraft_pic/hero_blowup_n2.png"))
        self.bomb_list.append(pygame.image.load("./aircraft_pic/hero_blowup_n3.png"))
        self.bomb_list.append(pygame.image.load("./aircraft_pic/hero_blowup_n4.png"))

    def display(self):
        """显示玩家的飞机"""
        # 如果被击中,就显示爆炸效果,否则显示普通的飞机效果
        if self.hit == True:
            self.screen.blit(self.bomb_list[self.image_index], (self.x, self.y))
            self.image_num += 1
            if self.image_num == 7:
                self.image_num = 0
                self.image_index += 1
            if self.image_index > 3:
                time.sleep(1)
                exit()  # 调用exit让游戏退出
                # self.image_index = 0
        else:
            self.screen.blit(self.image, (self.x, self.y))
        # 不管玩家飞机是否被击中,都要显示发射出去的子弹
        for bullet in self.bullet_list:
            bullet.display()
            bullet.move()

    def move_left(self):
        self.x -= 5

    def move_right(self):
        self.x += 5

    def fire(self):
        self.bullet_list.append(Bullet(self.screen, self.x, self.y))
    def bomb(self):
        self.hit = True

class EnemyPlane(BasePlane):
    """敌机的类"""
    def __init__(self, screen_temp):
        BasePlane.__init__(self, screen_temp, 0, 0, "./aircraft_pic/enemy0.png")
        self.direction = "right"#用来存储飞机默认的显示方向

    def move(self):
        
        if self.direction=="right":
            self.x += 5
        elif self.direction=="left":
            self.x -= 5

        if self.x>480-50:
            self.direction = "left"
        elif self.x<0:
            self.direction = "right"

    def fire(self):
        random_num = random.randint(1,100) 
        if random_num == 8 or random_num == 20:
            self.bullet_list.append(EnemyBullet(self.screen, self.x, self.y))

class BaseBullet(Base):
    def display(self):
        self.screen.blit(self.image, (self.x, self.y))

class Bullet(BaseBullet):
    def __init__(self, screen_temp, x, y):
        BaseBullet.__init__(self, screen_temp, x+40, y-20, "./aircraft_pic/bullet.png")

    def move(self):
        self.y-=20

    def judge(self):
        if self.y<0:
            return True
        else:
            return False
    def display(self):
        self.screen.blit(self.image, (self.x, self.y))


class EnemyBullet(BaseBullet):
    def __init__(self, screen_temp, x, y):
        BaseBullet.__init__(self, screen_temp, x+25, y+40, "./aircraft_pic/bullet1.png")

    def move(self):
        self.y+=5

    def judge(self):
        if self.y>852:
            return True
        else:
            return False

def key_control(hero_temp):

    #获取事件，比如按键等
    for event in pygame.event.get():

        #判断是否是点击了退出按钮
        if event.type == QUIT:
            print("exit")
            exit()
        #判断是否是按下了键
        elif event.type == KEYDOWN:
            #检测按键是否是a或者left
            if event.key == K_a or event.key == K_LEFT:
                print('left')
                hero_temp.move_left()
            #检测按键是否是d或者right
            elif event.key == K_d or event.key == K_RIGHT:
                print('right')
                hero_temp.move_right()
            #检测按键是否是空格键
            elif event.key == K_SPACE:
                print('space')
                hero_temp.fire()
            elif event.key == K_b:
                print('b')
                hero_temp.bomb()

def main():
    #1. 创建窗口
    screen = pygame.display.set_mode((400,600),0,32)

    #2. 创建一个背景图片
    background = pygame.image.load("./aircraft_pic/background.png")

    #3. 创建一个飞机对象
    hero = HeroPlane(screen)

    #4. 创建一个敌机
    enemy = EnemyPlane(screen)

    while True:
        screen.blit(background, (0,0))
        hero.display()
        enemy.display()
        enemy.move()#调用敌机的移动方法
        enemy.fire()#敌机开火
        pygame.display.update()
        key_control(hero)
        time.sleep(0.01)

if __name__ == "__main__":
    main()
