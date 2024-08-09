import pygame
import pygame_gui

from src import Const
from src.MenuScreen import MenuScreen


class ScreenManager:
    global ACTIVE_SCREEN

    def __init__(self):
        self.ACTIVE_SCREEN = MenuScreen()
        self.cursor = pygame.image.load(Const.PATH + 'assets/images/cursor.png').convert_alpha()
        self.font = pygame.font.Font(None, 30)

    def start_screen(self, new_screen):
        self.ACTIVE_SCREEN.destroy()
        self.ACTIVE_SCREEN = new_screen

    def events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                from main import exit_game
                exit_game()

            if event.type == pygame.KEYDOWN and event.key == pygame.K_F11:
                Const.SETTINGS.fullscreen = not Const.SETTINGS.fullscreen
                if Const.SETTINGS.fullscreen:
                    Const.SCREEN = pygame.display.set_mode(
                        (Const.SCREEN_WIDTH, Const.SCREEN_HEIGHT), pygame.FULLSCREEN
                    )
                else:
                    Const.SCREEN = pygame.display.set_mode(
                        (Const.SCREEN_WIDTH, Const.SCREEN_HEIGHT), 0
                    )

            if event.type == pygame_gui.UI_BUTTON_ON_HOVERED:
                Const.HOVER_SOUND.play()

            self.ACTIVE_SCREEN.events(event)

    def update(self, time_delta):
        self.ACTIVE_SCREEN.update(time_delta)

        if Const.VIEW_FPS:
            self.draw_fps()
        Const.SCREEN.blit(self.cursor, (Const.MOUSE_POS[0] - 40, Const.MOUSE_POS[1] - 40))

    def draw_fps(self):
        fps_text = self.font.render(f"FPS: {int(Const.CLOCK.get_fps())}", True, (0, 255, 0))
        Const.SCREEN.blit(fps_text, (10, 10))
