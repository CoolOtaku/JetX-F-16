import pygame
import cv2

from src import Const


class GIFImage:
    image_pool = {}

    def __init__(self, filename, frame_duration=0.1, x=0, y=0, loop=True):
        self.filename = filename
        self.x = x
        self.y = y
        self.angle = 0
        self.is_flip_x = False
        self.is_flip_y = False
        self.current_frame = 0
        self.frame_duration = frame_duration
        self.last_frame_change = pygame.time.get_ticks()
        self.images = self.load_images(filename)
        self.rotated_rect = pygame.Rect(0, 0, 0, 0)
        self.loop = loop
        self.is_alive = True

    @staticmethod
    def load_images(filename):
        if filename in GIFImage.image_pool:
            return list(GIFImage.image_pool[filename])
        else:
            if not filename:
                return []
            images = []
            gif = cv2.VideoCapture(filename)
            while True:
                ret, cv2_image = gif.read()
                if not ret:
                    break
                size = cv2_image.shape[1::-1]
                color_format = 'RGBA' if cv2_image.shape[2] == 4 else 'RGB'
                cv2_image[:, :, [0, 2]] = cv2_image[:, :, [2, 0]]
                surface = pygame.image.frombuffer(cv2_image.flatten(), size, color_format)
                pygame_image = surface.convert_alpha() if color_format == 'RGBA' else surface.convert()
                pygame_image.set_colorkey((255, 255, 255, 255))
                images.append(pygame_image.copy())
            GIFImage.image_pool[filename] = tuple(images)
            return list(images)

    def update(self):
        if self.is_alive:
            current_time = pygame.time.get_ticks()
            if current_time - self.last_frame_change > self.frame_duration * 1000:
                self.current_frame = (self.current_frame + 1) % len(self.images)
                self.last_frame_change = current_time

                if not self.loop and self.current_frame == len(self.images) - 1:
                    self.is_alive = False
                    return

            image_to_blit = self.images[self.current_frame]
            rotated_image = pygame.transform.rotate(image_to_blit, self.angle)
            self.rotated_rect = rotated_image.get_rect(center=image_to_blit.get_rect(center=(self.x, self.y)).center)

            Const.SCREEN.blit(rotated_image, self.rotated_rect.topleft)

    def set_x(self, x):
        self.x = x

    def get_x(self):
        return self.x

    def set_y(self, y):
        self.y = y

    def get_y(self):
        return self.y

    def set_rotate(self, angle):
        self.angle = angle
        if self.angle >= 360:
            self.angle = 0
        elif self.angle <= -360:
            self.angle = 0

    def get_rotate(self):
        return self.angle

    def get_width(self):
        return self.images[0].get_width()

    def get_height(self):
        return self.images[0].get_height()

    def flip_horizontal(self):
        self.is_flip_x = not self.is_flip_x
        for i in range(len(self.images)):
            self.images[i] = pygame.transform.flip(self.images[i], True, False)

    def is_horizontal_flipped(self):
        return self.is_flip_x

    def flip_vertical(self):
        self.is_flip_y = not self.is_flip_y
        for i in range(len(self.images)):
            self.images[i] = pygame.transform.flip(self.images[i], False, True)

    def is_vertical_flipped(self):
        return self.is_flip_y

    def get_rect(self):
        return self.rotated_rect
