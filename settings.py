import os
import sys

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

        # ============ 智能查找资源路径 ============
        self.base_path = self._find_resource_path()
        
        # 初始化动态设置
        self.initialize_dynamic_settings()
    
    def _find_resource_path(self):
        """智能查找资源文件所在的目录"""
        possible_paths = [
            # 打包后的路径
            getattr(sys, '_MEIPASS', None),
            
            # 开发环境的各种可能路径
            os.path.dirname(os.path.abspath(__file__)),  # settings.py所在目录
            os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'),  # 上级目录
            '/Users/ltzz/Desktop/py/alien_invasion',  # 绝对路径
            os.path.join(os.path.expanduser('~'), 'Desktop', 'py', 'alien_invasion'),
        ]
        
        # 添加当前工作目录
        possible_paths.append(os.getcwd())
        
        for path in possible_paths:
            if path and os.path.exists(path):
                # 检查是否有images和sounds文件夹
                has_images = os.path.exists(os.path.join(path, 'images', 'ship.bmp'))
                has_sounds = os.path.exists(os.path.join(path, 'sounds', 'shoot.wav'))
                
                if has_images or has_sounds:
                    return path
        
        # 如果没有找到，返回当前文件所在目录
        fallback_path = os.path.dirname(os.path.abspath(__file__))
        return fallback_path
    
    def get_resource_path(self, relative_path):
        """获取资源文件的完整路径"""
        full_path = os.path.join(self.base_path, relative_path)
        if not os.path.exists(full_path):
            # 尝试在上级目录查找
            parent_dir = os.path.dirname(self.base_path)
            alt_path = os.path.join(parent_dir, relative_path)
            if os.path.exists(alt_path):
                return alt_path
        return full_path

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