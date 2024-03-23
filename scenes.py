import pygame
import pygame_gui

from better_pygame import *

pygame.font.init()
normal_font = lambda size:pygame.font.Font("fonts/Helvetica-Font/Helvetica.ttf", size)
bold_font = lambda size:pygame.font.Font("fonts/Helvetica-Font/Helvetica-Bold.ttf", size)
oblique_font = lambda size:pygame.font.Font("fonts/Helvetica-Font/Helvetica-Oblique.ttf", size)
bold_oblique_font = lambda size:pygame.font.Font("fonts/Helvetica-Font/Helvetica-BoldOblique.ttf", size)

class StartMenu(Scene):
    def __init__(self, screen_size: tuple[int, int]) -> None:
        self.ui_manager = pygame_gui.UIManager(screen_size, "themes/start_menu.json")
                    
        self.title = pygame_gui.elements.UILabel(relative_rect=pygame.Rect((0, 0), (600, 100)), 
                                                text="Snake Shooter", 
                                                manager=self.ui_manager, 
                                                anchors={"center":"center"},
                                                object_id=pygame_gui.core.ObjectID("#title", "@title"))
        
        
        self.start_btn = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((-100, 200), (100, 100)),
                                                      text="",
                                                      manager=self.ui_manager,
                                                      anchors={"center":"center"},
                                                      object_id=pygame_gui.core.ObjectID("#start_button", "@image_button"))
        
        self.settings_btn = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((100, 200), (100, 100)),
                                                         text="",
                                                         manager=self.ui_manager,
                                                         anchors={"center":"center"},
                                                         object_id=pygame_gui.core.ObjectID("#settings_button", "@image_button"))
        
        self.background_img = pygame.image.load("assets/start_menu_background.png")
        self.background_img = pygame.transform.scale(self.background_img, screen_size)
        
    
    def handle_event(self, event:pygame.Event):
        if event.type == pygame_gui.UI_BUTTON_PRESSED:
            if event.ui_element == self.settings_btn:
                # Switch to settings scene
                self.scene_manager.change_scene("settings")
        self.ui_manager.process_events(event)
        

    def update(self, dt:float):
        self.ui_manager.update(dt)

    def draw(self, screen:pygame.Surface):
        screen.blit(self.background_img, (0,0))
        self.ui_manager.draw_ui(screen)


class Settings(Scene):
    def __init__(self, screen_size:tuple[int, int]) -> None:
        self.ui_manager = pygame_gui.UIManager(screen_size, "themes/settings.json")
        
        self.return_btn = pygame_gui.elements.UIButton(pygame.Rect((0, 0), (100, 100)),
                                                       "",
                                                       self.ui_manager,
                                                       object_id=pygame_gui.core.ObjectID("#return_button", "@image_button"))
        
        self.background_img = pygame.image.load("assets/settings_background.png")
        self.background_img = pygame.transform.scale(self.background_img, screen_size)
        
        
    
    def handle_event(self, event: pygame.Event):
        self.ui_manager.process_events(event)
    
    def update(self, dt: float):
        self.ui_manager.update(dt)
    
    def draw(self, screen: pygame.Surface):
        screen.blit(self.background_img, (0,0))
        self.ui_manager.draw_ui(screen)
    
    