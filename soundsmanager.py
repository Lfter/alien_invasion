import pygame
import os

class SoundManager:
    """管理游戏音效的类"""
    
    def __init__(self):
        """初始化音效管理器"""
        pygame.mixer.init()
        self.sounds = {}
        self.current_music = None
        
    def load_sound(self, name, filepath):
        """加载音效"""
        try:
            sound = pygame.mixer.Sound(filepath)
            self.sounds[name] = sound
        except Exception:
            self.sounds[name] = None
    
    def play_sound(self, name):
        """播放音效"""
        if name in self.sounds and self.sounds[name]:
            self.sounds[name].play()
    
    def play_music(self, filepath=None, loops=-1):
        """播放背景音乐"""
        if filepath:
            try:
                pygame.mixer.music.load(filepath)
                pygame.mixer.music.play(loops)
                self.current_music = filepath
            except Exception:
                pass
    
    def stop_music(self):
        """停止背景音乐"""
        pygame.mixer.music.stop()