
# import pygame
# import random

# class Ball:
#     def __init__(self, x, y, width, height, screen_width, screen_height):
#         self.original_x = x
#         self.original_y = y
#         self.x = x
#         self.y = y
#         self.width = width
#         self.height = height
#         self.screen_width = screen_width
#         self.screen_height = screen_height
#         self.reset()

#     def move(self):
#         self.x += self.velocity_x
#         self.y += self.velocity_y

#         # Bounce off top and bottom walls
#         if self.y <= 0:
#             self.y = 0
#             self.velocity_y *= -1
#         elif self.y + self.height >= self.screen_height:
#             self.y = self.screen_height - self.height
#             self.velocity_y *= -1

#     def check_collision(self, player, ai):
#         if self.rect().colliderect(player.rect()):
#             self.x = player.x + player.width
#             self.velocity_x *= -1
#             # Slight random vertical velocity change
#             self.velocity_y += random.uniform(-1, 1)
#         elif self.rect().colliderect(ai.rect()):
#             self.x = ai.x - self.width
#             self.velocity_x *= -1
#             self.velocity_y += random.uniform(-1, 1)

#     def reset(self):
#         self.x = self.original_x
#         self.y = self.original_y
#         self.velocity_x = random.choice([-5, 5])
#         self.velocity_y = random.choice([-3, 3])

#     def rect(self):
#         return pygame.Rect(self.x, self.y, self.width, self.height)
import pygame
import math, random

class Ball:
    def __init__(self, x, y, radius=10, base_speed=7, screen_width=900, screen_height=600):
        self.x = float(x)
        self.y = float(y)
        self.radius = radius
        self.base_speed = base_speed
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.reset(random.choice([-1, 1]))

    def reset(self, direction=1):
        self.x = self.screen_width / 2
        self.y = self.screen_height / 2
        angle = random.uniform(-0.4, 0.4)
        self.vx = direction * self.base_speed * math.cos(angle)
        self.vy = self.base_speed * math.sin(angle)

    def rect(self):
        return pygame.Rect(int(self.x - self.radius), int(self.y - self.radius),
                           self.radius * 2, self.radius * 2)

    def update(self, player, ai):
        """
        Step-based update to avoid tunneling at high speed.
        """
        steps = int(max(1, math.ceil(max(abs(self.vx), abs(self.vy)))))
        dx_step = self.vx / steps
        dy_step = self.vy / steps

        for _ in range(steps):
            self.x += dx_step
            self.y += dy_step

            # Wall collision
            if self.y - self.radius <= 0:
                self.y = self.radius
                self.vy *= -1
                return "wall"
            if self.y + self.radius >= self.screen_height:
                self.y = self.screen_height - self.radius
                self.vy *= -1
                return "wall"

            # Paddle collisions
            brect = self.rect()
            if brect.colliderect(player.rect()):
                self.x = player.x + player.width + self.radius
                self.vx = abs(self.vx) * 1.03
                offset = (self.y - (player.y + player.height / 2)) / (player.height / 2)
                self.vy += offset * 2
                return "paddle"

            if brect.colliderect(ai.rect()):
                self.x = ai.x - self.radius
                self.vx = -abs(self.vx) * 1.03
                offset = (self.y - (ai.y + ai.height / 2)) / (ai.height / 2)
                self.vy += offset * 2
                return "paddle"

        return None

    def is_out_left(self):
        return self.x + self.radius < 0

    def is_out_right(self):
        return self.x - self.radius > self.screen_width

    def draw(self, surface, color):
        pygame.draw.circle(surface, color, (int(self.x), int(self.y)), self.radius)

