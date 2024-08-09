import pygame
import pygame_gui
import platform

from src.Screen import Screen
from src import Const
from core.Game import Game


class GameScreen(Screen):
    is_pressed = False
    pressed_button = None

    def __init__(self, map_folder):
        super().__init__()
        self.game = Game(map_folder)

        if platform.system() == 'Android' or Const.ANDROID_GUI:
            self.up_button = pygame_gui.elements.UIButton(
                object_id=pygame_gui.core.ObjectID(class_id='@game_buttons', object_id='#up_button'),
                relative_rect=pygame.Rect(
                    (15, Const.SCREEN_HEIGHT - (95 * 2) - 15),
                    (95, 95)
                ),
                text='', manager=self.gui_manager
            )
            self.down_button = pygame_gui.elements.UIButton(
                object_id=pygame_gui.core.ObjectID(class_id='@game_buttons', object_id='#down_button'),
                relative_rect=pygame.Rect(
                    (15, Const.SCREEN_HEIGHT - 95 - 15),
                    (95, 95)
                ),
                text='', manager=self.gui_manager
            )
            self.to_twist_button = pygame_gui.elements.UIButton(
                object_id=pygame_gui.core.ObjectID(class_id='@game_buttons', object_id='#to_twist_button'),
                relative_rect=pygame.Rect(
                    (110, Const.SCREEN_HEIGHT - 55 - 15 - 20),
                    (55, 55)
                ),
                text='', manager=self.gui_manager
            )
            self.bullet_button = pygame_gui.elements.UIButton(
                object_id=pygame_gui.core.ObjectID(class_id='@game_buttons', object_id='#bullet_button'),
                relative_rect=pygame.Rect(
                    (Const.SCREEN_WIDTH - 95 - 15, Const.SCREEN_HEIGHT - 95 - 15),
                    (95, 95)
                ),
                text='', manager=self.gui_manager
            )
            self.rocket_button = pygame_gui.elements.UIButton(
                object_id=pygame_gui.core.ObjectID(class_id='@game_buttons', object_id='#rocket_button'),
                relative_rect=pygame.Rect(
                    (Const.SCREEN_WIDTH - (95 * 2) - 15, Const.SCREEN_HEIGHT - 95 - 15),
                    (95, 95)
                ),
                text='', manager=self.gui_manager
            )
            self.infrared_button = pygame_gui.elements.UIButton(
                object_id=pygame_gui.core.ObjectID(class_id='@game_buttons', object_id='#infrared_button'),
                relative_rect=pygame.Rect(
                    (Const.SCREEN_WIDTH - 55 - 15 - 20, Const.SCREEN_HEIGHT - 95 - 55 - 15),
                    (55, 55)
                ),
                text='', manager=self.gui_manager
            )

        self.top_panel = pygame_gui.elements.UIPanel(
            relative_rect=pygame.Rect(
                ((Const.SCREEN_WIDTH / 2) - 100, 0),
                (200, 75)
            ),
            manager=self.gui_manager
        )
        self.exit_button = pygame_gui.elements.UIButton(
            object_id=pygame_gui.core.ObjectID(class_id='@game_buttons', object_id='#exit_button'),
            relative_rect=pygame.Rect(
                (5, 5),
                (55, 55)
            ),
            text='', manager=self.gui_manager, container=self.top_panel
        )
        self.time_label = pygame_gui.elements.UILabel(
            relative_rect=pygame.Rect(
                (55, 0),
                (135, 75)
            ),
            text='00:00', manager=self.gui_manager, container=self.top_panel
        )

        self.bottom_panel = pygame_gui.elements.UIPanel(
            relative_rect=pygame.Rect(
                ((Const.SCREEN_WIDTH / 2) - 150, Const.SCREEN_HEIGHT - 75),
                (300, 75)
            ),
            manager=self.gui_manager
        )
        self.rocket_image = pygame_gui.elements.UIImage(
            relative_rect=pygame.Rect(
                (0, 0),
                (40, 40)
            ),
            image_surface=pygame.image.load(Const.PATH + 'assets/images/rocket_icon.png'), manager=self.gui_manager,
            container=self.bottom_panel
        )
        self.rocket_label = pygame_gui.elements.UILabel(
            relative_rect=pygame.Rect(
                (0, 35),
                (40, 35)
            ),
            text='0', manager=self.gui_manager, container=self.bottom_panel
        )
        self.health_label = pygame_gui.elements.UILabel(
            relative_rect=pygame.Rect(
                (35, 0),
                (220, 35)
            ),
            text='strings.health', manager=self.gui_manager, container=self.bottom_panel
        )
        self.health_bar = pygame_gui.elements.UIProgressBar(
            relative_rect=pygame.Rect(
                (75, 30),
                (150, 35)
            ),
            manager=self.gui_manager, container=self.bottom_panel
        )
        self.health_bar.set_current_progress(50)
        self.bullet_image = pygame_gui.elements.UIImage(
            relative_rect=pygame.Rect(
                (250, 0),
                (40, 40)
            ),
            image_surface=pygame.image.load(Const.PATH + 'assets/images/bullet_icon.png'), manager=self.gui_manager,
            container=self.bottom_panel
        )
        self.bullet_label = pygame_gui.elements.UILabel(
            relative_rect=pygame.Rect(
                (250, 35),
                (40, 35)
            ),
            text='0', manager=self.gui_manager, container=self.bottom_panel
        )

        self.message_window = pygame_gui.windows.UIMessageWindow(
            object_id=pygame_gui.core.ObjectID(object_id='#message_window'),
            rect=pygame.Rect(
                ((Const.SCREEN_WIDTH / 2) - 250, (Const.SCREEN_HEIGHT / 2) - 75),
                (500, 150)
            ),
            window_title='strings.message_window_title', html_message='strings.message_window_text',
            always_on_top=True, manager=self.gui_manager, visible=False
        )

    def update(self, time_delta):
        self.game.update(time_delta)
        time_update = time_delta / 1000.0
        self.gui_manager.update(time_update)
        self.gui_manager.draw_ui(Const.SCREEN)

        if self.is_pressed:
            if self.pressed_button == self.up_button:
                if self.game.player.body.is_vertical_flipped():
                    self.game.player.move_down()
                else:
                    self.game.player.move_up()
            elif self.pressed_button == self.down_button:
                if self.game.player.body.is_vertical_flipped():
                    self.game.player.move_up()
                else:
                    self.game.player.move_down()
        try:
            self.time_label.set_text(self.game.get_remaining_time())
            self.health_bar.set_current_progress(self.game.player.health)
            if self.game.player.ammunition == -1:
                self.bullet_label.set_text('0')
            else:
                self.bullet_label.set_text(str(self.game.player.ammunition))
            if self.game.player.rocket == -1:
                self.rocket_label.set_text('0')
            else:
                self.rocket_label.set_text(str(self.game.player.rocket))
        except Exception:
            return

    def events(self, event):
        if self.game.is_started:
            keys = pygame.key.get_pressed()
            if keys[Const.SETTINGS.key_bindings['move_up']]:
                if self.game.player.body.is_vertical_flipped():
                    self.game.player.move_down()
                else:
                    self.game.player.move_up()
            elif keys[Const.SETTINGS.key_bindings['move_down']]:
                if self.game.player.body.is_vertical_flipped():
                    self.game.player.move_up()
                else:
                    self.game.player.move_down()

            if event.type == pygame.KEYDOWN:
                if event.key == Const.SETTINGS.key_bindings['to_twist']:
                    self.game.player.to_twist()
                elif event.key == Const.SETTINGS.key_bindings['machine_gun']:
                    self.game.player.to_shoot(False)
                elif event.key == Const.SETTINGS.key_bindings['rocket']:
                    self.game.player.to_shoot(True)
                elif event.key == Const.SETTINGS.key_bindings['infrared_countermeasure']:
                    self.game.player.shooting_traps()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == Const.SETTINGS.key_bindings['to_twist']:
                    self.game.player.to_twist()
                elif event.button == Const.SETTINGS.key_bindings['machine_gun']:
                    self.game.player.to_shoot(False)
                elif event.button == Const.SETTINGS.key_bindings['rocket']:
                    self.game.player.to_shoot(True)
                elif event.button == Const.SETTINGS.key_bindings['infrared_countermeasure']:
                    self.game.player.shooting_traps()

            if platform.system() == 'Android' or Const.ANDROID_GUI:
                try:
                    if event.type == pygame_gui.UI_BUTTON_START_PRESS:
                        if event.ui_element == self.up_button or event.ui_element == self.down_button:
                            self.pressed_button = event.ui_element
                            self.is_pressed = True

                    if event.type == pygame_gui.UI_BUTTON_PRESSED:
                        if event.ui_element == self.up_button or event.ui_element == self.down_button:
                            self.pressed_button = None
                            self.is_pressed = False

                        elif event.ui_element == self.to_twist_button:
                            self.game.player.to_twist()
                        elif event.ui_element == self.bullet_button:
                            self.game.player.to_shoot(False)
                        elif event.ui_element == self.rocket_button:
                            self.game.player.to_shoot(True)
                        elif event.ui_element == self.infrared_button:
                            self.game.player.shooting_traps()
                except AttributeError:
                    print('Is not Android')

        if event.type == pygame_gui.UI_BUTTON_PRESSED and event.ui_element == self.exit_button:
            from src.MenuScreen import MenuScreen
            Const.SCREEN_MANAGER.start_screen(MenuScreen())

        self.gui_manager.process_events(event)

    def destroy(self):
        self.gui_manager.clear_and_reset()
        self.game = None
        if platform.system() == 'Android' or Const.ANDROID_GUI:
            self.up_button = None
            self.down_button = None
            self.to_twist_button = None
            self.bullet_button = None
            self.rocket_button = None
            self.infrared_button = None
        self.top_panel = None
        self.exit_button = None
        self.time_label = None
        self.bottom_panel = None
        self.rocket_image = None
        self.rocket_label = None
        self.health_label = None
        self.health_bar = None
        self.bullet_image = None
        self.bullet_label = None
