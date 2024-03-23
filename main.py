import pygame
pygame.init()
import better_pygame
from better_pygame import *
from scenes import *

SCREEN_SIZE = SCREEN_WIDTH, SCREEN_HEIGHT = (1280, 720)

def main():
    running = True
    clock = pygame.time.Clock()
    screen = pygame.display.set_mode(SCREEN_SIZE)
    dt = 0
    
    start_menu = StartMenu(SCREEN_SIZE)
    # start_menu.set_enter_transition(better_pygame.transition.LinearFadeIn(2))
    # start_menu.set_exit_transition(better_pygame.transition.LinearFadeOut(2))
    
    settings = Settings(SCREEN_SIZE)
    settings.set_enter_transition(better_pygame.transition.LinearSlideDownEnter(SCREEN_SIZE, 2))
    
    
    scene_manager = SceneManager(SCREEN_SIZE, 
                                 {
                                    "start":start_menu,
                                    "settings":settings
                                 }, 
                                 "start"
                                )
    
    while running:
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                running = False
            scene_manager.handle_event(event)
        
        scene_manager.update(dt)
        
        scene_manager.draw(screen)
        pygame.display.flip()
        
        dt = clock.tick(60)/1000

if __name__ == '__main__':
    main()
    pygame.quit()