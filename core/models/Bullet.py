import pygame
import math

from src import Const


class Bullet:
    bullet_image = None

    def __init__(self, x, y, angle, game, is_allied):
        self.x = x
        self.y = y
        self.angle = angle
        self.game = game
        self.is_allied = is_allied
        self.speed = 6
        if Bullet.bullet_image is None:
            Bullet.bullet_image = pygame.image.load(Const.PATH + 'assets/images/bullet.png').convert_alpha()
        self.body = pygame.transform.rotate(Bullet.bullet_image, angle)
        self.rect = self.body.get_rect(center=(self.x, self.y))

    def update(self):
        self.x += self.speed * math.cos(math.radians(self.angle))
        self.y -= self.speed * math.sin(math.radians(self.angle))

        if self.game.map.scroll_y != self.game.map.top_bound and self.game.map.scroll_y != 0:
            self.y += self.game.map.scroll_speed_y

        self.rect.center = (self.x, self.y)
        Const.SCREEN.blit(self.body, self.rect)

        if self.rect.colliderect(self.game.player.body.get_rect()) and not self.is_allied:
            self.game.player.health -= 10
            self.game.bullets.remove(self)
            self.destroy()
            return
        for unit in self.game.enemies:
            if self.rect.colliderect(unit.body.get_rect()) and self.is_allied:
                unit.health -= 10
                self.game.bullets.remove(self)
                self.destroy()
                return

        if (self.x < self.game.map.scroll_x or self.x > self.game.map.scroll_x +
                (self.game.map.bg_width * self.game.map.tiles) or self.y < -self.game.map.top_bound
                or self.y > (self.game.map.top_bound * self.game.map.tiles)):
            self.game.bullets.remove(self)
            self.destroy()

    def destroy(self):
        self.x = None
        self.y = None
        self.angle = None
        self.game = None
        self.is_allied = None
        self.speed = None
        self.body = None
        self.rect = None
