import pygame.font
from pygame.sprite import Group
from ship import Ship
class Scoreboard:
    def __init__(self,ai_game):
        self.ai_game = ai_game          #让当前对象可以使用ai_game中的属性和对象
        self.screen = ai_game.screen    #要把记分牌画在屏幕上
        self.screen_rect = self.screen.get_rect()    #要在屏幕上画矩形框
        self.settings = ai_game.settings   #与历史最高分有关
        self.stats = ai_game.stats        #分数显示与游戏状态有关

        self.text_color = (255,255,255)    #文本为白色字体
        self.font = pygame.font.SysFont(None,36)   #默认字体，设置字号36

        self.prep_score()           #渲染当前得分的图像
        self.prep_high_score()      #渲染最高分的图像
        self.prep_level()           #渲染当前等级
        self.prep_ships()           #渲染显示剩余飞船数

    def prep_score(self):   #将得分渲染为图像
        rounded_score = round(self.stats.score, -1)   #保留到小数点前一位，即十位
        score_str = f"Score:{rounded_score:,}"   #得分显示为字符串，且以逗号作为千位分隔符
        self.score_image = self.font.render(score_str,True,
                                            self.text_color)
        #在屏幕右上角显示得分
        self.score_rect = self.score_image.get_rect()    #计分板的框
        self.score_rect.right = self.screen_rect.right - 20    #框的右边缘与屏幕右边缘隔20像素
        self.score_rect.top = 10   #框的上边缘与屏幕上边缘隔10像素

    def prep_high_score(self):
        high_score = round(self.stats.high_score, -1)
        high_score_str = f"High Score:{high_score: ,}"
        self.high_score_image = self.font.render(high_score_str,True,
                                                 self.text_color)
        self.high_score_rect = self.high_score_image.get_rect()
        self.high_score_rect.centerx = self.screen_rect.centerx
        self.high_score_rect.top = self.score_rect.top

    def prep_level(self):
        level_str = f"Level: {self.stats.level}"
        self.level_image = self.font.render(level_str,True,
                                            self.text_color)
        self.level_rect = self.level_image.get_rect()
        self.level_rect.right = self.score_rect.right
        self.level_rect.top = self.score_rect.bottom + 10

    def prep_ships(self):
        self.ships = Group()   #空编组
        for ship_number in range(self.stats.ships_left):
            ship = Ship(self.ai_game)
            ship.rect.x = 10 + ship_number * ship.rect.width
            ship.rect.y = 10
            self.ships.add(ship)

    def show_score(self):   #逐个设置属性，一起显示
        self.screen.blit(self.score_image,self.score_rect)  #blit(图像，位置)
        self.screen.blit(self.high_score_image,self.high_score_rect)   #显示最高分
        self.screen.blit(self.level_image,self.level_rect)   #显示等级
        self.ships.draw(self.screen)   #显示剩下的飞船数

    def check_high_score(self):   #对比检查是否产生了新的最高分，触发时机为每次击落外星人时
        if self.stats.score > self.stats.high_score:
            self.stats.high_score = self.stats.score
            self.prep_high_score()











