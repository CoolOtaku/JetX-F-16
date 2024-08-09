import pygame

from core.GIFImage import GIFImage
from core.models.Rocket import Rocket
from core.models.Sprite import Sprite
from core.models.Target import Target
from src import Const


class Pantsir_S1(Target):
    def __init__(self, game):
        self.x = game.map.map_data['enemies_x']
        self.y = game.map.map_data['enemies_y']
        if game.map.is_reverse_scroll:
            spawn_index = game.map.current_index - 2
        else:
            spawn_index = game.map.current_index + 2
        super().__init__(spawn_index, 165, 4,
                         GIFImage(Const.PATH + "assets/images/pantsir_s1.gif", 5, self.x * 3, self.y * 3),
                         40000, game
                         )
        self.last_shot_time = pygame.time.get_ticks()

    def move_up(self):
        pass

    def move_down(self):
        pass

    def move_left(self):
        pass

    def move_right(self):
        pass

    def to_twist(self):
        pass

    def to_shoot(self, is_rocket):
        current_time = pygame.time.get_ticks()

        if self.ammunition > 0 and current_time - self.last_shot_time > 12000:
            self.ammunition -= 1
            Const.ROCKET_SOUND.play()

            rocket = Rocket(self.body.get_x(), self.body.get_y(), self.body.get_rotate(), self.game, False)
            self.game.rockets.append(rocket)
            self.last_shot_time = current_time
        elif self.ammunition == 0:
            self.current_reload_time = 0
            self.ammunition = -1

    def update(self, time_delta):
        self.visibility_range(self.x, self.y)

        if self.game.player is not None and self.is_visible(self.game.map.current_index):
            self.to_shoot(True)

        if self.ammunition == -1:
            self.current_reload_time += time_delta
            if self.current_reload_time >= self.reload_time:
                self.current_reload_time = 0
                self.ammunition = 4

        if self.health <= 0:
            self.game.sprites.append(
                Sprite(GIFImage(filename=Const.PATH + 'assets/images/explosion.gif', x=self.body.get_x(),
                                y=self.body.get_y(), loop=False), self.game)
            )
            Const.EXPLOSION_SOUND.play()
            self.game.enemies.remove(self)
            self.game.current_statistics.killing += 1
            self.destroy()
            return
        elif 0 < self.health < self.max_health:
            self.health += 0.003
            if self.health >= self.max_health:
                self.health = self.max_health

    def destroy(self):
        self.index = None
        self.health = None
        self.max_health = None
        self.ammunition = None
        self.body = None
        self.reload_time = None
        self.current_reload_time = None
        self.game = None
        self.x = None
        self.y = None
        self.last_shot_time = None
