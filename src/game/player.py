import pygame
from src.core.utils import load_image
from src.core.settings import PLAYER_SPEED, PLAYER_INITIAL_WATER, SPRITE_SCALE

class Player:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.speed = PLAYER_SPEED
        self.water = PLAYER_INITIAL_WATER
        self.score = 0
        self.life = 100  # Vida inicial
        self.direction = 0
        self.is_running = False
        self.animation_timer = 0
        self.frame_index = 0

        self.idle_sprites = self.load_spritesheet("player/idle.png", 4, 3)
        self.run_sprites = self.load_spritesheet("player/run.png", 8, 3)

    def load_spritesheet(self, path, cols, rows):
        spritesheet = load_image(path)
        sheet_width, sheet_height = spritesheet.get_size()
        sprite_width = sheet_width // cols
        sprite_height = sheet_height // rows

        sprites = []
        for row in range(rows):
            row_sprites = []
            for col in range(cols):
                x = col * sprite_width
                y = row * sprite_height
                sprite = spritesheet.subsurface(pygame.Rect(x, y, sprite_width, sprite_height))
                sprite = pygame.transform.scale(sprite, (sprite_width * SPRITE_SCALE, sprite_height * SPRITE_SCALE))
                row_sprites.append(sprite)
            sprites.append(row_sprites)
        return sprites

    def get_sprite(self, sprite_list, index, flipped=False):
        """
        Obtiene el sprite, invirtiéndolo si es necesario.
        """
        sprite = sprite_list[index]
        return pygame.transform.flip(sprite, True, False) if flipped else sprite

    def extinguish_fire(self, fires):
        """Apaga fuegos cercanos."""
        for fire in fires:
            if fire.is_extinguished_by(self):
                self.score += 10  # Incrementar puntaje
                self.water -= 20  # Reducir agua

    def update(self, dt, keys, fires):
        """
        Actualiza el estado del jugador.
        """
        dx, dy = 0, 0
        previous_running = self.is_running
        self.is_running = False

        if keys[pygame.K_RIGHT]:
            dx += self.speed
            self.direction = 0
            self.is_running = True
        if keys[pygame.K_LEFT]:
            dx -= self.speed
            self.direction = 3
            self.is_running = True
        if keys[pygame.K_DOWN]:
            dy += self.speed
            if dx == 0:
                self.direction = 1
            self.is_running = True
        if keys[pygame.K_UP]:
            dy -= self.speed
            if dx == 0:
                self.direction = 2
            self.is_running = True

        if dx != 0 and dy != 0:
            diagonal_scale = 1 / (2 ** 0.5)
            dx *= diagonal_scale
            dy *= diagonal_scale

        self.x += dx
        self.y += dy

        # Animación
        self.animation_timer += dt
        frame_rate = 0.1 if self.is_running else 0.3

        if self.animation_timer >= frame_rate:
            current_sprites = self.run_sprites if self.is_running else self.idle_sprites
            max_frames = len(current_sprites[0])
            self.frame_index = (self.frame_index + 1) % max_frames
            self.animation_timer = 0

        if previous_running != self.is_running:
            self.frame_index = 0

    def draw(self, screen):
        current_sprites = self.run_sprites if self.is_running else self.idle_sprites
        flipped = self.direction == 3
        sprite = self.get_sprite(current_sprites[0] if flipped else current_sprites[self.direction], self.frame_index, flipped)
        screen.blit(sprite, (self.x, self.y))
