import math
import pygame
import random
class Circle:
    def __init__(self, x, y, r, color):
        self.circle_pos = pygame.math.Vector2(x, y)
        self.r = r
        self.mass = r * r
        self.color = color
        self.vector_direc = pygame.math.Vector2(
            random.randint(-3, 3), random.randint(-3, 3)
        )

    def move(self, width, height):
        self.circle_pos += self.vector_direc

        if self.circle_pos.x - self.r < 0 or self.circle_pos.x + self.r > width:
            self.vector_direc.x *= -1
        if self.circle_pos.y - self.r < 0 or self.circle_pos.y + self.r > height:
            self.vector_direc.y *= -1

    def draw(self, screen):
        pygame.draw.circle(
            screen,
            self.color,
            (round(self.circle_pos.x), round(self.circle_pos.y)),
            self.r,
        )