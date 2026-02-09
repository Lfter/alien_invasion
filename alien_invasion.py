import sys
from time import sleep
from pathlib import Path
import json
import pygame
from settings import Settings
from game_stats import GameStats
from scoreboard import Scoreboard
from button import Button
from ship import Ship
from bullet import Bullet
from alien import Alien
from soundsmanager import SoundManager

class AlienInvasion:
    """管理游戏资源和行为的类"""

    def __init__(self):
        """初始化游戏并创建游戏资源"""
        pygame.init()
        self.sound_manager = SoundManager()
        self.clock = pygame.time.Clock()
        self.settings = Settings()
        self.screen = pygame.display.set_mode(
            (self.settings.screen_width, self.settings.screen_height))
        pygame.display.set_caption("Alien Invasion")

        #创建储存游戏统计信息的实例，并创建记分牌
        self.high_score_json = Path("alien_invasion/high_score.json")
        self.stats = GameStats(self)

        #读取最高分json文件位置，读取最高分文档
        self._load_high_score()

        self.sb = Scoreboard(self)
        self.ship = Ship(self)
        self.bullets = pygame.sprite.Group()
        self.aliens = pygame.sprite.Group()
        self._create_fleet()
        # 开始游戏时播放背景音乐
        self.sound_manager.play_music(loops=-1)

        # 游戏启动在一开始处于非活动状态
        self.game_active = False

        #创建Play按钮
        self.play_button = Button(self,"Play")

    def run_game(self):
        """开始游戏的主循环"""
        while True:
            self._check_events()
            if self.game_active:
                self.ship.update()
                self._update_bullets()
                self._update_aliens()
            self._update_screen()
            self.clock.tick(60)
    
    def _check_events(self):
        """响应按键和鼠标事件"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                self._check_play_button(mouse_pos)
            elif event.type == pygame.KEYDOWN:
                self._check_keydown_events(event)
            elif event.type == pygame.KEYUP:
                self._check_keyup_events(event)

    def _check_play_button(self,mouse_pos):
        """在玩家单机Play按钮开始新游戏"""
        button_clicked = self.play_button.rect.collidepoint(mouse_pos)
        if button_clicked and not self.game_active:
            #重制游戏的统计信息
            self.stats.reset_stats()
            self.sb.prep_images()

            #还原游戏设置
            self.settings.initialize_dynamic_settings()
            self._start_game()
            
    def _start_game(self):
        #重置游戏的统计信息
        self.stats.reset_stats()
        self.game_active = True

        #清空外星人列表和子弹列表
        self._empty_aliens_bullets()

        #创建一个新的外星舰队，并将飞船放在屏幕底部的中央
        self._create_fleet()
        self.ship.center_ship()

        #隐藏光标
        pygame.mouse.set_visible(False)

    def _check_keydown_events(self, event):
        """响应按下"""
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = True
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = True
        elif event.key == pygame.K_UP:
            self.ship.moving_up = True
        elif event.key == pygame.K_DOWN:
            self.ship.moving_down = True
        elif event.key == pygame.K_SPACE:
            self._fire_bullet()
        elif event.key == pygame.K_p:
            self._start_game()
        elif event.key == pygame.K_q:
            sys.exit()

    def _check_keyup_events(self, event):
        """响应释放"""
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = False
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = False
        elif event.key == pygame.K_UP:
            self.ship.moving_up = False
        elif event.key == pygame.K_DOWN:
            self.ship.moving_down = False

    def _fire_bullet(self):
        """创建一颗子弹，并将其加入编组bullets"""
        if len(self.bullets) < self.settings.bullets_allowed:
            new_bullet = Bullet(self)
            self.bullets.add(new_bullet)
            self.sound_manager.play_sound('shoot')

    def _update_bullets(self):
        """更新子弹的位置并删除已消失的子弹"""
        # 更新子弹的位置
        self.bullets.update()
        
        # 删除已经消失的子弹
        for bullet in self.bullets.copy():
            if bullet.rect.bottom <= 0:
                self.bullets.remove(bullet)
        
        self._check_bullet_alien_collision()

    def _check_bullet_alien_collision(self):
        """响应子弹和外星人的碰撞"""
        # 检查是否有子弹击中了外星人
        # 如果是，就删除相应的子弹和外星人
        collisions = pygame.sprite.groupcollide(
            self.bullets, self.aliens, True, True)
        if collisions:
            for aliens in collisions.values():
                self.stats.score += self.settings.alien_points *len(aliens)
                self.sb.prep_score()
                self.sb.check_high_score()
                self.sound_manager.play_sound('explosion')

        if not self.aliens:
            # 删除所有现有的子弹并创建一个新的外星舰队
            self._start_new_level()

    def _start_new_level(self):
        """删除所有现有的子弹并创建一个新的外星舰队并提高等级"""
        self.bullets.empty()
        self._create_fleet()
        self.settings.increase_speed()
        self.stats.level += 1
        self.sb.prep_level()

    def _create_fleet(self):
        """创建一个外星舰队"""
        alien = Alien(self)
        alien_width, alien_height = alien.rect.size
        
        # 计算一行可以容纳多少外星人
        available_space_x = self.settings.screen_width - (2 * alien_width)
        number_aliens_x = available_space_x // (2 * alien_width)
        
        # 计算可以容纳多少行外星人
        ship_height = self.ship.rect.height
        available_space_y = (self.settings.screen_height - 
                            (3 * alien_height) - ship_height)
        number_rows = available_space_y // (2 * alien_height)
        
        # 创建外星人舰队
        for row_number in range(number_rows):
            for alien_number in range(number_aliens_x):
                self._create_alien(alien_number, row_number)

    def _create_alien(self, alien_number, row_number):
        """创建一个外星人并将其加入外星舰队"""
        alien = Alien(self)
        alien_width, alien_height = alien.rect.size
        
        alien.x = alien_width + 2 * alien_width * alien_number
        alien.rect.x = alien.x
        alien.rect.y = alien.rect.height + 2 * alien.rect.height * row_number
        self.aliens.add(alien)

    def _update_aliens(self):
        """更新外星舰队中外星人的位置"""
        self._check_fleet_edges()
        self.aliens.update()
        
        # 检测外星人和飞船之间的碰撞
        if pygame.sprite.spritecollideany(self.ship, self.aliens):
            self._ship_hit()
        
        # 检查是否有外星人到达了屏幕的下边缘
        self._check_aliens_bottom()

    def _ship_hit(self):
        """响应飞船和外星人的碰撞"""
        if self.stats.ships_left > 0:
            #将ships_left减1并更新记分牌
            self.stats.ships_left -= 1
            self.sb.prep_ships()
            
            # 清空外星人列表和子弹的列表
            self._empty_aliens_bullets()
            
            # 创建一个新的外星舰队，并将飞船放到屏幕底部的中央
            self._create_fleet()
            self.ship.center_ship()
            
            # 重置飞船的移动标志
            self._reset_ship_flag()

            #播放飞船被撞到的音效
            self.sound_manager.play_sound('hit')
            
            # 暂停
            sleep(0.3)
        else:
            self.game_active = False
            pygame.mouse.set_visible(True)
            self.game_over()

    def game_over(self):
        """游戏结束"""
        # 播放游戏结束音效
        self.sound_manager.play_sound('game_over')
        # 停止背景音乐
        self.sound_manager.stop_music()

    def _reset_ship_flag(self):
        """重置飞船的移动标志"""
        self.ship.moving_right = False
        self.ship.moving_left = False
        self.ship.moving_up = False
        self.ship.moving_down = False

    def _check_aliens_bottom(self):
        """检查是否有外星人到达了屏幕的下边缘"""
        screen_rect = self.screen.get_rect()
        for alien in self.aliens.sprites():
            if alien.rect.bottom >= screen_rect.bottom:
                # 像飞船被撞到时一样处理
                self._ship_hit()
                break

    def _check_fleet_edges(self):
        """在有外星人到达边缘时采取相应措施"""
        for alien in self.aliens.sprites():
            if alien.check_edges():
                self._change_fleet_direction()
                break

    def _change_fleet_direction(self):
        """将整个外星舰队向下移动并改变他们的方向"""
        for alien in self.aliens.sprites():
            alien.rect.y += self.settings.fleet_drop_speed
        self.settings.fleet_direction *= -1

    def _update_screen(self):
        """更新屏幕上的图像，并切换到新屏幕"""
        self.screen.fill(self.settings.bg_color)
        for bullet in self.bullets.sprites():
            bullet.draw_bullet()
        self.ship.blitme()
        self.aliens.draw(self.screen)
        #显示得分
        self.sb.show_score()

        #如果游戏处于非活跃状态，就绘制Play按钮
        if not self.game_active:
            self.play_button.draw_button()
        
        # 让最近绘制的屏幕可见
        pygame.display.flip()

    def _load_high_score(self):
        """从文件加载最高分"""
        try:
            if self.high_score_json.exists():
                with open(self.high_score_json, 'r') as f:
                    self.stats.high_score = json.load(f)
        except (json.JSONDecodeError, IOError):
            self.stats.high_score = 0

    def _save_high_score(self):
        """保存最高分到文件"""
        try:
            with open(self.high_score_json, 'w') as f:
                json.dump(self.stats.high_score, f)
        except IOError:
            pass

    def _empty_aliens_bullets(self):
        """清空外星人列表和子弹列表"""
        self.bullets.empty()
        self.aliens.empty()

if __name__ == '__main__':
    # 创建游戏实例并运行游戏1.0
    ai = AlienInvasion()
    ai.run_game()