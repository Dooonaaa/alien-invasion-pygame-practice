import sys
from time import sleep  #从time模块导入sleep()函数，让飞船被撞后游戏暂停一会儿
import pygame
from settings import Settings
from game_stats import GameStats
from ship import Ship
from bullet import Bullet
from alien import Alien
from button import Button
from scoreboard import Scoreboard



class AlienInvasion:
    def __init__(self):   #初始化状态
        pygame.init()
        self.clock = pygame.time.Clock()
        self.settings = Settings()   #创建实例
        self.screen = pygame.display.set_mode(
            (self.settings.screen_width,self.settings.screen_height))  #不是直接传数值
        self.screen_rect = self.screen.get_rect()
        pygame.display.set_caption("Alien Invasion")
        self.bg_image = pygame.image.load('images/background.jpg')  #使用背景图
        self.game_active = False    #刚开始处于非活跃状态，点击play后才开始游戏
        self.game_over = False    #游戏结束状态初始为否
        self.paused = False   #初始暂停为否
        self.play_button = Button(self,'Play')   #创建开始按钮，但不是显示

        self.stats = GameStats(self)          #创建统计游戏状态信息的实例
        self.sb = Scoreboard(self)            #创建记分牌实例
        self.ship = Ship(self)                #创建飞船实例
        self.bullets = pygame.sprite.Group()  #创建子弹编组
        self.aliens = pygame.sprite.Group()   #创建外星人编组
        self._create_fleet()                  #创建外星人舰队
        self.restart_button = Button(self, 'Restart')   #再来一局的按钮
        self.quit_button = Button(self, 'Quit')         #退出的按钮
        self.restart_button.rect.center = self.screen_rect.center
        self.quit_button.rect.midtop = self.restart_button.rect.midbottom

        # 音效
        self.laser_sound = pygame.mixer.Sound("sounds/fire1.mp3")
        self.laser_sound.set_volume(0.7)  # 设置音量

        self.gameover_sound = pygame.mixer.Sound("sounds/game_over.wav")
        self.gameover_sound.set_volume(0.7)  # 可根据需要调节音量





    def run_game(self):   #游戏主循环
        while True:   #侦听键盘和鼠标事件
            self._check_events()    #输入检测一直存在
            if self.game_active and not self.paused:    #游戏处于活跃非暂停状态才运行
                self.ship.update()
                self._update_bullets()
                self._update_aliens()
            self._update_screen()
            self.clock.tick(60)   #游戏帧率设为60

    def _check_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.mixer.music.stop()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                self._check_keydown_events(event)
            elif event.type == pygame.KEYUP:
                self._check_keyup_events(event)
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                if self.play_button.rect.collidepoint(mouse_pos):
                    self._check_play_button(mouse_pos)
                elif self.restart_button.rect.collidepoint(mouse_pos):
                    self._check_restart_button(mouse_pos)
                elif self.quit_button.rect.collidepoint(mouse_pos):
                    pygame.mixer.music.stop()
                    sys.exit()

    def _check_play_button(self, mouse_pos):
        if self.play_button.rect.collidepoint(mouse_pos) and not self.game_active:
            self._start_new_game()

    def _check_keydown_events(self,event):   #辅助方法，按下按键
        if event.key == pygame.K_RIGHT:      #当按键为→时
            self.ship.moving_right = True    #右移表示变为真
        elif event.key == pygame.K_LEFT:     #当按键为←时
            self.ship.moving_left = True     #左移标志变为真
        elif event.key == pygame.K_q:        #当按键为q时
            pygame.mixer.music.stop()
            sys.exit()                       #结束游戏
        elif event.key == pygame.K_SPACE:    #当按下空格键
            self._fire_bullet()              #开火
        elif event.key == pygame.K_p:        #当按下p键
            if self.game_active and not self.game_over :
                self.paused = not self.paused    #暂停与继续状态互换
                print(f"Paused: {self.paused}")
                if self.paused:
                    pygame.mixer.music.pause()     #音乐暂停
                else:
                    pygame.mixer.music.unpause()   #音乐继续

    def _check_keyup_events(self,event):    #辅助方法，释放按键
        if event.key == pygame.K_RIGHT:      #右移键释放后，右移标志归零
            self.ship.moving_right = False
        elif event.key == pygame.K_LEFT:     #左移键释放后，左移标志归零
            self.ship.moving_left = False

    def _fire_bullet(self):    #管理开火操作的方法
        new_bullet = Bullet(self)    #创建子弹

        self.bullets.add(new_bullet)
        self.laser_sound.play()  # 播放发射音效

    def _update_bullets(self):    #管理子弹位置的方法
        self.bullets.update()
        #删除消失的子弹
        for bullet in self.bullets.copy():
            if bullet.rect.bottom <= 0:   #子弹超过上边界
                self.bullets.remove(bullet)    #从编组bullets中删除子弹
            #print(len(self.bullets))   只是为了检查，不运行太慢了
        self._check_bullet_alien_collisions()    #单拎出来，碰撞检测和舰队重置

    def _create_fleet(self):   #创建外星人舰队
        alien = Alien(self)   #创建Alien实例，名为alien
        alien_width = alien.rect.width   #外星人之间的间距为外星人的宽度
        alien_height = alien.rect.height  #间隔为外星人的高度
        num_aliens_per_row = 7   #列数最多为7
        num_rows = 4   #只设4行外星人
        for row in range(num_rows):
            current_x = alien_width  # 投放外星人的位置
            alien_count = 0
            top_offset = 70
            while (current_x < (self.settings.screen_width - 2 * alien_width)
                    and alien_count < num_aliens_per_row):  #控制外星人数量
                self._create_alien(current_x,top_offset + row * 2 * alien_height)    #用方法创建外星人
                current_x += 2.5 * alien_width #更新下个外星人投放位置的横坐标
                alien_count += 1   #外星人数量+1

    def _update_aliens(self):
        self._check_fleet_edges()
        self.aliens.update()
        if pygame.sprite.spritecollideany(self.ship, self.aliens):
            #print("Ship hit!!!")      #调试用，不运行
            self._ship_hit()    #飞船被撞毁后，游戏状态重置
        self._check_aliens_bottom()   #检查是否有外星人到达屏幕下边缘

    def _check_fleet_edges(self):
        for alien in self.aliens.sprites():
            if alien.check_edges():
                self._change_fleet_direction()
                break

    def _change_fleet_direction(self):
        for alien in self.aliens.sprites():
            alien.rect.y += self.settings.fleet_drop_speed
        self.settings.fleet_direction *= -1   #乘-1相当于倒转方向,在for完成后执行

    def _create_alien(self,x_positon,y_position):  #在指定位置创建外星人的方法
        new_alien = Alien(self)  #创建新外星人
        new_alien.x = x_positon    #初始位置
        new_alien.rect.x = x_positon    #外星人矩形框位置
        new_alien.rect.y = y_position
        self.aliens.add(new_alien)    #加入编组

    def _check_bullet_alien_collisions(self):
        collisions = pygame.sprite.groupcollide(
            self.bullets, self.aliens, True, True)   #碰撞检测

        if collisions:
            for aliens in collisions.values():    #被一颗子弹击中的不是一个外星人，而是外星人列表
                self.stats.score += self.settings.alien_points * len(aliens)  #对击落的每个外星人，更新得分值
            self.sb.prep_score()    #创建新得分的图像
            self.sb.check_high_score()  #每击落一个就检查是否产生最高分

        if not self.aliens:  # 当一整支舰队完全被消灭后
            self.bullets.empty()  # 清空屏幕上残留的旧子弹
            self._create_fleet()  # 重新生成新的舰队
            self.settings.increase_speed()   #当一波舰队被灭后，整体速度加快，提升了难度
            self.stats.level += 1   #等级+1
            self.sb.prep_level()   #显示更新后的等级

    def _update_screen(self):  # 更新屏幕的方法
        self.screen.blit(self.bg_image, (0, 0))   #这是我设的背景
        for bullet in self.bullets.sprites():
            bullet.draw_bullet()
        self.ship.blitme()
        self.aliens.draw(self.screen)   #用draw让外星人现身
        self.sb.show_score()   #记分牌上显示得分
        if not self.game_active:
            if self.game_over:  #游戏结束状态时
                self._draw_game_over()    #就在屏幕绘制两个按钮

            else:
                self.play_button.draw_button()
        if self.paused:
            font = pygame.font.SysFont(None,72)
            pause_text = font.render("Paused",True,(255,255,0))
            pause_rect = pause_text.get_rect(center = self.screen.get_rect().center)
            self.screen.blit(pause_text,pause_rect)


        pygame.display.flip()  # 让最近绘制的屏幕可见

    def _ship_hit(self):
        if self.stats.ships_left > 0:   #在飞船数有盈余的情况下
             self.stats.ships_left -= 1   #飞船数减少一个
             self.sb.prep_ships()        #剩余飞船数显示减少
             self.bullets.empty()        #子弹清屏
             self.aliens.empty()         #外星人清屏
             self._create_fleet()        #舰队重置
             self.ship.center_ship()     #新飞船重置
             sleep(0.5)                  #短暂停止
        else:                            #飞船数为0时再撞击就game over
             self.game_active = False    #游戏活动状态为否
             self.game_over = True       #游戏结束状态为真
             pygame.mixer.music.stop()  # 背景音乐结束
             pygame.mouse.set_visible(True)   #game over 后，光标重新显示
             self.gameover_sound.play()

    def _check_aliens_bottom(self):
        for alien in self.aliens.sprites():
            if alien.rect.bottom >= self.settings.screen_height:
                self._ship_hit()
                break

    def _draw_game_over(self):
        if not self.game_over:
            return
        #设置Game Over字样在屏幕正中间偏上一点
        font = pygame.font.SysFont(None,64)
        msg_image = font.render("Game Over", True,(255,0,0))
        msg_rect = msg_image.get_rect()
        msg_rect.centerx = self.screen_rect.centerx
        msg_rect.top = self.screen_rect.centery - 100

        self.screen.blit(msg_image, msg_rect)
        #设置再来一局按钮
        self.restart_button.rect.centerx = self.screen_rect.centerx
        self.restart_button.rect.top = msg_rect.bottom + 30
        self.restart_button._prep_msg("Restart")
        self.restart_button.draw_button()
        # 设置结束游戏按钮
        self.quit_button.rect.centerx = self.screen_rect.centerx
        self.quit_button.rect.top = self.restart_button.rect.bottom + 20
        self.quit_button._prep_msg("Quit")
        self.quit_button.draw_button()

    def _check_restart_button(self,mouse_pos):
        if self.restart_button.rect.collidepoint(mouse_pos):
            self._start_new_game()

    def _start_new_game(self):
        # 播放 / 重启 BGM
        pygame.mixer.music.stop()
        pygame.mixer.music.load('sounds/bgm.wav')
        pygame.mixer.music.set_volume(0.6)
        pygame.mixer.music.play(-1)

        # 重置动态设置
        self.settings.initialize_dynamic_settings()

        # 重置游戏状态
        self.stats.reset_stats()
        self.sb.prep_score()
        self.sb.prep_level()
        self.sb.prep_ships()

        # 清空并重新生成对象
        self.bullets.empty()
        self.aliens.empty()
        self._create_fleet()
        self.ship.center_ship()

        # 状态切换
        self.game_over = False
        self.game_active = True
        pygame.mouse.set_visible(False)


if __name__ == '__main__':
    ai = AlienInvasion()  # 创建游戏实例
    ai.run_game()  # 运行

