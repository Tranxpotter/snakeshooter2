import pygame
import pygame_gui

from better_pygame import *


class StartMenu(Scene):
    def __init__(self, screen_size: tuple[int, int]) -> None:
        self.ui_manager = pygame_gui.UIManager(screen_size)
        self.title = pygame_gui.elements.UILabel(relative_rect=pygame.Rect((0, 0), (200, 50)), 
                                                text="Snake Shooter", 
                                                manager=self.ui_manager, 
                                                anchors={"center", "center"})
        
        self.start_btn = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((0, 100), (150, 50)),
                                                      text="Start",
                                                      manager=self.ui_manager,
                                                      anchors={"center", "center"})
        

    def update(self, dt):
        raise NotImplementedError

    def render(self, screen):
        raise NotImplementedError

    def handle_events(self, events):
        raise NotImplementedError
