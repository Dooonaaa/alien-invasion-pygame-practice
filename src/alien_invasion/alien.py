import pygame
from pygame.sprite import Sprite

class Alien(Sprite):   #创建外星人的类，继承自父类Sprite
    def __init__(self,ai_game):   #初始化
        super().__init__()
        self.screen = ai_game.screen   #需要画在屏幕上
        self.settings = ai_game.settings   #需要外星人速度参数

        self.image = pygame.image.load('assets/images/alien.bmp')   #读入外星人图片
        self.rect = self.image.get_rect()  
        self.image.set_colorkey((230, 230, 230))  # 把原本的深灰色设为透明
        #外星人初始均出现在左上角
        self.rect.x = self.rect.width
        self.rect.y = self.rect.height
        #用浮点数精确表示外星人的位置
        self.x = float(self.rect.x)

    def check_edges(self):
        screen_rect = self.screen.get_rect()
        return (self.rect.right >= screen_rect.right) or (self.rect.left <= 0)
               #如果外星人的矩形框超过右边界或左边界，就记录下来

    def update(self):   #更新外星人位置的方法
        # 移动量为alien_speed,浮点数,向右为加，向左为减
        self.x += self.settings.alien_speed * self.settings.fleet_direction
        self.rect.x = self.x   #更新横坐标，按整数


