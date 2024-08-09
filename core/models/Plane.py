import math

from core.GIFImage import GIFImage
from core.models.Bullet import Bullet
from core.models.Rocket import Rocket
from core.models.Sprite import Sprite
from core.models.Target import Target
from src import Const


class Plane(Target):
    def __init__(self, game):
        super().__init__(0, 100, 150,
                         GIFImage(Const.PATH + "assets/images/plane.gif", 0.05, 220, Const.SCREEN_HEIGHT / 1.1),
                         25000, game
                         )
        self.rocket = 4
        self.rocket_reload_time = 45000
        self.rocket_current_reload_time = 0

    def move_up(self):
        self.body.set_rotate(self.body.get_rotate() + 2)

    def move_down(self):
        self.body.set_rotate(self.body.get_rotate() - 2)

    def move_left(self):
        self.body.set_x(self.body.get_x() - 1.5)

    def move_right(self):
        self.body.set_x(self.body.get_x() + 1.5)

    def to_twist(self):
        self.body.flip_vertical()

    def to_shoot(self, is_rocket):
        if self.game.map.is_reverse_scroll is None and self.game.map.scroll_speed_y == 2.2:
            x = self.body.get_x() + 20
        elif self.game.map.is_reverse_scroll is None and self.game.map.scroll_speed_y == -2.5:
            x = self.body.get_x() - 20
        else:
            x = self.body.get_x()

        if self.body.is_vertical_flipped() and self.game.map.is_reverse_scroll:
            y = self.body.get_y() + 17
        elif self.body.is_vertical_flipped() or self.game.map.is_reverse_scroll:
            y = self.body.get_y() - 17
        else:
            y = self.body.get_y() + 17

        pos = self.get_pos_bullet(x, y)

        if is_rocket:
            if self.rocket > 0:
                self.rocket -= 1
                Const.ROCKET_SOUND.play()

                rocket = Rocket(pos[0], pos[1], self.body.get_rotate(), self.game, True)
                self.game.rockets.append(rocket)
            elif self.rocket == 0:
                self.current_reload_time = 0
                self.rocket = -1
        else:
            if self.ammunition > 0:
                self.ammunition -= 1
                Const.SHOOT_SOUND_BULLET.play()

                bullet = Bullet(pos[0], pos[1], self.body.get_rotate(), self.game, True)
                self.game.bullets.append(bullet)
            elif self.ammunition == 0:
                self.current_reload_time = 0
                self.ammunition = -1

    def shooting_traps(self):
        infrared_obj = Sprite(GIFImage(filename=Const.PATH + 'assets/images/infrared_countermeasure.gif',
                                       frame_duration=0.2, loop=False), self.game, 5)
        pos = self.get_pos_traps()
        infrared_obj.body.set_x(pos[0])
        infrared_obj.body.set_y(pos[1])
        if self.game.map.is_reverse_scroll:
            infrared_obj.body.flip_horizontal()

        self.game.sprites.append(infrared_obj)
        Const.INFRARED_SOUND.play()

    def get_pos_bullet(self, x, y):
        res = [0, 0]
        radius = self.body.get_width() / 4
        rotation_radians = math.radians(-self.body.get_rotate())
        res[0] = x + radius * math.cos(rotation_radians)
        res[1] = y + radius * math.sin(rotation_radians)
        return res

    def get_pos_traps(self):
        res = [0, 0]
        radius = self.body.get_width() / 2
        rotation_radians = math.radians(-self.body.get_rotate() + 180)
        res[0] = self.body.get_x() + radius * math.cos(rotation_radians)
        res[1] = self.body.get_y() + radius * math.sin(rotation_radians)
        return res

    def update(self, time_delta):
        self.body.update()

        if self.ammunition == -1:
            self.current_reload_time += time_delta
            if self.current_reload_time >= self.reload_time:
                self.current_reload_time = 0
                self.ammunition = 150

        if self.rocket == -1:
            self.rocket_current_reload_time += time_delta
            if self.rocket_current_reload_time >= self.rocket_reload_time:
                self.rocket_current_reload_time = 0
                self.rocket = 4

        if self.health <= 0:
            self.game.sprites.append(
                Sprite(GIFImage(filename=Const.PATH + 'assets/images/explosion.gif', x=self.body.get_x(),
                                y=self.body.get_y(), loop=False), self.game)
            )
            Const.EXPLOSION_SOUND.play()
            self.game.end_game(False)
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
        self.game.player = None
        self.game = None
        self.rocket = None
        self.rocket_reload_time = None
        self.rocket_current_reload_time = None
