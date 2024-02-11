import pygame
import sys

from time import sleep
from setting import Setting
from ship import Ship
from bullet import Bullet
from alien import Alien
from gamestats import GameStats
from button import Button
from scoreboard import Scoreboard


class AlienInvasion:
    """管理游戏的类"""
    def __init__(self):
        # 初始化
        pygame.init()
        # 设置初始化
        self.setting = Setting()
        # 放屏幕
        self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        self.setting.screen_width = self.screen.get_rect().width
        self.setting.screen_height = self.screen.get_rect().height
        # 标题
        pygame.display.set_caption('AlienInvasion')
        self.clock = pygame.time.Clock()
        self.ship = Ship(self)
        # 子弹的编组
        self.bullets = pygame.sprite.Group()
        # 外星人的飞船
        self.aliens = pygame.sprite.Group()
        self._create_fleet()
        # 重置信息
        self.stats = GameStats(self)
        # 游戏是否进行
        self.game_active = False
        # 创建按键
        self.play_button = Button(self, "play")
        # 创建记分牌
        self.sb = Scoreboard(self)

    def run_game(self):
        while True:
            self._check_events()

            if self.game_active:
                self.ship.update()
                self._update_bullet()
                self._update_fleet()

            self._update_screen()
            self.clock.tick(60)

    def _check_events(self):
        # 处理事件
        for event in pygame.event.get():
            if event.type == pygame.QUIT :
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                self._check_keydown_event(event)
            elif event.type == pygame.KEYUP:
                self._check_keyup_event(event)
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                self._check_play_button(mouse_pos)

    def _check_play_button(self, mouse_pos):
        # 检查开始游戏的按钮
        button_clicked = self.play_button.rect.collidepoint(mouse_pos)
        if button_clicked and not self.game_active:
            self._stats_game()
            pygame.mouse.set_visible(False)
            self.stats.reset_stats()
            self.sb.prep_score()
            self.sb.prep_level()

    def _stats_game(self):
        """开始新游戏"""
        self.stats.reset_stats()
        self.game_active = True
        self.aliens.empty()
        self.bullets.empty()
        self._create_fleet()
        self.ship.center_ship()
        self.setting.initialize_dynamic_settings()

    def _check_keydown_event(self,event):
        # 获取键盘的事件
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = True
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = True
        elif event.key == pygame.K_q:
            sys.exit()
        elif event.key == pygame.K_p:
            self._stats_game()
        elif event.key == pygame.K_SPACE:
            self._fire_bullet()

    def _check_keyup_event(self, event):
        # 获取合适松开键盘
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = False
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = False

    def _fire_bullet(self):
        # 开火
        if len(self.bullets) < self.setting.bullet_allowed:
            new_bullet=Bullet(self)
            self.bullets.add(new_bullet)

    def _update_bullet(self):
        # 子弹的更新
        self.bullets.update()
        for bullet in self.bullets.copy():
            if bullet.rect.bottom < 0:
                self.bullets.remove(bullet)
        self._check_bullet_alien_collisions()

    def _check_bullet_alien_collisions(self):
        # 检查子弹和外星人是否碰撞
        collisions = pygame.sprite.groupcollide(
            self.bullets, self.aliens, True, True
        )
        if collisions:
            for aliens in collisions.values():
                self.stats.score += self.setting.alien_points * len(aliens)
            self.sb.prep_score()
            self.sb.check_high_score()
        if not self.aliens:
            self.bullets.empty()
            self._create_fleet()
            self.setting.increase_speed()
            self.stats.level += 1
            self.sb.prep_level()
            #self.sb.score += 1

    def _create_fleet(self):
        # 创造舰队
        alien = Alien(self)
        alien_width,alien_height = alien.rect.size
        available_space_x = self.setting.screen_width - (2 * alien_width)
        number_aliens_x = available_space_x // (2*alien_width)
        ship_height = self.ship.rect.height
        available_space_y = (self.setting.screen_height -
                             (3 * alien_height) - ship_height)
        number_rows = available_space_y // (2 * alien_height)
        for row_number in range(number_rows):
            for alien_number in range(number_aliens_x):
                self._create_alien(alien_number, row_number)

    def _create_alien(self, alien_number,row_number):
        # 创建外星人
        alien = Alien(self)
        alien_width,alien_height = alien.rect.size
        alien.x = alien_width + 2 * alien_width * alien_number
        alien.rect.x = alien.x
        alien.rect.y = alien.rect.height + 2 * alien.rect.height * row_number
        self.aliens.add(alien)

    def _check_fleet_edges(self):
        # 检查舰队是否碰到屏幕边缘
        for alien in self.aliens.sprites():
            if alien.check_edges():
                self._chang_fleet_direction()
                break

    def _chang_fleet_direction(self):
        # 舰队到达屏幕边缘转向
        for alien in self.aliens.sprites():
            alien.rect.y += self.setting.fleet_drop_speed
        self.setting.fleet_direction *= -1

    def _update_fleet(self):
        # 更新舰队位置
        self._check_fleet_edges()
        self.aliens.update()
        # 检查外星人和飞船的碰撞
        if pygame.sprite.spritecollideany(self.ship,self.aliens):
            self._ship_hit()
        self._check_aliens_bottom()

    def _check_aliens_bottom(self):
        # 检查是否有外星人到达了屏幕的下边缘
        for alien in self.aliens.sprites():
            if alien.rect.bottom > self.setting.screen_height:
                self._ship_hit()
                break

    def _ship_hit(self):
        # 刷新游戏
        if self.stats.ships_left > 0:
            self.stats.ships_left -= 1
            self.sb.prep_ships()
            self.bullets.empty()
            self.aliens.empty()
            self._create_fleet()
            self.ship.center_ship()
            sleep(0.5)
        else:
            self.game_active = False
            pygame.mouse.set_visible(True)

    def _update_screen(self):
        # 每次循环都刷新屏幕
        self.screen.fill(self.setting.bg_color)
        self.ship.blitme()
        for bullet in self.bullets.sprites():
            bullet.draw_bullet()
        self.aliens.draw(self.screen)
        self.sb.show_score()
        if not self.game_active:
            self.play_button.draw_button()
        # 让最近绘制的屏幕可见
        pygame.display.flip()


if __name__ == '__main__':
    ai = AlienInvasion()
    ai.run_game()
