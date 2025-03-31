import pygame
import random

from const import SCREEN_WIDTH, SCREEN_HEIGHT, FPS


def scale(img: pygame.Surface, factor):
    w, h = img.get_width() * factor, img.get_height() * factor
    return pygame.transform.scale(img, (int(w), int(h)))


class SmokeParticle:
    def __init__(self, smoke_image, x=SCREEN_WIDTH // 2, y=SCREEN_HEIGHT // 2 + 250):
        self.x = x
        self.y = y
        self.scale_k = 0.1
        self.smokeImg = smoke_image
        self.img = scale(smoke_image, self.scale_k)
        self.alpha = 255
        self.alpha_rate = 15
        self.alive = False
        self.vx = 0
        self.vy = 4 + random.randint(7, 10)
        self.k = 0.01 * random.random() * random.choice([-1, 1])

    def update(self):
        self.x += self.vx
        self.vx += self.k
        self.y -= self.vy
        self.vy *= 0.99
        self.scale_k += 0.005
        self.alpha -= self.alpha_rate
        self.alpha_rate -= 0.6
        if self.alpha < 0:
            self.alpha = 0
            self.alive = False
        if self.alpha_rate < 1:
            self.alpha_rate = 1
        self.img = scale(self.smokeImg, self.scale_k)
        self.img.set_alpha(self.alpha)

    def renew(self, x, y):
        self.x = x
        self.y = y - random.randint(15, 45)
        self.scale_k = 0.1
        self.alpha = 255
        self.alpha_rate = 15
        self.alive = True
        self.vx = 0
        self.vy = 4 + random.randint(7, 10) / 10
        self.k = 0.01 * random.random() * random.choice([-1, 1])


    def draw(self, screen):
        if self.alive:
            screen.blit(self.img, self.img.get_rect(center=(self.x, self.y)))

class Smoke:
    def __init__(self, smoke_image, x=SCREEN_WIDTH // 2, y=SCREEN_HEIGHT // 2 + 150):
        self.x = x
        self.y = y
        self.particles = [SmokeParticle(smoke_image) for i in range(8)]

    def renew(self):
        for i in self.particles:
            i.renew(self.x, self.y)

    def update(self):
        for i in self.particles:
            i.update()

    def draw(self, screen):
        for i in self.particles:
            i.draw(screen)


def test_smoke():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
    pygame.display.set_caption("Pygame Flame Simulation")

    clock = pygame.time.Clock()

    smoke_image = pygame.image.load('effects/smoke.png').convert_alpha()
    smoke = Smoke(smoke_image)

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                smoke.x, smoke.y = pygame.mouse.get_pos()
                smoke.renew()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    quit()

        screen.fill((0, 0, 0))
        overlay.fill((0, 0, 0, 0))

        smoke.update()
        smoke.draw(overlay)

        screen.blit(overlay, (0, 0))

        pygame.display.flip()
        clock.tick(FPS)  # Consistent frame rate

    pygame.quit()
