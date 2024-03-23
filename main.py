import pygame
from better_pygame import *
from scenes import StartMenu

SCREEN_SIZE = SCREEN_WIDTH, SCREEN_HEIGHT = (1280, 720)

def main():
    running = True
    clock = pygame.time.Clock()
    screen = pygame.display.set_mode(SCREEN_SIZE)
    dt = 0
    
    scene_manager = SceneManager(SCREEN_SIZE, 
                                 {
                                    "start":StartMenu(SCREEN_SIZE)
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
        
        dt = clock.tick(60)/1000