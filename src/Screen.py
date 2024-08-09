import pygame_gui

from abc import ABC, abstractmethod

from src import Const


class Screen(ABC):
    def __init__(self):
        self.gui_manager = pygame_gui.UIManager(
            (Const.SCREEN_WIDTH, Const.SCREEN_HEIGHT),
            starting_language=Const.SETTINGS.locale, translation_directory_paths=['data/translations'],
            theme_path=Const.PATH + 'assets/theme.json'
        )

    @abstractmethod
    def update(self, time_delta):
        """A method for updating the status of the screen and all its objects."""
        pass

    @abstractmethod
    def events(self, event):
        """Screen interaction listener."""
        pass

    @abstractmethod
    def destroy(self):
        """Destroy all objects on the screen and free memory."""
        pass
