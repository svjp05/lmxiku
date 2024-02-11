import pygame
from pygame.sprite import Sprite

class Ship(Sprite):
    def __init__(self,ai_game):
        """初始化飞船并设置其属性"""
        super().__init__()
        self.screen = ai_game.screen
        self.setting = ai_game.setting
        self.screen_rect = ai_game.screen.get_rect()
        # 加载飞船图像并获取其矩形
        self.image = pygame.image.load('image/ship.bmp')
        self.rect = self.image.get_rect()
        # 每艘飞船都放在屏幕底部的中央
        self.rect.midbottom = self.screen_rect.midbottom
        # 添加持续移动的标志
        self.moving_right = False
        self.moving_left = False
        # 添加速度
        self.x = float(self.rect.x)

    def update(self):
        if self.moving_right and self.rect.right < self.screen_rect.right:
            self.x += self.setting.ship_speed
        if self.moving_left and self.rect.left > self.screen_rect.left:
            self.x -= self.setting.ship_speed
        self.rect.x = self.x

    def blitme(self):
        self.screen.blit(self.image,self.rect)

    def center_ship(self):
        self.rect.midbottom = self.screen_rect.midbottom
        self.x = float(self.rect.x)
