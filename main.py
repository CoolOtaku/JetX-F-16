import os
import sys
import threading

import pygame
import platform

from src import Const
from src.GameSettings import GameSettings
from src.ScreenManager import ScreenManager
from src.Сommand import process_command


def run_commands():
    while Const.IS_RUNNING:
        user_input = input('Enter command: ')
        process_command(user_input)


def exit_game():
    Const.IS_RUNNING = False
    pygame.quit()
    sys.exit()


if __name__ == '__main__':
    pygame.init()
    Const.CLOCK = pygame.time.Clock()
    Const.FPS = 60

    Const.PATH = os.path.abspath('.') + '/'

    Const.SETTINGS = GameSettings()
    Const.SETTINGS.load_settings()
    Const.ANDROID_GUI = False
    Const.GAME_DURATION = 10 * 60
    Const.VIEW_FPS = False
    Const.SPAWN_INTERVAL = 8000

    pygame.mixer.init()
    pygame.mixer.music.load(Const.PATH + 'assets/sounds/bg_music.mp3')
    pygame.mixer.music.set_volume(Const.SETTINGS.volume_music)
    if Const.SETTINGS.volume_music != 0.0:
        pygame.mixer.music.play(-1)
    Const.HOVER_SOUND = pygame.mixer.Sound(Const.PATH + 'assets/sounds/hover_sound.mp3')
    Const.HOVER_SOUND.set_volume(Const.SETTINGS.volume_all)
    Const.SHOOT_SOUND_BULLET = pygame.mixer.Sound(Const.PATH + 'assets/sounds/shoot_bullet_sound.mp3')
    Const.SHOOT_SOUND_BULLET.set_volume(Const.SETTINGS.volume_all)
    Const.EXPLOSION_SOUND = pygame.mixer.Sound(Const.PATH + 'assets/sounds/explosion.mp3')
    Const.EXPLOSION_SOUND.set_volume(Const.SETTINGS.volume_all)
    Const.INFRARED_SOUND = pygame.mixer.Sound(Const.PATH + 'assets/sounds/infrared.mp3')
    Const.INFRARED_SOUND.set_volume(Const.SETTINGS.volume_all)
    Const.ROCKET_SOUND = pygame.mixer.Sound(Const.PATH + 'assets/sounds/rocket.mp3')
    Const.ROCKET_SOUND.set_volume(Const.SETTINGS.volume_all)

    Const.SCREEN_WIDTH = 1280
    Const.SCREEN_HEIGHT = 720
    Const.SCREEN = pygame.display.set_mode((Const.SCREEN_WIDTH, Const.SCREEN_HEIGHT))

    if platform.system() == 'Android':
        Const.SETTINGS.fullscreen = True
    if Const.SETTINGS.fullscreen:
        Const.SCREEN = pygame.display.set_mode(
            (Const.SCREEN_WIDTH, Const.SCREEN_HEIGHT), pygame.FULLSCREEN
        )

    pygame.display.set_caption('JetX✈F-16')
    Const.ICON = pygame.image.load(Const.PATH + 'assets/images/icon.png').convert_alpha()
    pygame.display.set_icon(Const.ICON)
    pygame.mouse.set_visible(False)

    Const.SCREEN_MANAGER = ScreenManager()
    Const.IS_RUNNING = True

    command_thread = threading.Thread(target=run_commands)
    command_thread.start()

    while Const.IS_RUNNING:
        time_delta = Const.CLOCK.tick(Const.FPS)

        Const.MOUSE_POS = pygame.mouse.get_pos()
        Const.SCREEN_MANAGER.events()

        Const.SCREEN.fill((255, 255, 255))
        Const.SCREEN_MANAGER.update(time_delta)

        pygame.display.update()
