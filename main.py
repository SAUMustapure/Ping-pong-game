import pygame
import sys
<<<<<<< HEAD
from game.game_engine import GameEngine

SCREEN_W, SCREEN_H = 900, 600

def main():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_W, SCREEN_H))
    pygame.display.set_caption("Ping Pong: Clean Edition")
    clock = pygame.time.Clock()

    engine = GameEngine(screen)

    running = True
    while running:
        dt = clock.tick(60) / 1000.0

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            engine.handle_event(event)

        engine.update(dt)
        engine.draw()
        pygame.display.flip()

    pygame.quit()
    sys.exit()
=======
import numpy as np
from game.game_engine import GameEngine

WIDTH, HEIGHT = 800, 600
FPS = 60

def make_sound(frequency=440, duration_ms=80, volume=0.2, sample_rate=44100):
    """
    Return a pygame.mixer.Sound generated with a sine wave using numpy.
    """
    t = np.linspace(0, duration_ms/1000, int(sample_rate * duration_ms/1000), False)
    wave = 0.5 * np.sin(2 * np.pi * frequency * t)
    envelope = np.linspace(1, 0.1, wave.size)
    wave = wave * envelope
    audio = np.int16(wave * 32767 * volume)
    sound = pygame.sndarray.make_sound(audio)
    return sound

def init_sounds():
    pygame.mixer.pre_init(44100, -16, 1, 512)
    pygame.mixer.init()
    sounds = {}
    try:
        sounds['paddle'] = make_sound(800, 60, 0.2)
        sounds['wall'] = make_sound(400, 40, 0.15)
        sounds['score'] = make_sound(200, 200, 0.35)
    except Exception as e:
        print("Sound init failed:", e)
    return sounds

def choose_best_of(screen):
    font = pygame.font.Font(None, 36)
    selecting = True
    best_of = 5
    while selecting:
        screen.fill((0,0,0))
        title = pygame.font.Font(None, 48).render("Choose match length", True, (255,255,255))
        screen.blit(title, (WIDTH//2 - title.get_width()//2, 100))
        info = font.render("Press 3 for best of 3 | 5 for best of 5 (default) | 7 for best of 7", True, (255,255,255))
        screen.blit(info, (WIDTH//2 - info.get_width()//2, 200))
        choose = font.render(f"Current selection: Best of {best_of}", True, (255,255,255))
        screen.blit(choose, (WIDTH//2 - choose.get_width()//2, 300))
        cont = font.render("Press ENTER to start", True, (255,255,255))
        screen.blit(cont, (WIDTH//2 - cont.get_width()//2, 380))
        pygame.display.flip()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit(); sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_3:
                    best_of = 3
                if event.key == pygame.K_5:
                    best_of = 5
                if event.key == pygame.K_7:
                    best_of = 7
                if event.key == pygame.K_RETURN:
                    selecting = False
    return best_of

def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Ping Pong - Pygame Version")
    clock = pygame.time.Clock()

    sounds = init_sounds()

    while True:
        best_of = choose_best_of(screen)
        target_score = (best_of // 2) + 1

        engine = GameEngine(WIDTH, HEIGHT, target_score=target_score, sounds=sounds)

        running = True
        while running:
            keys = pygame.key.get_pressed()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit(); sys.exit()
                if event.type == pygame.KEYDOWN:
                    if engine.game_over:
                        if event.key == pygame.K_r:
                            engine.reset_match()
                        if event.key == pygame.K_q:
                            pygame.quit(); sys.exit()
                        if event.key == pygame.K_3:
                            engine.reset_match(best_of=3)
                        if event.key == pygame.K_5:
                            engine.reset_match(best_of=5)
                        if event.key == pygame.K_7:
                            engine.reset_match(best_of=7)

            engine.handle_input(keys, HEIGHT)
            engine.update()
            engine.render(screen)

            pygame.display.flip()
            clock.tick(FPS)


>>>>>>> 9299041ec4886eaac5cc76f6128bf7e46a4e5f74

if __name__ == "__main__":
    main()
