import pygame
from pygame.sprite import Sprite

class Ship(Sprite):   #让Ship继承Sprite
    def __init__(self,ai_game):
        super().__init__()
        self.screen = ai_game.screen    #需要画在屏幕上
        self.settings = ai_game.settings   #需要飞船速度参数
        self.screen_rect = ai_game.screen.get_rect()

        self.image = pygame.image.load('images/ship.bmp')  #用自己选择的图像
        self.image.set_colorkey((230, 230, 230))  # 把原本的深灰色设为透明
        self.rect = self.image.get_rect()

        self.rect.midbottom = self.screen_rect.midbottom  #每艘飞船出现在底部中央
        self.x = float(self.rect.x)   #飞船的属性x中存储一个浮点数
        self.moving_right = False    #初始右移标志为0
        self.moving_left = False     #初始左移标志为0

    def update(self):   #调整飞船位置的方法
        if self.moving_right and self.rect.right < self.screen_rect.right: #控制右边界
            self.x += self.settings.ship_speed   #速度不固定为1，可以动态更改
        if self.moving_left and self.rect.left > 0:   #控制左边界
            self.x -= self.settings.ship_speed

        self.rect.x = self.x   #根据self.x更新rect对象

    def center_ship(self):
        self.rect.midbottom = self.screen_rect.midbottom  #飞船放在屏幕正中央
        self.x = float(self.rect.x)    #坐标为矩形框的横坐标，浮点数

    def blitme(self):
        self.screen.blit(self.image, self.rect)



