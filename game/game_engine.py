
import random
import pygame

from game.player import Player
from game.anvil import Anvil


class GameEngine:
    def __init__(self, width, height):
        self.width = width
        self.height = height

        self.player = Player(width, height)
        self.anvils = []

        # Dynamic difficulty settings
        self.base_spawn_delay = 700
        self.min_spawn_delay = 250
        self.spawn_delay = self.base_spawn_delay

        self.difficulty_interval = 5
        self.speed_increase = 0.5
        self.max_speed_bonus = 5

        self.last_spawn_time = pygame.time.get_ticks()
        self.start_ticks = pygame.time.get_ticks()

        self.survival_time = 0
        self.game_state = "PLAYING"

        # Ground impact effects
        self.particles = []
        self.shake_duration = 180  # milliseconds
        self.shake_magnitude = 7
        self.shake_start_time = 0
        self.shake_active = False

        self.font_big = pygame.font.SysFont(None, 52)
        self.font_medium = pygame.font.SysFont(None, 34)
        self.font_small = pygame.font.SysFont(None, 24)

    def handle_event(self, event):
        if self.game_state == "GAME_OVER":
            if event.type == pygame.KEYDOWN and event.key == pygame.K_r:
                self.reset()

    def create_impact(self, x, y):
        """Create particles and trigger screen shake."""
        for _ in range(14):
            particle = {
                "x": float(x),
                "y": float(y),
                "vx": random.uniform(-3.5, 3.5),
                "vy": random.uniform(-5.0, -1.0),
                "life": random.randint(15, 28),
                "size": random.randint(3, 6),
            }
            self.particles.append(particle)

        self.shake_start_time = pygame.time.get_ticks()
        self.shake_active = True

    def update_particles(self):
        """Move particles and remove expired ones."""
        for particle in self.particles[:]:
            particle["x"] += particle["vx"]
            particle["y"] += particle["vy"]
            particle["vy"] += 0.25
            particle["life"] -= 1

            if particle["life"] <= 0:
                self.particles.remove(particle)

    def update(self):
        now = pygame.time.get_ticks()

        # Continue displaying impact particles after Game Over
        if self.game_state != "PLAYING":
            self.update_particles()
            return

        keys = pygame.key.get_pressed()

        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            self.player.move_left()

        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            self.player.move_right()

        self.player.update()

        self.survival_time = (
            now - self.start_ticks
        ) // 1000

        # Dynamic difficulty scaling
        difficulty_level = (
            self.survival_time // self.difficulty_interval
        )

        self.spawn_delay = max(
            self.min_spawn_delay,
            self.base_spawn_delay - difficulty_level * 50
        )

        speed_bonus = min(
            self.max_speed_bonus,
            difficulty_level * self.speed_increase
        )

        # Spawn new anvils
        if now - self.last_spawn_time >= self.spawn_delay:
            anvil = Anvil(self.width)
            anvil.speed += speed_bonus

            self.anvils.append(anvil)
            self.last_spawn_time = now

        player_rect = self.player.rect
        ground_y = self.height - 20

        # Update anvils and detect collisions
        for anvil in self.anvils[:]:
            anvil.update()

            # Player collision takes priority
            if player_rect.colliderect(anvil.rect):
                self.game_state = "GAME_OVER"
                break

            # Ground impact
            if anvil.y + anvil.height >= ground_y:
                self.create_impact(
                    anvil.x + anvil.width / 2,
                    ground_y
                )
                self.anvils.remove(anvil)
                continue

            # Clean up anvils that leave the screen
            if anvil.is_off_screen(self.height):
                self.anvils.remove(anvil)

        self.update_particles()

    def reset(self):
        self.player = Player(self.width, self.height)
        self.anvils.clear()
        self.particles.clear()

        self.base_spawn_delay = 700
        self.min_spawn_delay = 250
        self.spawn_delay = self.base_spawn_delay

        self.start_ticks = pygame.time.get_ticks()
        self.last_spawn_time = self.start_ticks

        self.survival_time = 0
        self.game_state = "PLAYING"

        self.shake_start_time = 0
        self.shake_active = False

    def render(self, screen):
        now = pygame.time.get_ticks()

        # Calculate temporary screen shake offset
        offset_x = 0
        offset_y = 0

        if self.shake_active:
            elapsed = now - self.shake_start_time

            if elapsed < self.shake_duration:
                strength = self.shake_magnitude * (
                    1 - elapsed / self.shake_duration
                )

                offset_x = int(
                    random.uniform(-strength, strength)
                )
                offset_y = int(
                    random.uniform(-strength, strength)
                )
            else:
                self.shake_active = False

        # Draw the scene to an off-screen surface
        scene = pygame.Surface((self.width, self.height))
        scene.fill((35, 38, 45))

        ground_y = self.height - 20

        pygame.draw.rect(
            scene,
            (70, 75, 85),
            (0, ground_y, self.width, 20)
        )

        pygame.draw.line(
            scene,
            (160, 90, 40),
            (0, ground_y),
            (self.width, ground_y),
            3
        )

        self.player.render(scene)

        for anvil in self.anvils:
            anvil.render(scene)

        # Draw impact particles
        for particle in self.particles:
            color = (255, 180, 65)

            pygame.draw.circle(
                scene,
                color,
                (int(particle["x"]), int(particle["y"])),
                particle["size"]
            )

        # Survival timer
        time_surf = self.font_medium.render(
            f"Survival Time: {self.survival_time}s",
            True,
            (240, 240, 240)
        )
        scene.blit(time_surf, (20, 20))

        # Controls
        inst_surf = self.font_small.render(
            "Use [A/D] or [Arrow Keys] to Dodge",
            True,
            (170, 175, 185)
        )
        scene.blit(
            inst_surf,
            (self.width - inst_surf.get_width() - 20, 25)
        )

        # Game Over overlay
        if self.game_state == "GAME_OVER":
            overlay = pygame.Surface(
                (self.width, self.height),
                pygame.SRCALPHA
            )
            overlay.fill((0, 0, 0, 190))
            scene.blit(overlay, (0, 0))

            over_surf = self.font_big.render(
                "CRUSHED! GAME OVER",
                True,
                (235, 65, 65)
            )
            scene.blit(
                over_surf,
                (
                    self.width // 2 - over_surf.get_width() // 2,
                    self.height // 2 - 60
                )
            )

            score_surf = self.font_medium.render(
                f"You survived: {self.survival_time} seconds",
                True,
                (255, 255, 255)
            )
            scene.blit(
                score_surf,
                (
                    self.width // 2 - score_surf.get_width() // 2,
                    self.height // 2
                )
            )

            restart_surf = self.font_small.render(
                "Press [R] to Play Again",
                True,
                (200, 200, 200)
            )
            scene.blit(
                restart_surf,
                (
                    self.width // 2 - restart_surf.get_width() // 2,
                    self.height // 2 + 50
                )
            )

        # Apply screen shake to the rendered scene
        screen.fill((35, 38, 45))
        screen.blit(scene, (offset_x, offset_y))
