import os

import pygame
import json
import math

from src import Const


class Map:
    scroll_speed_mapping = {
        (15, -15, 360, 345): (3, 0, False),
        (195, 165, -195, -165): (3, 0, True),
        (105, 75, -285, -255): (0, 2.2, None),
        (285, 255, -105, -75): (0, -2.5, None),
        (45, 15, -345, -315): (2.5, 1, False),
        (75, 45, -315, -285): (1.5, 1.5, False),
        (345, 315, -45, -15): (2.5, -1, False),
        (315, 285, -75, -45): (1.5, -1.5, False),
        (165, 135, -225, -195): (2.5, 1, True),
        (135, 105, -255, -225): (1.5, 1.5, True),
        (225, 195, -165, -135): (2.5, -1, True),
        (255, 225, -135, -105): (1.5, -1.5, True)
    }

    def __init__(self, map_folder, player):
        self.map_folder = map_folder
        self.map_data = self.load_map_data()
        self.bg_layers = self.load_bg_layers()
        start_image = pygame.image.load(os.path.join(self.map_folder, self.map_data['start_bg']['res'])).convert_alpha()
        self.start_bg = {'image': start_image, 'x': self.map_data['start_bg']['x'], 'y': self.map_data['start_bg']['y']}

        self.bg_width = self.bg_layers[0]['image'].get_width()
        self.tiles = math.ceil(Const.SCREEN_WIDTH / self.bg_width) + 1
        self.scroll_x = -self.bg_width
        self.scroll_y = 0
        self.left_bound = Const.SCREEN_WIDTH - (self.bg_width * self.tiles)
        self.top_bound = abs(self.find_min_y())

        self.current_index = 0
        self.scroll_speed_x = 3
        self.scroll_speed_y = 0
        self.is_reverse_scroll = False
        self.is_two_types_of_enemies = self.map_data['is_two_types_of_enemies']
        self.player = player

    def load_map_data(self):
        with open(os.path.join(self.map_folder, 'map.json'), 'r') as f:
            return json.load(f)

    def load_bg_layers(self):
        bg_layers = []
        for layer_data in self.map_data['bg']:
            image_path = os.path.join(self.map_folder, layer_data['res'])
            if image_path.lower().endswith('.png'):
                image = pygame.image.load(image_path).convert_alpha()
            else:
                image = pygame.image.load(image_path).convert()
            bg_layers.append({'image': image, 'x': layer_data['x'], 'y': layer_data['y']})
        return bg_layers

    def find_min_y(self):
        min_y = float('inf')
        for layer_data in self.bg_layers:
            y = layer_data['y']
            if y < min_y:
                min_y = y
        return min_y

    def update(self, time_delta):
        self.update_scroll_behavior()

        for layer in self.bg_layers:
            for i in range(0, self.tiles):
                Const.SCREEN.blit(layer['image'], (self.scroll_x + (i * self.bg_width), self.scroll_y + layer['y']))

        if self.start_bg_visible():
            if self.current_index == 0:
                x_position = self.scroll_x + self.bg_width + self.start_bg['x']
            elif self.current_index == -1:
                x_position = self.scroll_x + (self.bg_width * 2) + self.start_bg['x']
            else:
                x_position = self.scroll_x + self.start_bg['x']

            Const.SCREEN.blit(self.start_bg['image'], (x_position, self.scroll_y + self.start_bg['y']))

        if self.is_reverse_scroll:
            self.scroll_x += self.scroll_speed_x
        else:
            self.scroll_x -= self.scroll_speed_x

        if self.scroll_x <= self.left_bound:
            self.scroll_x = -self.bg_width + (Const.SCREEN_WIDTH - self.bg_width)
            self.current_index += 1
            self.player.index = self.current_index
        elif self.scroll_x >= 0:
            self.scroll_x = -self.bg_width
            self.current_index -= 1
            self.player.index = self.current_index

    def start_bg_visible(self):
        return self.current_index in [-1, 0, 1]

    def update_scroll_behavior(self):
        angle = self.player.body.get_rotate()
        for angle_range, (speed_x, speed_y, reverse_scroll) in self.scroll_speed_mapping.items():
            if angle_range[0] >= angle >= angle_range[1] or angle_range[2] <= angle <= angle_range[3]:
                self.scroll_speed_x = speed_x
                self.scroll_speed_y = speed_y
                self.scroll_y += self.scroll_speed_y
                self.is_reverse_scroll = reverse_scroll
                break

        if (self.scroll_y - 3 <= self.scroll_y <= self.top_bound and self.player.body.get_y() < (
                Const.SCREEN_HEIGHT / 2)
                and (345 >= angle >= 195 or -195 <= angle <= -15)):
            self.scroll_y = self.top_bound
            self.player.body.set_y(self.player.body.get_y() + 2.2)
            if self.player.body.get_y() >= (Const.SCREEN_HEIGHT / 2):
                self.player.body.set_y(Const.SCREEN_HEIGHT / 2)
        elif (self.scroll_y + 3 >= self.scroll_y >= 0 and self.player.body.get_y() > (Const.SCREEN_HEIGHT / 2)
              and (165 >= angle >= 15 or -345 <= angle <= -195)):
            self.scroll_y = 0
            self.player.body.set_y(self.player.body.get_y() - 2.5)
            if self.player.body.get_y() <= (Const.SCREEN_HEIGHT / 2):
                self.player.body.set_y(Const.SCREEN_HEIGHT / 2)
        elif self.scroll_y >= self.top_bound:
            self.scroll_y = self.top_bound
            self.player.body.set_y(self.player.body.get_y() - 2.5)
        elif self.scroll_y < 0:
            self.scroll_y = 0
            self.player.body.set_y(self.player.body.get_y() + 2.2)

        if self.is_reverse_scroll and self.player.body.get_x() != (
                Const.SCREEN_WIDTH - 220) and self.scroll_speed_x == 3:
            self.player.move_right()
            if self.player.body.get_x() >= (Const.SCREEN_WIDTH - 220):
                self.player.body.set_x(Const.SCREEN_WIDTH - 220)
        elif not self.is_reverse_scroll and self.player.body.get_x() != 220 and self.scroll_speed_x == 3:
            self.player.move_left()
            if self.player.body.get_x() <= 220:
                self.player.body.set_x(220)
