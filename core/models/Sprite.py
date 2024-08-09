import random


class Sprite:
    def __init__(self, body, game, probability=0):
        self.body = body
        self.game = game
        self.is_fake_target = False
        if random.random() < (5 + probability) / 100:
            self.is_fake_target = True

    def update(self):
        if self.game.map.is_reverse_scroll:
            self.body.set_x(self.body.get_x() + self.game.map.scroll_speed_x)
        else:
            self.body.set_x(self.body.get_x() - self.game.map.scroll_speed_x)
        self.body.set_y(self.body.get_y() + self.game.map.scroll_speed_y)

        self.body.update()

        if not self.body.is_alive:
            self.game.sprites.remove(self)
            self.destroy()

    def destroy(self):
        self.body = None
        self.game = None
        self.is_fake_target = None
