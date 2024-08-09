import pygame
import time
import random
import json

from core.Map import Map
from core.models.Ka_50 import Ka_50
from core.models.Pantsir_S1 import Pantsir_S1
from core.models.Plane import Plane

from src import Const
from src.EndGameScreen import EndGameScreen
from src.Statistics import Statistics


class Game:
    def __init__(self, map_folder):
        self.player = Plane(self)
        self.map = Map(map_folder, self.player)
        self.is_started = False
        self.start_time = time.time()
        self.last_enemy_spawn_time = pygame.time.get_ticks()
        self.bullets = []
        self.rockets = []
        self.enemies = []
        self.sprites = []
        self.current_timer_time = 20000

        self.current_statistics = Statistics()
        if Const.SETTINGS.locale == 'en':
            pathText = Const.PATH + 'data/translations/strings.en.json'
        else:
            pathText = Const.PATH + 'data/translations/strings.uk.json'

        with open(pathText, 'r') as f:
            localization_data = json.load(f)
        self.message_text = localization_data[Const.SETTINGS.locale]['message_window_text']

    def update(self, time_delta):
        self.map.update(time_delta)

        if self.bullets:
            for bullet in self.bullets:
                bullet.update()

        if self.enemies:
            for unit in self.enemies:
                unit.update(time_delta)

        self.player.update(time_delta)

        if self.sprites:
            for sprite in self.sprites:
                sprite.update()

        if self.rockets:
            for rocket in self.rockets:
                rocket.update()

        if not self.is_started:
            self.player.body.set_y(self.player.body.get_y() - 1)
            if self.player.body.get_y() <= (Const.SCREEN_HEIGHT / 2):
                self.player.body.set_y(Const.SCREEN_HEIGHT / 2)
                self.is_started = True
        else:
            current_time = pygame.time.get_ticks()
            if current_time - self.last_enemy_spawn_time >= Const.SPAWN_INTERVAL:
                if random.random() < 40 / 100:
                    if self.map.is_two_types_of_enemies and random.random() < 50 / 100:
                        self.enemies.append(Pantsir_S1(self))
                    else:
                        self.enemies.append(Ka_50(self))
                self.last_enemy_spawn_time = current_time

        if self.player is None:
            return

        if self.player.body.get_y() < 0 or self.player.body.get_y() > Const.SCREEN_HEIGHT:
            if not Const.SCREEN_MANAGER.ACTIVE_SCREEN.message_window.visible:
                Const.SCREEN_MANAGER.ACTIVE_SCREEN.message_window.show()
            self.current_timer_time -= time_delta
            current_time_str = ' {:.1f}'.format(self.current_timer_time / 1000)
            Const.SCREEN_MANAGER.ACTIVE_SCREEN.message_window.text_block.clear()
            Const.SCREEN_MANAGER.ACTIVE_SCREEN.message_window.text_block.append_html_text(self.message_text)
            Const.SCREEN_MANAGER.ACTIVE_SCREEN.message_window.text_block.append_html_text(current_time_str)
            if self.current_timer_time <= 0:
                self.player.health = 0
        elif 0 < self.player.body.get_y() < Const.SCREEN_HEIGHT:
            if Const.SCREEN_MANAGER.ACTIVE_SCREEN.message_window.visible:
                Const.SCREEN_MANAGER.ACTIVE_SCREEN.message_window.hide()
                self.current_timer_time = 20000

        if time.time() - self.start_time >= Const.GAME_DURATION:
            self.end_game(True)

    def end_game(self, is_win):
        Const.SCREEN_MANAGER.start_screen(EndGameScreen(is_win, self.current_statistics, self.map.map_folder))
        self.player = None
        self.map = None
        self.bullets.clear()
        self.rockets.clear()
        self.enemies.clear()
        self.sprites.clear()

    def get_remaining_time(self):
        remaining_seconds = self.start_time + Const.GAME_DURATION - time.time()
        remaining_minutes, remaining_seconds = divmod(remaining_seconds, 60)
        return "{:02}:{:02}".format(int(remaining_minutes), int(remaining_seconds))
