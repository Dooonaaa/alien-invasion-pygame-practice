import pygame.font
class Button:    #设置按钮类， 使用了三次创建实例，play, restart, quit
    def __init__(self,ai_game, msg):
        self.screen = ai_game.screen    #需要把按钮画在屏幕上
        self.screen_rect = self.screen.get_rect()   #需要从屏幕获取矩形框区域

        self.width, self.height = 200,50   #设置文本框的尺寸
        self.button_color = (255,165,0)   #按钮框背景设为橙色
        self.text_color = (255,255,255)   #文本设为白色
        self.font = pygame.font.SysFont(None,48)   #创建字体

        self.rect = pygame.Rect(0,0,self.width,self.height)   #创建矩形区域
        self.rect.center = self.screen_rect.center

        self._prep_msg(msg)

    def _prep_msg(self, msg): #使用了两次，restart, quit  #把文字渲染成图像
        self.msg_image = self.font.render(msg,True, self.text_color,
                                          self.button_color)
        self.msg_image_rect = self.msg_image.get_rect()
        self.msg_image_rect.center = self.rect.center

    def draw_button(self):   #使用了三次，play, restart, quit
        self.screen.fill(self.button_color,self.rect)   #给矩形框填充颜色
        self.screen.blit(self.msg_image,self.msg_image_rect)   #把文字图像渲染到指定位置



