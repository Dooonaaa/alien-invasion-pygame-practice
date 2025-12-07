class GameStats:
    #跟踪游戏状态

    def __init__(self,ai_game):  #初始化统计信息
        self.settings = ai_game.settings
        self.reset_stats()
        self.high_score = 0   #不会重置，出现更高分时更新


    def reset_stats(self):   #重置状态的方法
        self.ships_left = self.settings.ship_limit   #剩余飞船数量，初始为配额2
        self.score = 0  #在每次开始游戏时重置得分为0
        self.level = 1  # 玩家等级初始为1
