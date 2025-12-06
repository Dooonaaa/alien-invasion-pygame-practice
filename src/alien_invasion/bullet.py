import pygame
from pygame.sprite import Sprite  #从pygame.sprite模块  导入  Sprite类

class Bullet(Sprite):   #继承自父类Sprite
    def __init__(self,ai_game):
        super().__init__()   #继承父类的写法
        self.screen = ai_game.screen   #需要把子弹画在屏幕上
        self.settings = ai_game.settings    #需要获取子弹的速度参数
        self.color = (255,215,0)     #子弹颜色设为金色
        #设置子弹为圆形
        self.image = pygame.Surface((12,12),pygame.SRCALPHA)   #子弹背景为透明
        pygame.draw.circle(self.image,self.color,(6,6),6)   #子弹大小
        self.rect = self.image.get_rect()

        #更改子弹位置为飞船的位置
        self.rect.midtop = ai_game.ship.rect.midtop   #子弹出现在飞船的顶部中央
        self.y = float(self.rect.y)  #y坐标表示子弹的位置

    def update(self):
        self.y -= self.settings.bullet_speed   #子弹向上移动，y值按速度减少,x不变
        self.rect.y = self.y   #取整

    def draw_bullet(self):
        self.screen.blit(self.image,self.rect)



