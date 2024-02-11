import pygame

from pygame.sprite import Sprite


class Alien(Sprite):
    def __init__(self,ai_game):
        # 初始化
        super().__init__()
        # 加载图片并设置初始位置
        self.screen = ai_game.screen
        self.setting = ai_game.setting
        self.image = pygame.image.load('image/alien.bmp')
        self.rect = self.image.get_rect()
        # 位置信息
        self.rect.x = self.rect.width
        self.rect.y = self.rect.height
        self.x = float(self.rect.x)
        self.y = float(self.rect.y)

    def check_edges(self):
        # 检查边缘
        screen_rect = self.screen.get_rect()
        if self.rect.right >= screen_rect.right or self.rect.left <= 0:
            return True

    def update(self):
        self.x += (self.setting.alien_speed *
                    self.setting.fleet_direction)
        self.rect.x = self.x



