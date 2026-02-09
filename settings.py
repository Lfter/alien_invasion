class Settings:
    """储存游戏《外星人入侵》中所有设置的类"""

    def __init__(self):
        # 屏幕设置
        self.screen_width = 1280
        self.screen_height = 720
        self.bg_color = (230, 230, 230)
        
        # 飞船设置
        self.ship_acceleration = 0.5
        self.ship_obstruction = 0.05
        self.ship_speed_max = 3
        self.ship_speed = 0
        self.ship_limit = 3
        
        # 子弹设置
        self.bullet_speed = 2.0
        self.bullet_width = 3
        self.bullet_height = 15
        self.bullet_color = (60, 60, 60)
        self.bullets_allowed = 3
        
        # 外星人设置
        self.alien_speed = 0.5  # 稍微减慢一点
        self.fleet_drop_speed = 10  # 减少下移距离
        # fleet_direction为1代表向右移动，为-1代表向左移动
        self.fleet_direction = 1

        #以什么速度加快游戏的节奏
        self.speedup_scale = 1.1

        #外星人分数的提高速度
        self.score_scale = 1.5
        self.initialize_dynamic_settings()

    def initialize_dynamic_settings(self):
        """初始化随着游戏进行而变化的设置"""
        self.ship_speed = 1.5
        self.bullet_speed = 2.5
        self.alien_speed = 0.5

        # fleet_direction为1代表向右移动，为-1代表向左移动
        self.fleet_direction = 1

        #记分设置
        self.alien_points = 50

    def increase_speed(self):
        """提高速度设置的值"""
        self.ship_speed *= self.speedup_scale
        self.bullet_speed *= self.speedup_scale
        self.alien_speed *= self.speedup_scale
        self.ship_acceleration = self.speedup_scale
        self.ship_speed_max *= self.speedup_scale

        self.alien_points = int(self.alien_points * self.score_scale)

        