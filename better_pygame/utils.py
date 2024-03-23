import pygame

def tup_add(vec1:tuple[int|float, int|float], vec2:tuple[int|float, int|float]):
    return vec1[0] + vec2[0], vec1[1] + vec2[1]

def tup_subtract(vec1:tuple[int|float, int|float], vec2:tuple[int|float, int|float]):
    return vec1[0] - vec2[0], vec1[1] - vec2[1]

def tup_multiply(vec1:tuple[int|float, int|float], vec2:tuple[int|float, int|float]):
    return vec1[0] * vec2[0], vec1[1] * vec2[1]

def tup_divide(vec1:tuple[int|float, int|float], vec2:tuple[int|float, int|float]):
    return vec1[0] / vec2[0], vec1[1] / vec2[1]

def transparent_surface(size:tuple[int|float, int|float]):
    return pygame.Surface(size, pygame.SRCALPHA)