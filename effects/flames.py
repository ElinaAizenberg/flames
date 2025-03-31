import time
import pygame
import random

from const import SCREEN_WIDTH, SCREEN_HEIGHT, FPS


class FlameParticle:
    alpha_layer_qty = 2
    alpha_glow_difference_constant = 2

    def __init__(self, x=SCREEN_WIDTH // 2, y=SCREEN_HEIGHT // 2, r=5):
        self.x = x
        self.y = y
        self.radius = r
        self.original_radius = r
        self.step = 7
        self.alpha_layers = FlameParticle.alpha_layer_qty
        self.alpha_glow = FlameParticle.alpha_glow_difference_constant
        max_surf_size = 2 * self.radius * self.alpha_layers * self.alpha_layers * self.alpha_glow
        self.surf = pygame.Surface((max_surf_size, max_surf_size), pygame.SRCALPHA)
        self.burn_rate = 0.1 * random.randint(1, 4)
        self.life = 0

    def move(self, dt):
        self.y -= (self.step - self.radius) * dt * 60
        self.x += random.randint(-self.radius, self.radius)

        self.original_radius -= self.burn_rate * dt * 60
        self.radius = max(1, int(self.original_radius))

    def get_color(self, alpha):
        time = min(2.0, self.life / 20)

        red = (255, 50, 0)
        yellow = (255, 220, 0)
        grey = (220, 220, 220)

        if time <= 1.0:
            blend = time
            color = (
                int(red[0] + (yellow[0] - red[0]) * blend),
                int(red[1] + (yellow[1] - red[1]) * blend),
                int(red[2] + (yellow[2] - red[2]) * blend)
            )
        else:
            blend = time - 1.0
            color = (
                int(yellow[0] + (grey[0] - yellow[0]) * blend),
                int(yellow[1] + (grey[1] - yellow[1]) * blend),
                int(yellow[2] + (grey[2] - yellow[2]) * blend)
            )

        return *color, alpha

    def draw(self, screen):
        self.surf.fill((0, 0, 0, 0))
        for i in range(self.alpha_layers, -1, -1):
            alpha = 255 - i * (255 // self.alpha_layers - 5)
            if alpha <= 0:
                alpha = 0
            radius = self.radius * i * i * self.alpha_glow
            color = self.get_color(alpha)
            pygame.draw.circle(self.surf, color, (self.surf.get_width() // 2, self.surf.get_height() // 2), radius)
        screen.blit(self.surf, self.surf.get_rect(center=(self.x, self.y)))
        self.life += 1


class Flame:
    def __init__(self, intensity = 100):
        self.x = 0
        self.y = 0
        self.flame_intensity = intensity
        self.flame_particles = []

    def update_flame(self, delta):
        if delta > 0:
            max_new_particles = max(0, self.flame_intensity - len(self.flame_particles))
            new_particles = [
                FlameParticle(
                    self.x + random.randint(-5, 5),
                    self.y,
                    random.randint(1, 5)
                )
                for _ in range(min(delta, max_new_particles))
            ]
            self.flame_particles.extend(new_particles)
        else:
            del self.flame_particles[delta:]

    def start_flame(self, x=0, y=0):
        self.x, self.y = x, y
        for i in range(self.flame_intensity):
            self.flame_particles.append(FlameParticle(self.x + random.randint(-5, 5), self.y, random.randint(1, 5)))

    def draw_flame(self, screen, dt):
        i = 0
        while i < len(self.flame_particles):
            particle = self.flame_particles[i]

            if particle.original_radius <= 0:
                spawn_offset = random.randint(-5, 5)
                new_radius = random.randint(1, 5)
                self.flame_particles[i] = FlameParticle(self.x + spawn_offset, self.y + spawn_offset, new_radius)
            else:
                particle.move(dt)
                particle.draw(screen)
            i += 1

def test_flame():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
    pygame.display.set_caption("Pygame Flame Simulation")

    clock = pygame.time.Clock()
    flame = Flame()
    prev_time = time.time()

    running = True
    while running:
        curr_time = time.time()
        dt = curr_time - prev_time
        prev_time = curr_time

        flame.x, flame.y = pygame.mouse.get_pos()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                flame.start_flame(flame.x, flame.y)
            elif event.type == pygame.MOUSEWHEEL:
                flame.update_flame(event.y)

        screen.fill((0, 0, 0))
        overlay.fill((0, 0, 0, 0))

        flame.draw_flame(overlay, dt)
        screen.blit(overlay, (0, 0))

        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()