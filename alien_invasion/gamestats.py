class GameStats:
    def __init__(self,ai_game):
        self.setting = ai_game.setting
        self.reset_stats()
        self.high_score = 0

    def reset_stats(self):
        """初始化在游戏运行期间可能发生变化的信息"""
        self.ships_left = self.setting.ship_limit
        self.score = 0
        self.level = 1
