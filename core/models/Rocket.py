import random
import math

from core.GIFImage import GIFImage
from core.models.Sprite import Sprite
from src import Const


class Rocket:

    def __init__(self, x, y, angle, game, is_allied):
        self.x = x
        self.y = y
        self.angle = angle
        self.game = game
        self.is_allied = is_allied
        self.speed = 4
        self.body = GIFImage(Const.PATH + "assets/images/rocket.gif", 0.05, self.x, self.y)
        self.body.set_rotate(self.angle)
        self.target = None

    def update(self):
        if self.target is None:
            self.find_target()

        if self.game.map.is_reverse_scroll:
            self.body.set_x(self.body.get_x() + self.game.map.scroll_speed_x)
        else:
            self.body.set_x(self.body.get_x() - self.game.map.scroll_speed_x)
        self.body.set_y(self.body.get_y() + self.game.map.scroll_speed_y)

        fake_targets = [sprite for sprite in self.game.sprites if sprite.is_fake_target]
        if fake_targets and self.target:
            for fake_target in fake_targets:
                fake_target_x, fake_target_y = fake_target.body.get_x(), fake_target.body.get_y()
                distance_to_fake = math.sqrt((fake_target_x - self.x) ** 2 + (fake_target_y - self.y) ** 2)
                distance_to_real = math.sqrt(
                    (self.target.body.get_x() - self.x) ** 2 + (self.target.body.get_y() - self.y) ** 2)
                if distance_to_fake < distance_to_real:
                    self.target = fake_target

        if self.target is not None:
            try:
                target_x, target_y = self.target.body.get_x(), self.target.body.get_y()
            except AttributeError:
                self.game.sprites.append(
                    Sprite(GIFImage(filename=Const.PATH + 'assets/images/explosion.gif', x=self.body.get_x(),
                                    y=self.body.get_y(), loop=False), self.game)
                )
                Const.EXPLOSION_SOUND.play()
                self.game.rockets.remove(self)
                self.destroy()
                return

            direction_x = target_x - self.x
            direction_y = target_y - self.y

            angle_radians = math.atan2(direction_y, direction_x)
            angle_degrees = math.degrees(angle_radians)
            self.body.set_rotate(-angle_degrees)

            distance = math.sqrt(direction_x ** 2 + direction_y ** 2)
            if distance > 0:
                self.x += (direction_x / distance) * self.speed
                self.y += (direction_y / distance) * self.speed

        self.body.set_x(self.x)
        self.body.set_y(self.y)
        self.body.update()

        if self.target is not None:
            if self.body.get_rect().colliderect(self.target.body.get_rect()):
                try:
                    self.target.health -= 100
                except AttributeError:
                    pass
                finally:
                    self.game.sprites.append(
                        Sprite(GIFImage(filename=Const.PATH + 'assets/images/explosion.gif', x=self.body.get_x(),
                                        y=self.body.get_y(), loop=False), self.game)
                    )
                    Const.EXPLOSION_SOUND.play()
                    self.game.rockets.remove(self)
                    self.destroy()
                    return

        if (self.x < self.game.map.scroll_x or self.x > self.game.map.scroll_x +
                (self.game.map.bg_width * self.game.map.tiles) or self.y < -self.game.map.top_bound
                or self.y > (self.game.map.top_bound * self.game.map.tiles)):
            Const.EXPLOSION_SOUND.play()
            self.game.rockets.remove(self)
            self.destroy()

    def find_target(self):
        closest_enemy = None
        closest_enemy_distance = float('inf')

        if self.is_allied:
            for enemy in self.game.enemies:
                enemy_x, enemy_y = enemy.body.get_x(), enemy.body.get_y()
                distance = math.sqrt((enemy_x - self.x) ** 2 + (enemy_y - self.y) ** 2)
                if distance < closest_enemy_distance:
                    closest_enemy = enemy
                    closest_enemy_distance = distance
        else:
            closest_enemy = self.game.player

        if closest_enemy is not None:
            self.target = closest_enemy
        else:
            random_x = random.randint(Const.SCREEN_WIDTH * 3, Const.SCREEN_WIDTH * 4)
            random_y = random.randint(Const.SCREEN_HEIGHT * 3, Const.SCREEN_HEIGHT * 4)
            self.target = Sprite(GIFImage(None, x=random_x, y=random_y), self.game)

    def destroy(self):
        self.x = None
        self.y = None
        self.angle = None
        self.game = None
        self.is_allied = None
        self.speed = None
        self.body = None
        self.target = None
