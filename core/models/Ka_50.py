import pygame
import random

from core.GIFImage import GIFImage
from core.models.Bullet import Bullet
from core.models.Sprite import Sprite
from core.models.Target import Target
from src import Const


class Ka_50(Target):
    def __init__(self, game):
        self.x = random.randint(0, game.map.bg_width)
        self.y = Const.SCREEN_HEIGHT / 2
        if game.map.is_reverse_scroll:
            spawn_index = game.map.current_index - 2
        else:
            spawn_index = game.map.current_index + 2
        super().__init__(spawn_index, 125, 130,
                         GIFImage(Const.PATH + "assets/images/ka_50.gif", 0.05, self.x * 3, self.y * 3),
                         30000, game
                         )
        self.last_shot_time = pygame.time.get_ticks()

    def move_up(self):
        self.y -= 1

    def move_down(self):
        self.y += 1

    def move_left(self):
        self.x -= 2
        if self.body.is_horizontal_flipped():
            self.to_twist()

    def move_right(self):
        self.x += 2
        if not self.body.is_horizontal_flipped():
            self.to_twist()

    def to_twist(self):
        self.body.flip_horizontal()

    def to_shoot(self, is_rocket):
        current_time = pygame.time.get_ticks()

        if self.ammunition > 0 and current_time - self.last_shot_time > 300:
            self.ammunition -= 1
            Const.SHOOT_SOUND_BULLET.play()

            rotate = 180
            if self.body.is_horizontal_flipped():
                rotate = 0

            bullet = Bullet(self.body.get_x(), self.body.get_y() + 50, rotate, self.game, False)
            self.game.bullets.append(bullet)
            self.last_shot_time = current_time
        elif self.ammunition == 0:
            self.current_reload_time = 0
            self.ammunition = -1

    def update(self, time_delta):
        self.visibility_range(self.x, self.y)

        if self.game.player is not None:
            if self.index < self.game.player.index:
                self.move_right()
            elif self.index > self.game.player.index:
                self.move_left()
            else:
                if self.body.get_y() < self.game.player.body.get_y() - (self.game.player.body.get_height() / 3):
                    self.move_down()
                if self.body.get_y() > self.game.player.body.get_y() + (self.game.player.body.get_height() / 3):
                    self.move_up()
                else:
                    self.to_shoot(False)

        if self.x < 0:
            self.index -= 1
            self.x = self.game.map.bg_width
        elif self.x > self.game.map.bg_width:
            self.index += 1
            self.x = 0

        if self.ammunition == -1:
            self.current_reload_time += time_delta
            if self.current_reload_time >= self.reload_time:
                self.current_reload_time = 0
                self.ammunition = 130

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
