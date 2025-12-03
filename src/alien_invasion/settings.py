class Settings:
    def __init__(self):   #初始化控制游戏外观和飞船速度
        self.screen_width = 1187
        self.screen_height = 750
        #self.bg_color = (230,230,230)   #因为用了背景图片，所以用不着配色了

        self.ship_limit = 2   # 左上角剩余飞船数量限额
        self.fleet_drop_speed = 10     #舰队向下移动的速度不变
        self.speedup_scale = 1.3   #设置游戏加快的节奏
        self.score_scale = 1.5    #设置外星人分值提高的速度

        self.initialize_dynamic_settings()   #下面专门进行速度初始化设置

    def initialize_dynamic_settings(self):    #统一初始设置
        self.ship_speed = 5
        self.bullet_speed = 3
        self.alien_speed = 5
        self.fleet_direction = 1   #外星人向右移动为1，向左移动为-1
        self.alien_points = 50    #击落一个外星人得50分

    def increase_speed(self):    #设置速度加快的方法,在一波外星人舰队被消灭后触发
        self.ship_speed *= self.speedup_scale       #飞船移动加快
        self.alien_speed *= self.speedup_scale      #外星人移动加快
        self.bullet_speed *= self.speedup_scale     #子弹速度加快
        self.alien_points = int(self.alien_points * self.score_scale)  #分值取整



