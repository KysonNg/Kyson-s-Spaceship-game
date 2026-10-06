import math
import pygame
import random
class Ship:
    def __init__(self, x, y):
        self.radius = 22
        self.position = pygame.math.Vector2(x, y)
        self.angle = 90
        self.rotation_speed = 3
        self.velocity = pygame.Vector2(0, 0)
        self.acceleration = pygame.Vector2(0, 0)
        self.color = (90, 190, 255)
        self.drag = 0.99
        self.thrust = 0.15
        self.max_speed = 4
        self.is_thrusting = False
#this is the rotation code
    def forward(self):
        radians = math.radians(self.angle)
        return pygame.Vector2(math.cos(radians), -math.sin(radians))

    def move(self, keys, width, height):
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            self.angle += self.rotation_speed
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            self.angle -= self.rotation_speed

        self.acceleration = pygame.Vector2(0, 0)
        self.is_thrusting = False
        if keys[pygame.K_UP] or keys[pygame.K_w]:
            self.acceleration = self.forward() * self.thrust
            self.is_thrusting = True

        if self.velocity.length() > self.max_speed:
            self.velocity.scale_to_length(self.max_speed)

        self.velocity += self.acceleration
        self.position += self.velocity
        self.velocity *= self.drag

        self.position.x %= width
        self.position.y %= height

    def draw(self, screen):
        forward = self.forward()
        left = forward.rotate(140)
        right = forward.rotate(-140)
        points = [
            self.position + forward * 22,
            self.position + left * 16,
            self.position + right * 16,
        ]
        if self.is_thrusting:
            self.thrust_effect(screen)
        pygame.draw.polygon(screen, self.color, points, 2)

    def thrust_effect(self, screen):
        back = self.position - self.forward() * 18
        pygame.draw.circle(screen, (255, 180, 50), (round(back.x), round(back.y)), 5)