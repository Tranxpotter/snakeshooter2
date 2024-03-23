from typing import Literal

import pygame

from ._constants import ON_TRANSITION_END
from .utils import *

class Transition:
    '''Base of all scene transitions
    
    Usage
    ---------
    Initialize the transition object, pass it into a scene's set_start_transition() or set_end_transition() method\n
    To make transition work, Scene.draw() should not be used, instead call Transition.draw(). Transition works by modifying the Surface the Scene drew on.\n
    If Scene is animated, Scene.update() should be called every loop such that the animation will still run during transition.\n
    Do be aware that the Scene's objects coordinates are not moved along with the transition, Scene.handle_event() should not be called while transition is running.\n
    
    Events
    ----------
    on transition end - type: ON_TRANSITION_END, element: Transition, object_id:str|None
    '''
    def __init__(self, sections:list[dict] = [], object_id:str|None = None) -> None:
        '''
        Parameters
        ------------
        sections: list[dict]
            A list of different sections at different durations of the transition
        
        sections
        ---------
        A section consist of many things, listed below (`key`: `value_type` - description)\n
        must-have -- `duration`: `int|float` - How long this section lasts\n
        `start_position`: `tuple[int|float, int|float]` - position of the scene at the start of the section\n
        `end_position`: `tuple[int|float, int|float]` - position of the scene at the end of the section\n
        `start_size`: `tuple[int|float, int|float]` - size of the scene at the start of the section\n
        `end_size`: `tuple[int|float, int|float]` - size of the scene at the end of the section\n
        `start_angle`: `tuple[int|float, int|float]` - angle of rotation of the scene at the start of the section\n
        `end_angle`: `tuple[int|float, int|float]` - angle of rotation of the scene at the end of the section, 
            bigger than start for clockwise, smaller than start for anti-clockwise\n
        `start_transparency`: `tuple[int|float, int|float]` - transparency of the scene at the start of the section, 0-255\n
        `end_transparency`: `tuple[int|float, int|float]` - transparency of the scene at the end of the section, 0-255\n
        If any of the start values are omitted, it will default to the previous section end value.\n
        Angles can be bigger than 360, for example, start_angle=0 end_engle=720 gives you 2 clockwise rotations.
        '''
        self.sections = sections
        self.curr_section_index = 0
        self.scene = None
        self.timer = 0
        self._running = False
        
        self._curr_position = (0, 0)
        self._curr_position_shift_rate = None
        self._curr_size_change_rate = None
        self._curr_angle = 0
        self._curr_angle_change_rate = None
        self._curr_transparency = 255
        self._curr_transparency_change_rate = None
        
        self.object_id = object_id


    def start(self, scene, scene_size:tuple[int, int]):
        '''Start the transition for a specific scene
        
        Parameters
        ------------
        scene: `Scene`
            The scene to be transitioned
        scene_size: `tuple`[`int`, `int`]
            The intended screen size for the scene'''
        self.scene = scene
        self.scene_size = scene_size
        self._curr_size = scene_size
        self.timer:int|float = self.sections[self.curr_section_index]["duration"]
        self.on_change_section()
        self._running = True
    
    def terminate(self):
        '''Terminate the running transition and reset all attributes. Triggers ON_TRANSITION_END event'''
        if not self._running:
            return
        self.curr_section_index = 0
        self.scene = None
        self.timer = 0
        self._running = False
        
        self._curr_position = (0, 0)
        self._curr_position_shift_rate = None
        self._curr_size_change_rate = None
        self._curr_angle = 0
        self._curr_angle_change_rate = None
        self._curr_transparency = 255
        self._curr_transparency_change_rate = None
        event = pygame.Event(ON_TRANSITION_END, {"element":self, "object_id":self.object_id})
        pygame.event.post(event)
    
    @staticmethod
    def get_change_rate_vec(start_vec:tuple[int|float, int|float], end_vec:tuple[int|float, int|float], duration:int|float):
        return tup_divide(tup_subtract(end_vec, start_vec), (duration, duration))

    @staticmethod
    def get_change_rate(start_val:int|float, end_val:int|float, duration:int|float):
        return (end_val - start_val) / duration
    
    def on_change_section(self):
        curr_section = self.sections[self.curr_section_index]
        
        duration = curr_section.get("duration")
        if duration is None:
            raise ValueError(f"Duration missing from Transition section, index-{self.curr_section_index}")
        
        #Defaulting current values
        self._curr_position_shift_rate = None
        self._curr_size_change_rate = None
        self._curr_angle_change_rate = None
        self._curr_transparency_change_rate = None
        
        
        
        #Position shifting init
        start_position = curr_section.get("start_position")
        if not start_position:
            start_position = self._curr_position
        else:
            self._curr_position = start_position
        end_position = curr_section.get("end_position")
        if end_position:
            self._curr_position_shift_rate = self.get_change_rate_vec(start_position, end_position, duration)
        
        #Size changing init
        start_size = curr_section.get("start_size")
        if not start_size:
            start_size = self._curr_size
        else:
            self._curr_size = start_size
        end_size = curr_section.get("end_size")
        if end_size:
            self._curr_size_change_rate = self.get_change_rate_vec(start_size, end_size, duration)
        
        #angle changing init
        start_angle = curr_section.get("start_angle")
        if not start_angle:
            start_angle = self._curr_angle
        else:
            self._curr_angle = start_angle
        end_angle = curr_section.get("end_angle")
        if end_angle:
            self._curr_angle_change_rate = self.get_change_rate(start_angle, end_angle, duration)
        
        #transparency changing init
        start_transparency = curr_section.get("start_transparency")
        if not start_transparency:
            start_transparency = self._curr_transparency
        else:
            self._curr_transparency = start_transparency
        end_transparency = curr_section.get("end_transparency")
        if end_transparency:
            self._curr_transparency_change_rate = self.get_change_rate(start_transparency, end_transparency, duration)
    
    def _update_curr_values(self, time:float):
        if self._curr_position_shift_rate:
            self._curr_position = tup_add(self._curr_position, tup_multiply(self._curr_position_shift_rate, (time, time)))
        if self._curr_size_change_rate:
            self._curr_size = tup_add(self._curr_size, tup_multiply(self._curr_size_change_rate, (time, time)))
        if self._curr_angle_change_rate:
            self._curr_angle += self._curr_angle_change_rate * time
            if self._curr_angle > 360:
                self._curr_angle -= 360
            elif self._curr_angle < 0:
                self._curr_angle += 360
        if self._curr_transparency_change_rate:
            self._curr_transparency += self._curr_transparency_change_rate * time
    
    def update(self, dt:float):
        self.timer -= dt
        if self.timer < 0:
            section_time = self.timer + dt
            self.timer += section_time
        else:
            section_time = dt
        self._update_curr_values(section_time)
        
        
        
        while self.timer < 0:
            self.curr_section_index += 1
            if self.curr_section_index >= len(self.sections):
                self._running = False
                self.scene = None
                self.curr_section_index -= 1
                event = pygame.Event(ON_TRANSITION_END, {"element":self, "object_id":self.object_id})
                pygame.event.post(event)
                break
            next_section = self.sections[self.curr_section_index]
            next_section_duration = next_section["duration"]
            
            if next_section_duration >= self.timer:
                next_section_time = -self.timer
                self.timer = 0
            else:
                next_section_time = next_section_duration
                self.timer += next_section_duration
            
            self._update_curr_values(next_section_time)
    
    def draw(self, screen:pygame.Surface):
        if not self.scene:
            return
        surf = transparent_surface(self.scene_size)
        self.scene.draw(surf)
        surf = pygame.transform.scale(surf, self._curr_size)
        surf = pygame.transform.rotate(surf, self._curr_angle % 360)
        surf.set_alpha(self._curr_transparency)
        screen.blit(surf, self._curr_position)



# def fast_build(screen_size:tuple[int, int], 
#                type:Literal["enter", "exit"], 
#                move_direction:Literal["up", "down", "left", "right", "left-up", "left-down", "right-up", "right-down"]|None,
#                transition_speed:Literal["linear", ""]
#             ):
#     ...




class LinearSlideDownExit(Transition):
    def __init__(self, screen_size:tuple[int, int], duration:float, object_id: str | None = None) -> None:
        sections = [
            {
                "start_position":(0, 0),
                "end_position":(0, screen_size[1]),
                "duration":duration
            }
        ]
        super().__init__(sections, object_id)


class LinearSlideDownEnter(Transition):
    def __init__(self, screen_size:tuple[int, int], duration:float, object_id: str | None = None) -> None:
        sections = [
            {
                "start_position":(0, -screen_size[1]),
                "end_position":(0, 0),
                "duration":duration
            }
        ]
        super().__init__(sections, object_id)

class LinearFadeIn(Transition):
    def __init__(self, duration, object_id: str | None = None) -> None:
        sections = [
            {
                "start_transparency": 0,
                "end_transparency": 255,
                "duration": duration
            }
        ]
        super().__init__(sections, object_id)

class LinearFadeOut(Transition):
    def __init__(self, duration, object_id: str | None = None) -> None:
        sections = [
            {
                "start_transparency": 255,
                "end_transparency": 0,
                "duration": duration
            }
        ]
        super().__init__(sections, object_id)













