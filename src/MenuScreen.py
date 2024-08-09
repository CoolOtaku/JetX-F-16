import os

import pygame
import pygame_gui
import platform

from src.Screen import Screen
from src.GameScreen import GameScreen
from src import Const
from core.GIFImage import GIFImage
from src.Statistics import Statistics


class MenuScreen(Screen):
    is_change_control = False
    control_button = None

    def __init__(self):
        super().__init__()
        self.background = GIFImage(
            Const.PATH + 'assets/images/bg_menu.gif', 0.05,
            Const.SCREEN_WIDTH / 2, Const.SCREEN_HEIGHT / 2
        )

        Const.STATISTICS = Statistics()
        Const.STATISTICS.load_statistics()
        self.map_list = self.load_map_list()

        self.play_button = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect(
                (15, Const.SCREEN_HEIGHT - (105 * 3)),
                (430, 90)
            ),
            text='strings.play', manager=self.gui_manager
        )
        self.settings_button = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect(
                (15, Const.SCREEN_HEIGHT - (105 * 2)),
                (430, 90)
            ),
            text='strings.settings', manager=self.gui_manager
        )
        self.quit_button = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect(
                (15, Const.SCREEN_HEIGHT - 105),
                (430, 90)
            ),
            text='strings.quit', manager=self.gui_manager
        )

        self.maps_window = pygame_gui.elements.UIWindow(
            rect=pygame.Rect(
                ((Const.SCREEN_WIDTH / 2) - 400, (Const.SCREEN_HEIGHT / 2) - 300),
                (800, 600)
            ),
            window_display_title='strings.select_a_map', manager=self.gui_manager, visible=False
        )
        self.maps_selection_list = pygame_gui.elements.UISelectionList(
            relative_rect=pygame.Rect(
                (0, 0),
                (763, 460)
            ),
            item_list=self.map_list, manager=self.gui_manager, container=self.maps_window
        )
        cancel_button_rect = pygame.Rect((0, 0), (292, 55))
        cancel_button_rect.bottomright = (0 - (400 - (292 / 2)), -15)
        self.cancel_button = pygame_gui.elements.UIButton(
            object_id=pygame_gui.core.ObjectID(class_id='@settings_buttons', object_id='#cancel_button'),
            relative_rect=cancel_button_rect,
            text='strings.cancel', manager=self.gui_manager,
            container=self.maps_window,
            anchors={'right': 'right',
                     'bottom': 'bottom'}
        )

        self.settings_window = pygame_gui.elements.UIWindow(
            rect=pygame.Rect(
                ((Const.SCREEN_WIDTH / 2) - 400, (Const.SCREEN_HEIGHT / 2) - 300),
                (800, 600)
            ),
            window_display_title='strings.settings', manager=self.gui_manager, visible=False
        )
        self.locale_button = pygame_gui.elements.UIButton(
            object_id=pygame_gui.core.ObjectID(class_id='@game_buttons', object_id='#locale_button'),
            relative_rect=pygame.Rect(
                (15, 15),
                (95, 95)
            ),
            text="", manager=self.gui_manager, container=self.settings_window
        )
        self.sound_label = pygame_gui.elements.UILabel(
            relative_rect=pygame.Rect(
                (0, 0),
                (763, 25)
            ),
            text='strings.sounds', manager=self.gui_manager, container=self.settings_window
        )
        self.volume_all_label = pygame_gui.elements.UILabel(
            relative_rect=pygame.Rect(
                (0, 30),
                (763, 25)
            ),
            text='strings.volume_of_all_objects', manager=self.gui_manager, container=self.settings_window
        )
        self.volume_all_slider = pygame_gui.elements.UIHorizontalSlider(
            relative_rect=pygame.Rect(
                (250, 60),
                (300, 20)
            ),
            start_value=Const.SETTINGS.volume_all, value_range=(0.0, 1.0), manager=self.gui_manager,
            container=self.settings_window
        )
        self.volume_music_label = pygame_gui.elements.UILabel(
            relative_rect=pygame.Rect(
                (0, 90),
                (763, 25)
            ),
            text='strings.music_volume', manager=self.gui_manager, container=self.settings_window
        )
        self.volume_music_slider = pygame_gui.elements.UIHorizontalSlider(
            relative_rect=pygame.Rect(
                (250, 120),
                (300, 20)
            ),
            start_value=Const.SETTINGS.volume_music, value_range=(0.0, 1.0), manager=self.gui_manager,
            container=self.settings_window
        )
        if platform.system() != 'Android':
            self.display_mode_label = pygame_gui.elements.UILabel(
                relative_rect=pygame.Rect(
                    (0, 150),
                    (763, 25)
                ),
                text='strings.display_mode', manager=self.gui_manager, container=self.settings_window
            )
            display_mode = ['windowed mode', 'fullscreen mode']
            self.display_mode_menu = pygame_gui.elements.UIDropDownMenu(
                relative_rect=pygame.Rect(
                    (250, 180),
                    (300, 30)
                ),
                starting_option=display_mode[Const.SETTINGS.fullscreen], options_list=display_mode,
                manager=self.gui_manager, container=self.settings_window
            )
            self.control_label = pygame_gui.elements.UILabel(
                relative_rect=pygame.Rect(
                    (0, 210),
                    (763, 25)
                ),
                text='strings.control', manager=self.gui_manager, container=self.settings_window
            )
            self.move_up_label = pygame_gui.elements.UILabel(
                relative_rect=pygame.Rect(
                    (0, 240),
                    (381, 25)
                ),
                text='strings.move_up', manager=self.gui_manager, container=self.settings_window
            )
            self.move_up_button = pygame_gui.elements.UIButton(
                object_id=pygame_gui.core.ObjectID(class_id='@control_buttons'),
                relative_rect=pygame.Rect(
                    (127, 270),
                    (127, 30)
                ),
                text=Const.SETTINGS.get_key_name(Const.SETTINGS.key_bindings['move_up']), manager=self.gui_manager,
                container=self.settings_window
            )
            self.move_down_label = pygame_gui.elements.UILabel(
                relative_rect=pygame.Rect(
                    (0, 300),
                    (381, 25)
                ),
                text='strings.move_down', manager=self.gui_manager, container=self.settings_window
            )
            self.move_down_button = pygame_gui.elements.UIButton(
                object_id=pygame_gui.core.ObjectID(class_id='@control_buttons'),
                relative_rect=pygame.Rect(
                    (127, 330),
                    (127, 30)
                ),
                text=Const.SETTINGS.get_key_name(Const.SETTINGS.key_bindings['move_down']), manager=self.gui_manager,
                container=self.settings_window
            )
            self.to_twist_label = pygame_gui.elements.UILabel(
                relative_rect=pygame.Rect(
                    (0, 360),
                    (381, 25)
                ),
                text='strings.to_twist', manager=self.gui_manager, container=self.settings_window
            )
            self.to_twist_button = pygame_gui.elements.UIButton(
                object_id=pygame_gui.core.ObjectID(class_id='@control_buttons'),
                relative_rect=pygame.Rect(
                    (127, 390),
                    (127, 30)
                ),
                text=Const.SETTINGS.get_key_name(Const.SETTINGS.key_bindings['to_twist']), manager=self.gui_manager,
                container=self.settings_window
            )
            self.machine_gun_label = pygame_gui.elements.UILabel(
                relative_rect=pygame.Rect(
                    (381, 240),
                    (381, 25)
                ),
                text='strings.machine_gun', manager=self.gui_manager, container=self.settings_window
            )
            self.machine_gun_button = pygame_gui.elements.UIButton(
                object_id=pygame_gui.core.ObjectID(class_id='@control_buttons'),
                relative_rect=pygame.Rect(
                    (508, 270),
                    (127, 30)
                ),
                text=Const.SETTINGS.get_key_name(Const.SETTINGS.key_bindings['machine_gun']), manager=self.gui_manager,
                container=self.settings_window
            )
            self.rocket_label = pygame_gui.elements.UILabel(
                relative_rect=pygame.Rect(
                    (381, 300),
                    (381, 25)
                ),
                text='strings.rocket', manager=self.gui_manager, container=self.settings_window
            )
            self.rocket_button = pygame_gui.elements.UIButton(
                object_id=pygame_gui.core.ObjectID(class_id='@control_buttons'),
                relative_rect=pygame.Rect(
                    (508, 330),
                    (127, 30)
                ),
                text=Const.SETTINGS.get_key_name(Const.SETTINGS.key_bindings['rocket']), manager=self.gui_manager,
                container=self.settings_window
            )
            self.infrared_countermeasure_label = pygame_gui.elements.UILabel(
                relative_rect=pygame.Rect(
                    (381, 360),
                    (381, 25)
                ),
                text='strings.infrared_countermeasure', manager=self.gui_manager, container=self.settings_window
            )
            self.infrared_countermeasure_button = pygame_gui.elements.UIButton(
                object_id=pygame_gui.core.ObjectID(class_id='@control_buttons'),
                relative_rect=pygame.Rect(
                    (508, 390),
                    (127, 30)
                ),
                text=Const.SETTINGS.get_key_name(Const.SETTINGS.key_bindings['infrared_countermeasure']),
                manager=self.gui_manager,
                container=self.settings_window
            )

        save_button_rect = pygame.Rect((0, 0), (292, 55))
        save_button_rect.bottomright = (0 - (400 - (292 / 2)), -15)
        self.save_button = pygame_gui.elements.UIButton(
            object_id=pygame_gui.core.ObjectID(class_id='@settings_buttons', object_id='#ok_button'),
            relative_rect=save_button_rect,
            text='strings.save', manager=self.gui_manager,
            container=self.settings_window,
            anchors={'right': 'right',
                     'bottom': 'bottom'}
        )

        self.statistics_panel = pygame_gui.elements.UIPanel(
            relative_rect=pygame.Rect(
                (Const.SCREEN_WIDTH - 515, 15),
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

    def update(self, time_delta):
        self.background.update()
        time_update = time_delta / 1000.0
        self.gui_manager.update(time_update)
        self.gui_manager.draw_ui(Const.SCREEN)

    def events(self, event):
        if self.is_change_control:
            new_button = None
            if event.type == pygame.KEYDOWN:
                new_button = event.key
            elif event.type == pygame.MOUSEBUTTONDOWN:
                new_button = event.button

            if new_button:
                self.control_button.set_text(Const.SETTINGS.get_key_name(new_button))
                if self.control_button == self.move_up_button:
                    Const.SETTINGS.key_bindings['move_up'] = new_button
                elif self.control_button == self.move_down_button:
                    Const.SETTINGS.key_bindings['move_down'] = new_button
                elif self.control_button == self.to_twist_button:
                    Const.SETTINGS.key_bindings['to_twist'] = new_button
                elif self.control_button == self.machine_gun_button:
                    Const.SETTINGS.key_bindings['machine_gun'] = new_button
                elif self.control_button == self.rocket_button:
                    Const.SETTINGS.key_bindings['rocket'] = new_button
                elif self.control_button == self.infrared_countermeasure_button:
                    Const.SETTINGS.key_bindings['infrared_countermeasure'] = new_button

                Const.SETTINGS.save_settings()
                self.control_button = None
                self.is_change_control = False
        else:
            if event.type == pygame_gui.UI_BUTTON_PRESSED:
                if event.ui_element == self.play_button:
                    self.maps_window.show()
                elif event.ui_element == self.settings_button:
                    self.settings_window.show()
                elif event.ui_element == self.quit_button:
                    from main import exit_game
                    exit_game()
                elif event.ui_element == self.cancel_button:
                    self.maps_window.hide()
                elif event.ui_element == self.locale_button:
                    if Const.SETTINGS.locale == 'en':
                        Const.SETTINGS.locale = 'uk'
                    else:
                        Const.SETTINGS.locale = 'en'
                    self.gui_manager.set_locale(Const.SETTINGS.locale)
                elif event.ui_object_id == 'window.@control_buttons':
                    self.control_button = event.ui_element
                    self.control_button.set_text('')
                    self.is_change_control = True
                elif event.ui_element == self.save_button:
                    Const.SETTINGS.save_settings()
                    self.settings_window.hide()

            if event.type == pygame_gui.UI_SELECTION_LIST_NEW_SELECTION:
                if event.ui_element == self.maps_selection_list:
                    Const.SCREEN_MANAGER.start_screen(GameScreen(Const.PATH + 'data/maps/' + event.text))

            if event.type == pygame_gui.UI_HORIZONTAL_SLIDER_MOVED:
                if event.ui_element == self.volume_all_slider:
                    Const.SETTINGS.volume_all = event.value
                    Const.HOVER_SOUND.set_volume(Const.SETTINGS.volume_all)
                    Const.SHOOT_SOUND_BULLET.set_volume(Const.SETTINGS.volume_all)
                    Const.EXPLOSION_SOUND.set_volume(Const.SETTINGS.volume_all)
                    Const.INFRARED_SOUND.set_volume(Const.SETTINGS.volume_all)
                    Const.ROCKET_SOUND.set_volume(Const.SETTINGS.volume_all)
                elif event.ui_element == self.volume_music_slider:
                    Const.SETTINGS.volume_music = event.value
                    pygame.mixer.music.set_volume(Const.SETTINGS.volume_music)
                    if Const.SETTINGS.volume_music != 0.0:
                        pygame.mixer.music.play(-1)
                    else:
                        pygame.mixer.music.pause()

            if event.type == pygame_gui.UI_DROP_DOWN_MENU_CHANGED:
                if event.ui_element == self.display_mode_menu:
                    if event.text == 'windowed mode':
                        Const.SETTINGS.fullscreen = False
                    elif event.text == 'fullscreen mode':
                        Const.SETTINGS.fullscreen = True

                    if Const.SETTINGS.fullscreen:
                        Const.SCREEN = pygame.display.set_mode(
                            (Const.SCREEN_WIDTH, Const.SCREEN_HEIGHT), pygame.FULLSCREEN
                        )
                    else:
                        Const.SCREEN = pygame.display.set_mode(
                            (Const.SCREEN_WIDTH, Const.SCREEN_HEIGHT), 0
                        )

        self.gui_manager.process_events(event)

    @staticmethod
    def load_map_list():
        map_folder = Const.PATH + 'data/maps'
        map_list = []
        for entry in os.listdir(map_folder):
            if os.path.isdir(os.path.join(map_folder, entry)):
                map_list.append(entry)
        return map_list

    def destroy(self):
        self.gui_manager.clear_and_reset()
        self.background = None
        self.play_button = None
        self.settings_button = None
        self.quit_button = None
        self.maps_window = None
        self.maps_selection_list = None
        self.cancel_button = None
        self.settings_window = None
        self.locale_button = None
        self.sound_label = None
        self.volume_all_label = None
        self.volume_all_slider = None
        self.volume_music_label = None
        self.volume_music_slider = None
        self.display_mode_label = None
        self.display_mode_menu = None
        self.control_label = None
        self.move_up_label = None
        self.move_up_button = None
        self.move_down_label = None
        self.move_down_button = None
        self.to_twist_label = None
        self.to_twist_button = None
        self.machine_gun_label = None
        self.machine_gun_button = None
        self.rocket_label = None
        self.rocket_button = None
        self.infrared_countermeasure_label = None
        self.infrared_countermeasure_button = None
        self.save_button = None
        self.statistics_panel = None
        self.statistics_label = None
        self.killing_label = None
        self.wins_label = None
        self.loses_label = None
        self.killing_value_label = None
        self.wins_value_label = None
        self.loses_value_label = None
