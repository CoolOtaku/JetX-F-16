import pygame
import pygame_gui

from core.GIFImage import GIFImage
from src.Screen import Screen
from src import Const


class EndGameScreen(Screen):
    def __init__(self, is_win, current_statistics, map_folder):
        super().__init__()
        self.map_folder = map_folder
        self.background = GIFImage(
            Const.PATH + 'assets/images/bg_menu.gif', 0.05,
            Const.SCREEN_WIDTH / 2, Const.SCREEN_HEIGHT / 2
        )

        if is_win:
            current_statistics.wins += 1
            self.win_lose_image = pygame.image.load(Const.PATH + 'assets/images/win.png').convert_alpha()
        else:
            current_statistics.loses += 1
            self.win_lose_image = pygame.image.load(Const.PATH + 'assets/images/lose.png').convert_alpha()

        Const.STATISTICS = Const.STATISTICS + current_statistics
        Const.STATISTICS.save_statistics()

        self.statistics_panel = pygame_gui.elements.UIPanel(
            relative_rect=pygame.Rect(
                ((Const.SCREEN_WIDTH / 2) - 250, Const.SCREEN_HEIGHT / 3),
                (500, 130)
            ),
            manager=self.gui_manager
        )
        self.statistics_label = pygame_gui.elements.UILabel(
            relative_rect=pygame.Rect(
                (0, 5),
                (500, 25)
            ),
            text='strings.statistics', manager=self.gui_manager, container=self.statistics_panel
        )
        self.killing_label = pygame_gui.elements.UILabel(
            relative_rect=pygame.Rect(
                (0, 35),
                (166, 25)
            ),
            text='strings.killing', manager=self.gui_manager, container=self.statistics_panel
        )
        self.wins_label = pygame_gui.elements.UILabel(
            relative_rect=pygame.Rect(
                (166, 35),
                (166, 25)
            ),
            text='strings.wins', manager=self.gui_manager, container=self.statistics_panel
        )
        self.loses_label = pygame_gui.elements.UILabel(
            relative_rect=pygame.Rect(
                ((166 * 2), 35),
                (166, 25)
            ),
            text='strings.loses', manager=self.gui_manager, container=self.statistics_panel
        )
        self.killing_value_label = pygame_gui.elements.UILabel(
            object_id=pygame_gui.core.ObjectID(class_id='@statistics_texts'),
            relative_rect=pygame.Rect(
                (0, 65),
                (166, 25)
            ),
            text=str(Const.STATISTICS.killing), manager=self.gui_manager, container=self.statistics_panel
        )
        self.wins_value_label = pygame_gui.elements.UILabel(
            object_id=pygame_gui.core.ObjectID(class_id='@statistics_texts'),
            relative_rect=pygame.Rect(
                (166, 65),
                (166, 25)
            ),
            text=str(Const.STATISTICS.wins), manager=self.gui_manager, container=self.statistics_panel
        )
        self.loses_value_label = pygame_gui.elements.UILabel(
            object_id=pygame_gui.core.ObjectID(class_id='@statistics_texts'),
            relative_rect=pygame.Rect(
                ((166 * 2), 65),
                (166, 25)
            ),
            text=str(Const.STATISTICS.loses), manager=self.gui_manager, container=self.statistics_panel
        )

        self.play_again_button = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect(
                ((Const.SCREEN_WIDTH / 2) - 325, Const.SCREEN_HEIGHT - (105 * 3)),
                (650, 90)
            ),
            text='strings.play_again', manager=self.gui_manager
        )
        self.return_to_menu_button = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect(
                ((Const.SCREEN_WIDTH / 2) - 325, Const.SCREEN_HEIGHT - (105 * 2)),
                (650, 90)
            ),
            text='strings.return_to_menu', manager=self.gui_manager
        )

    def update(self, time_delta):
        self.background.update()
        time_update = time_delta / 1000.0
        self.gui_manager.update(time_update)
        self.gui_manager.draw_ui(Const.SCREEN)
        Const.SCREEN.blit(self.win_lose_image, ((Const.SCREEN_WIDTH / 2) - 123, 15))

    def events(self, event):
        if event.type == pygame_gui.UI_BUTTON_PRESSED:
            if event.ui_element == self.play_again_button:
                from src.GameScreen import GameScreen
                Const.SCREEN_MANAGER.start_screen(GameScreen(self.map_folder))
            elif event.ui_element == self.return_to_menu_button:
                from src.MenuScreen import MenuScreen
                Const.SCREEN_MANAGER.start_screen(MenuScreen())

        self.gui_manager.process_events(event)

    def destroy(self):
        self.gui_manager.clear_and_reset()
        self.map_folder = None
        self.background = None
        self.win_lose_image = None
        self.statistics_panel = None
        self.statistics_label = None
        self.killing_label = None
        self.wins_label = None
        self.loses_label = None
        self.killing_value_label = None
        self.wins_value_label = None
        self.loses_value_label = None
        self.play_again_button = None
        self.return_to_menu_button = None
