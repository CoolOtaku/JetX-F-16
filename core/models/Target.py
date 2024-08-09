import pygame

from abc import ABC, abstractmethod

from src import Const


class Target(ABC):
    def __init__(self, index=0, health=100, ammunition=100, body=None, reload_time=1000, game=None):
        self.index = index
        self.health = health
        self.max_health = health
        self.ammunition = ammunition
        self.body = body
        self.reload_time = reload_time
        self.current_reload_time = 0
        self.game = game

    @abstractmethod
    def move_up(self):
        """Method for lifting up."""
        pass

    @abstractmethod
    def move_down(self):
        """Method for lowering."""
        pass

    @abstractmethod
    def move_left(self):
        """Method for moving to the left."""
        pass

    @abstractmethod
    def move_right(self):
        """Method for moving to the right."""
        pass

    @abstractmethod
    def to_twist(self):
        """Method to rotate the object."""
        pass

    @abstractmethod
    def to_shoot(self, is_rocket):
        """Method for shooting."""
        pass

    @abstractmethod
    def update(self, time_delta):
        """Method to update the status of the object."""
        pass

    @abstractmethod
    def destroy(self):
        """Method to clean up the object."""
        pass

    def visibility_range(self, x, y):
        if self.is_visible(self.game.map.current_index):
            x_position = x
            if self.game.map.current_index == self.index:
                x_position = self.game.map.scroll_x + self.game.map.bg_width + x
            elif self.game.map.current_index == (self.index - 1):
                x_position = self.game.map.scroll_x + (self.game.map.bg_width * 2) + x
            elif self.game.map.current_index == (self.index + 1):
                x_position = self.game.map.scroll_x + x
            self.body.set_x(x_position)
            y_position = self.game.map.scroll_y + y
            self.body.set_y(y_position)
            self.body.update()
            self.draw_health_bar()

    def draw_health_bar(self):
        width = 120
        height = 6
        health_bar_width = int(width * (self.health / self.max_health))

        x = self.body.get_x() - width // 2
        y = self.body.get_y() - 100

        pygame.draw.rect(Const.SCREEN, (255, 0, 0), (x, y, width, height))
        pygame.draw.rect(Const.SCREEN, (0, 255, 0), (x, y, health_bar_width, height))

    def is_visible(self, current_index):
        return current_index in [self.index - 1, self.index, self.index + 1]
