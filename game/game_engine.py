

# import pygame
# from .paddle import Paddle
# from .ball import Ball

# WHITE = (255, 255, 255)

# class GameEngine:
#     def __init__(self, width, height):
#         self.width = width
#         self.height = height
#         self.paddle_width = 10
#         self.paddle_height = 100

#         self.player = Paddle(10, height // 2 - 50, self.paddle_width, self.paddle_height)
#         self.ai = Paddle(width - 20, height // 2 - 50, self.paddle_width, self.paddle_height)
#         self.ball = Ball(width // 2, height // 2, 10, 10, width, height)  # slightly bigger ball

#         self.player_score = 0
#         self.ai_score = 0
#         self.font = pygame.font.SysFont("Arial", 30)

#     def handle_input(self):
#         keys = pygame.key.get_pressed()
#         if keys[pygame.K_w]:
#             self.player.move(-self.player.speed, self.height)
#         if keys[pygame.K_s]:
#             self.player.move(self.player.speed, self.height)

#     def update(self):
#         self.ball.move()
#         self.ball.check_collision(self.player, self.ai)

#         # Score update
#         if self.ball.x <= 0:
#             self.ai_score += 1
#             self.ball.reset()
#         elif self.ball.x >= self.width:
#             self.player_score += 1
#             self.ball.reset()

#         # Update AI paddle
#         self.ai.auto_track(self.ball, self.height)

#     def render(self, screen):
#         # Draw paddles and ball
#         pygame.draw.rect(screen, WHITE, self.player.rect())
#         pygame.draw.rect(screen, WHITE, self.ai.rect())
#         pygame.draw.ellipse(screen, WHITE, self.ball.rect())
#         pygame.draw.aaline(screen, WHITE, (self.width//2, 0), (self.width//2, self.height))

#         # Draw scores
#         player_text = self.font.render(str(self.player_score), True, WHITE)
#         ai_text = self.font.render(str(self.ai_score), True, WHITE)
#         screen.blit(player_text, (self.width//4, 20))
#         screen.blit(ai_text, (self.width * 3//4, 20))

import pygame
from .paddle import Paddle
from .ball import Ball

# Colors
PLAYER_COLOR = (0, 255, 255)   # Cyan
AI_COLOR = (255, 0, 255)       # Magenta
BALL_COLOR = (255, 255, 255)   # White
BG_COLOR = (15, 15, 30)        # Dark Navy
LINE_COLOR = (60, 60, 80)      # Midline

class GameEngine:
    def __init__(self, screen, target_score=5, sounds=None):
        self.screen = screen
        self.rect = screen.get_rect()
        self.width = self.rect.width
        self.height = self.rect.height
        self.sounds = sounds or {}

        # Entities
        self.player = Paddle(40, self.height // 2 - 50)
        self.ai = Paddle(self.width - 50, self.height // 2 - 50)
        self.ball = Ball(self.width // 2, self.height // 2)

        # Game state
        self.player_score = 0
        self.ai_score = 0
        self.target_score = target_score
        self.state = "PLAYING"
        self.winner = None

        # Fonts
        self.font_large = pygame.font.SysFont("consolas", 64)
        self.font_small = pygame.font.SysFont("consolas", 28)

    def reset_point(self, direction):
        self.ball.reset(direction)

    def reset_match(self, best_of=None):
        """Resets the match with optional new best-of target."""
        if best_of:
            self.target_score = (best_of // 2) + 1
        self.player_score = 0
        self.ai_score = 0
        self.ball.reset()
        self.state = "PLAYING"
        self.winner = None

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_w:
                self.player.move_up()
            elif event.key == pygame.K_s:
                self.player.move_down()
            elif event.key == pygame.K_r and self.state == "GAMEOVER":
                self.reset_match()
            elif event.key == pygame.K_q:
                pygame.event.post(pygame.event.Event(pygame.QUIT))
            elif event.key in (pygame.K_3, pygame.K_5, pygame.K_7):
                self.reset_match(best_of=int(event.unicode))
        elif event.type == pygame.KEYUP:
            if event.key in (pygame.K_w, pygame.K_s):
                self.player.stop()

    def update_ai(self, dt):
        """Simple tracking AI with some delay for fairness."""
        target_y = self.ball.y
        if abs(target_y - self.ai.rect.centery) > 10:
            direction = 1 if target_y > self.ai.rect.centery else -1
            self.ai.rect.centery += int(direction * self.ai.speed * dt * 0.75)

    def update(self, dt):
        if self.state != "PLAYING":
            return

        self.player.update(dt, self.height)
        self.update_ai(dt)

        event = self.ball.update(dt, self.player, self.ai, self.rect)

        # Sounds
        if event == "paddle" and "paddle" in self.sounds:
            self.sounds["paddle"].play()
        if event == "wall" and "wall" in self.sounds:
            self.sounds["wall"].play()

        # Scoring
        if event == "PLAYER":
            self.player_score += 1
            if "score" in self.sounds: self.sounds["score"].play()
            if self.player_score >= self.target_score:
                self.state = "GAMEOVER"
                self.winner = "PLAYER"
            else:
                self.reset_point(direction=-1)

        elif event == "AI":
            self.ai_score += 1
            if "score" in self.sounds: self.sounds["score"].play()
            if self.ai_score >= self.target_score:
                self.state = "GAMEOVER"
                self.winner = "AI"
            else:
                self.reset_point(direction=1)

    def render(self):
        self.screen.fill(BG_COLOR)

        # Draw midline
        pygame.draw.line(self.screen, LINE_COLOR,
                         (self.width // 2, 0), (self.width // 2, self.height), 2)

        # Draw entities
        self.player.draw(self.screen, PLAYER_COLOR)
        self.ai.draw(self.screen, AI_COLOR)
        self.ball.draw(self.screen, BALL_COLOR)

        # Score
        score_text = self.font_large.render(f"{self.player_score}   |   {self.ai_score}", True, (255, 255, 255))
        self.screen.blit(score_text, (self.width // 2 - score_text.get_width() // 2, 30))

        # Game over screen
        if self.state == "GAMEOVER":
            msg = self.font_large.render(f"{self.winner} WINS!", True, (255, 255, 100))
            self.screen.blit(msg, (self.width // 2 - msg.get_width() // 2, self.height // 2 - 50))
            sub = self.font_small.render("Press R to Restart | Q to Quit | 3/5/7 to change match length", True, (200, 200, 200))
            self.screen.blit(sub, (self.width // 2 - sub.get_width() // 2, self.height // 2 + 30))


