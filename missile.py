import math
import pygame
import random


class Missile:

    def __init__(self, position, direction):
        self.position = pygame.math.Vector2(position)
        self.velocity = direction.normalize() * 8
        self.radius = 4
        self.color = (255, 220, 80)

    def move(self):
        self.position += self.velocity

    def is_off_screen(self, width, height):
        return (
            self.position.x < -self.radius
            or self.position.x > width + self.radius
            or self.position.y < -self.radius
            or self.position.y > height + self.radius
        )

    def draw(self, screen):
        pygame.draw.circle(
            screen,
            self.color,
            (round(self.position.x), round(self.position.y)),
            self.radius,
        )

