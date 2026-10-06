import pygame
import random
import math
from circle import Circle
from ship import Ship
from missile import Missile
import asyncio

async def main():
    pygame.init()
    WIDTH = 600
    HEIGHT = 800

    # AI enemy settings and starting position
    DETECTION_RANGE = 300
    FOV_THRESHOLD = 0.7
    ENEMY_SPEED = 2.5
    PATROL_TURN_SPEED = 2.5
    CHASE_TURN_SPEED = 100.0
    ENEMY_RADIUS = 18
    enemy_position = pygame.Vector2(ENEMY_RADIUS, ENEMY_RADIUS)
    enemy_angle = 0  # Faces right

    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Asteroid")
    clock = pygame.time.Clock()

    start_time = pygame.time.get_ticks()
    font = pygame.font.Font(None, 28)
    circles = []
    missiles = []
    ship = Ship(WIDTH / 2, HEIGHT / 2)

    running = True
    last_shot_time = 0
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        now = pygame.time.get_ticks()
        keys = pygame.key.get_pressed()
        mouse_buttons = pygame.mouse.get_pressed()
        if (keys[pygame.K_SPACE] or mouse_buttons[0]) and now - last_shot_time >= 200:
            missiles.append(Missile(ship.position, ship.forward()))
            last_shot_time = now

        # Update the player
        ship.move(keys, WIDTH, HEIGHT)

        # AI enemy: detect the player, patrol, or turn toward and follow the player
        to_player = ship.position - enemy_position
        distance = to_player.length()
        if distance > 0:
            direction_to_player = to_player.normalize() 
        else: 
            pygame.Vector2()

        enemy_radians = math.radians(enemy_angle)
        enemy_forward = pygame.Vector2(
            math.cos(enemy_radians), -math.sin(enemy_radians)
        )
        detected = (distance < DETECTION_RANGE and enemy_forward.dot(direction_to_player) > FOV_THRESHOLD)

        if detected and distance > 0:
            target_angle = math.degrees(
                math.atan2(-direction_to_player.y, direction_to_player.x)
            )
            angle_difference = (target_angle - enemy_angle + 180) % 360 - 180
            enemy_angle += max(-CHASE_TURN_SPEED, min(CHASE_TURN_SPEED, angle_difference))
        else:
            enemy_angle += PATROL_TURN_SPEED

        enemy_radians = math.radians(enemy_angle)
        enemy_forward = pygame.Vector2(
            math.cos(enemy_radians), -math.sin(enemy_radians)
        )
        enemy_position += enemy_forward * ENEMY_SPEED
        enemy_position.x %= WIDTH
        enemy_position.y %= HEIGHT

        # End the game if the AI touches the ship, and also allows for wraping of edges
        enemy_to_ship = ship.position - enemy_position
        if enemy_to_ship.x > WIDTH / 2:
            enemy_to_ship.x -= WIDTH
        elif enemy_to_ship.x < -WIDTH / 2:
            enemy_to_ship.x += WIDTH
        if enemy_to_ship.y > HEIGHT / 2:
            enemy_to_ship.y -= HEIGHT
        elif enemy_to_ship.y < -HEIGHT / 2:
            enemy_to_ship.y += HEIGHT
        if enemy_to_ship.length() <= ship.radius + ENEMY_RADIUS:
            running = False

        for missile in missiles:
            missile.move()
            if missile.is_off_screen(WIDTH, HEIGHT):
                missiles.remove(missile)

        if not circles:
            for _ in range(6):
                r = random.randint(10, 15)
                while True:
                    x = random.randint(r, WIDTH - r)
                    y = random.randint(r, HEIGHT - r)
                    spawn_position = pygame.math.Vector2(x, y)
                    if spawn_position.distance_to(ship.position) > ship.radius + r:
                        break

                color = (
                    random.randint(0, 255),
                    random.randint(0, 255),
                    random.randint(0, 255),
                )
                circles.append(Circle(x, y, r, color))

        for circle in circles:
            circle.move(WIDTH, HEIGHT)
            ship_apart = ship.position - circle.circle_pos
            ship_distance = ship_apart.length()
            if ship_distance <= ship.radius + circle.r:
                running = False

        # Elastic circle collisions using some vector magic
        for i in range(len(circles)):
            for j in range(i + 1, len(circles)):
                c1, c2 = circles[i], circles[j]
                offset = c2.circle_pos - c1.circle_pos
                distance = offset.length()

                if 0 < distance <= c1.r + c2.r:
                    normal = offset / distance
                    relative_velocity = c2.vector_direc - c1.vector_direc

                    if relative_velocity.dot(normal) < 0:
                        impulse = (2 * relative_velocity.dot(normal)) / (c1.mass + c2.mass)
                        c1.vector_direc += impulse * c2.mass * normal
                        c2.vector_direc -= impulse * c1.mass * normal

        for missile in missiles:
            for circle in circles:
                apart = missile.position - circle.circle_pos
                distance = apart.length()

                if distance <= missile.radius + circle.r:
                    missiles.remove(missile)
                    circles.remove(circle)
                    break

        # RENDER
        screen.fill((20, 24, 40))
        
        elapsed_seconds = (pygame.time.get_ticks() - start_time) // 1000
        time_text = font.render(f"Time Survived: {elapsed_seconds}s", True, (255, 255, 255))
        screen.blit(time_text, (10, 10))
        for circle in circles:
            circle.draw(screen)

        for missile in missiles:
            missile.draw(screen)

        ship.draw(screen)

        # AI enemy: draw detection range, facing direction, and detection status
        pygame.draw.circle(screen, (120, 120, 120), enemy_position, DETECTION_RANGE, 1)
        if detected:
            enemy_color = (255, 60, 60)
        else: 
            enemy_color = (255, 255, 255)
        pygame.draw.circle(screen, enemy_color, enemy_position, ENEMY_RADIUS)
        pygame.draw.line(
            screen,
            (255, 60, 60),
            enemy_position,
            enemy_position + enemy_forward * 100,
            3,
        )
        if detected:
            status = "PLAYER DETECTED!"
        else: 
            status = "PATROL"
        status_text = font.render(status, True, enemy_color)
        screen.blit(status_text, (10, 40))

        pygame.display.flip()
        clock.tick(60)

        await asyncio.sleep(0)

    pygame.quit()

if __name__ == "__main__":
    asyncio.run(main())
    
