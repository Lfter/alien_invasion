import pygame
from pygame.sprite import Sprite

class Ship(Sprite):
    """管理飞船的类"""
    
    def __init__(self, ai_game):
        """初始化飞船并设置其初始位置"""
        super().__init__()
        self.screen = ai_game.screen
        self.settings = ai_game.settings
        self.screen_rect = ai_game.screen.get_rect()
        
        # 加载飞船图形并获取其外接矩形
        # 使用settings中的get_resource_path方法
        image_path = self.settings.get_resource_path('images/ship.bmp')
        self.image = pygame.image.load(image_path)
        self.rect = self.image.get_rect()

        # 每艘新飞船都放在屏幕底部的中央
        self.rect.midbottom = self.screen_rect.midbottom
        
        # 在飞船属性x和y中设置浮点数
        self.x = float(self.rect.x)
        self.y = float(self.rect.y)
        
        # 移动标志（飞船一开始不移动）
        self.moving_right = False
        self.moving_left = False
        self.moving_up = False
        self.moving_down = False
        
    def update(self):
        """根据标志调整飞船的位置"""
        # 更新飞船的属性x和y的值
        if self.moving_right and self.rect.right < self.screen_rect.right:
            self.x += self.settings.ship_speed
            self._ship_speed()
            if not self.moving_right:
                self.x += self.settings.ship_speed
                self._ship_speed_slow()
        if self.moving_left and self.rect.left > 0:
            self.x -= self.settings.ship_speed
            self._ship_speed()
            if not self.moving_left:
                self.x -= self.settings.ship_speed
                self._ship_speed_slow()
        if self.moving_up and self.rect.top > 0:
            self.y -= self.settings.ship_speed
            self._ship_speed()
            if not self.moving_up:
                self.y -= self.settings.ship_speed
                self._ship_speed_slow()
        if self.moving_down and self.rect.bottom < self.screen_rect.bottom:
            self.y += self.settings.ship_speed
            self._ship_speed()
            if not self.moving_down:
                self.y += self.settings.ship_speed
                self._ship_speed_slow()

        # 根据self.x和self.y更新rect对象
        self.rect.x = int(self.x)
        self.rect.y = int(self.y)

    def _ship_speed(self):
        """更新飞船的速度"""
        if self.settings.ship_speed <= self.settings.ship_speed_max:
            self.settings.ship_speed += self.settings.ship_acceleration

    def _ship_speed_slow(self):
        """减慢飞船的速度"""
        if self.settings.ship_speed > 0:
            self.settings.ship_speed -= self.settings.ship_obstruction

    def blitme(self):
        """在指定位置绘制飞船"""
        self.screen.blit(self.image, self.rect)

    def center_ship(self):
        """将飞船放在屏幕底部的中央"""
        self.rect.midbottom = self.screen_rect.midbottom
        self.x = float(self.rect.x)
        self.y = float(self.rect.y)