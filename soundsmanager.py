import pygame

class SoundManager():
    """音效管理器"""

    def __init__(self):
        """初始化mixer与音效和背景音乐"""
        # 初始化mixer模块（不是实例化类）
        try:
            pygame.mixer.init(frequency=44100, size=-16, channels=2, buffer=512)
            self.mixer_initialized = True
        except pygame.error as e:
            print(f"初始化音频系统失败: {e}")
            self.mixer_initialized = False
            return
        
        # 音效缓存字典
        self.sounds = {}
        
        # 加载音效和音乐
        self._load_sounds()
        self._load_music()
        
        # 背景音乐可用标志
        self.music_available = True

    def _load_sounds(self):
        """加载音效"""
        # 定义要加载的音效列表
        sound_files = {
            'shoot': 'alien_invasion/sounds/shoot.WAV',
            'explosion': 'alien_invasion/sounds/explosion.wav', 
            'hit': 'alien_invasion/sounds/hit.wav',
            'game_over': 'alien_invasion/sounds/game_over.wav'
        }
        
        for name, path in sound_files.items():
            try:
                # 使用 pygame.mixer.Sound 类加载音效
                sound = pygame.mixer.Sound(path)
                self.sounds[name] = sound
                print(f"成功加载音效: {name}")
            except (pygame.error, FileNotFoundError) as e:
                print(f"加载音效失败 {name}: {e}")
                # 创建虚拟音效替代
                self._create_dummy_sound(name)
    
    def _create_dummy_sound(self, name):
        """创建虚拟音效"""
        try:
            # 创建一个非常短的声音（避免完全静音）
            # 注意：Sound构造函数需要有效的音频数据
            # 这里创建一个0.01秒的静音（44.1kHz * 0.01s = 441个采样点）
            # 立体声：2个声道，每个采样2字节（16位）
            silent_buffer = bytes([0] * (441 * 2 * 2))  # 441采样 * 2声道 * 2字节
            sound = pygame.mixer.Sound(buffer=silent_buffer)
            self.sounds[name] = sound
            print(f"为 {name} 创建了虚拟音效")
        except Exception as e:
            print(f"创建虚拟音效失败: {e}")
            self.sounds[name] = None

    def _load_music(self):
        """加载背景音乐"""
        if not self.mixer_initialized:
            return
            
        try:
            # pygame.mixer.music 是模块级别的对象
            pygame.mixer.music.load('alien_invasion/music/background.MP3')
            pygame.mixer.music.set_volume(0.3)
            print("成功加载背景音乐")
        except (pygame.error, FileNotFoundError) as e:
            print(f"加载背景音乐失败: {e}")
            self.music_available = False
        else:
            self.music_available = True

    def play_sound(self, name, volume=None):
        """播放指定音效"""
        if not self.mixer_initialized:
            return False
            
        if name in self.sounds and self.sounds[name] is not None:
            sound = self.sounds[name]
            if volume is not None:
                sound.set_volume(volume)
            sound.play()
            return True
        else:
            print(f"音效 {name} 不存在或加载失败")
            return False

    def play_music(self, loops=-1, start=0.0):
        """播放背景音乐"""
        if not self.mixer_initialized or not self.music_available:
            return False
            
        try:
            pygame.mixer.music.play(loops=loops, start=start)
            return True
        except pygame.error as e:
            print(f"播放音乐失败: {e}")
            return False

    def stop_music(self):
        """停止背景音乐"""
        if self.mixer_initialized:
            pygame.mixer.music.stop()

    def pause_music(self):
        """暂停背景音乐"""
        if self.mixer_initialized:
            pygame.mixer.music.pause()

    def unpause_music(self):
        """恢复背景音乐"""
        if self.mixer_initialized:
            pygame.mixer.music.unpause()

    def set_music_volume(self, volume):
        """设置背景音乐音量"""
        if not self.mixer_initialized:
            return
            
        if 0.0 <= volume <= 1.0:
            pygame.mixer.music.set_volume(volume)
        else:
            print(f"音量值 {volume} 无效，应在0.0到1.0之间")

    def set_sound_volume(self, name, volume):
        """设置指定音效的音量"""
        if not self.mixer_initialized:
            return
            
        if name in self.sounds and self.sounds[name] is not None:
            if 0.0 <= volume <= 1.0:
                self.sounds[name].set_volume(volume)
            else:
                print(f"音量值 {volume} 无效，应在0.0到1.0之间")

    def is_music_playing(self):
        """检查背景音乐是否正在播放"""
        if not self.mixer_initialized:
            return False
        return pygame.mixer.music.get_busy()

    def get_sound(self, name):
        """获取指定音效对象"""
        return self.sounds.get(name)