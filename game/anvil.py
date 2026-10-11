
import random
import pygame


class Anvil:
    def __init__(self, screen_width):
        self.screen_width = screen_width
        self.width = 40
        self.height = 32

        self.x = random.randint(
            20, screen_width - self.width - 20
        )
        self.y = -self.height
        self.speed = random.uniform(4.5, 7.0)

    def update(self):
        self.y += self.speed

    def is_off_screen(self, screen_height):
        return self.y > screen_height + 10

    @property
    def rect(self):
        return pygame.Rect(
            int(self.x),
            int(self.y),
            self.width,
            self.height
        )

    def render(self, surface):
        # Select warning colors based on anvil speed
        if self.speed >= 10:
            # Red: very fast anvil
            top_color = (255, 65, 65)
            base_color = (180, 25, 25)
            outline_color = (255, 150, 150)

        elif self.speed >= 8:
            # Orange: fast anvil
            top_color = (255, 165, 40)
            base_color = (190, 95, 20)
            outline_color = (255, 210, 130)

        else:
            # Grey: normal anvil
            top_color = (120, 120, 130)
            base_color = (80, 80, 90)
            outline_color = (200, 200, 210)

        # Draw the top section
        top_rect = pygame.Rect(
            int(self.x) + 4,
            int(self.y),
            self.width - 8,
            14
        )
        pygame.draw.rect(
            surface,
            top_color,
            top_rect,
            border_radius=2
        )

        # Draw the base section
        base_rect = pygame.Rect(
            int(self.x),
            int(self.y) + 14,
            self.width,
            18
        )
        pygame.draw.rect(
            surface,
            base_color,
            base_rect,
            border_radius=3
        )

        # Draw the outline
        pygame.draw.rect(
            surface,
            outline_color,
            base_rect,
            width=1,
            border_radius=3
        )
