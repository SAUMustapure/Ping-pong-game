
# import pygame

# class Paddle:
#     def __init__(self, x, y, width, height):
#         self.x = x
#         self.y = y
#         self.width = width
#         self.height = height
#         self.speed = 7

#     def move(self, dy, screen_height):
#         self.y += dy
#         self.y = max(0, min(self.y, screen_height - self.height))

#     def rect(self):
#         return pygame.Rect(self.x, self.y, self.width, self.height)

#     def auto_track(self, ball, screen_height):
#         # Move toward the center of the ball, but smoothly
#         target_y = ball.y + ball.height / 2 - self.height / 2
#         diff = target_y - self.y

#         # Limit AI speed to make it more realistic
#         if abs(diff) < self.speed:
#             self.move(diff, screen_height)
#         else:
#             self.move(self.speed if diff > 0 else -self.speed, screen_height)

import pygame

class Paddle:
    def __init__(self, x, y, width=10, height=100, speed=500):
        self.rect = pygame.Rect(x, y, width, height)
        self.speed = speed
        self.velocity = 0

    # --- Player Controls ---
    def move_up(self):
        self.velocity = -self.speed

    def move_down(self):
        self.velocity = self.speed

    def stop(self):
        self.velocity = 0

    def update(self, dt, screen_height):
        """Update paddle position with velocity & clamp to screen."""
        self.rect.y += int(self.velocity * dt)
        if self.rect.top < 0:
            self.rect.top = 0
        if self.rect.bottom > screen_height:
            self.rect.bottom = screen_height

    # --- AI Controls ---
    def auto_track(self, ball, screen_height, tracking_factor=0.75):
        """
        Simple AI: Move towards the ball's y position with scaling factor.
        """
        target = ball.y
        if abs(target - self.rect.centery) > 10:
            direction = 1 if target > self.rect.centery else -1
            self.rect.centery += int(direction * self.speed * tracking_factor)

        # Clamp again
        if self.rect.top < 0:
            self.rect.top = 0
        if self.rect.bottom > screen_height:
            self.rect.bottom = screen_height

    # --- Drawing ---
    def draw(self, surface, color):
        pygame.draw.rect(surface, color, self.rect, border_radius=6)

