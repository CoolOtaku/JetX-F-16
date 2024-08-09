import os

import pygame
import json

from src import Const


class GameSettings:
    def __init__(self):
        self.volume_all = 0.5
        self.volume_music = 0.5
        self.fullscreen = False
        self.locale = 'en'
        self.key_bindings = {
            'move_up': pygame.K_UP,
            'move_down': pygame.K_DOWN,
            'to_twist': pygame.K_SPACE,
            'machine_gun': pygame.BUTTON_LEFT,
            'rocket': pygame.BUTTON_RIGHT,
            'infrared_countermeasure': pygame.K_q
        }

    def load_settings(self):
        if os.path.exists(Const.PATH + 'data/settings.json'):
            with open(Const.PATH + 'data/settings.json', 'r') as file:
                settings_json = json.load(file)
                self.volume_all = settings_json.get('volume_all', self.volume_all)
                self.volume_music = settings_json.get('volume_music', self.volume_music)
                self.fullscreen = settings_json.get('fullscreen', self.fullscreen)
                self.locale = settings_json.get('locale', self.locale)
                self.key_bindings = settings_json.get('key_bindings', self.key_bindings)

    def save_settings(self):
        with open(Const.PATH + 'data/settings.json', 'w') as file:
            json.dump(self.to_json(), file)

    def to_json(self):
        return {
            'volume_all': self.volume_all,
            'volume_music': self.volume_music,
            'fullscreen': self.fullscreen,
            'locale': self.locale,
            'key_bindings': self.key_bindings
        }

    @staticmethod
    def get_key_name(key):
        res = pygame.key.name(key)
        if not res:
            if key == pygame.BUTTON_LEFT:
                return 'MOUSE LEFT'
            elif key == pygame.BUTTON_MIDDLE:
                return 'MOUSE MIDDLE'
            elif key == pygame.BUTTON_RIGHT:
                return 'MOUSE RIGHT'
            elif key == pygame.BUTTON_X1:
                return 'MOUSE X1'
            elif key == pygame.BUTTON_X2:
                return 'MOUSE X2'
        else:
            return res
