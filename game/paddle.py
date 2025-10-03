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
#         if ball.y < self.y:
#             self.move(-self.speed, screen_height)
#         elif ball.y > self.y + self.height:
#             self.move(self.speed, screen_height)


import pygame

class Paddle:
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.speed = 7

    def move(self, dy, screen_height):
        self.y += dy
        self.y = max(0, min(self.y, screen_height - self.height))

    def rect(self):
        return pygame.Rect(self.x, self.y, self.width, self.height)

    def auto_track(self, ball, screen_height):
        # Move toward the center of the ball, but smoothly
        target_y = ball.y + ball.height / 2 - self.height / 2
        diff = target_y - self.y

        # Limit AI speed to make it more realistic
        if abs(diff) < self.speed:
            self.move(diff, screen_height)
        else:
            self.move(self.speed if diff > 0 else -self.speed, screen_height)
