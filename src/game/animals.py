import pygame
import random
from src.core.utils import load_image, draw_text
from src.core.settings import SPRITE_SCALE_ANIMAL, SCREEN_WIDTH, SCREEN_HEIGHT

class Animal:

    def __init__(self, x, y, rescue_time=2):
        self.x = x
        self.y = y
        self.rescued = False
        self.rescue_time = rescue_time
        self.animation_timer = 0
        self.frame_index = 0
        self.row_index = 0  # Índice de la fila en la que estamos
        self.is_rescuing = False
        self.sprites = self.load_spritesheet("animals/llama_eat.png", 4, 4)
        self.rescue_message_shown = False  # Indicador de si el mensaje de rescate ha sido mostrado

    def load_spritesheet(self, path, cols, rows):
        """Carga y divide el spritesheet en una lista de sprites (filas y columnas)."""
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
                sprite = pygame.transform.scale(sprite, (sprite_width * SPRITE_SCALE_ANIMAL, sprite_height * SPRITE_SCALE_ANIMAL))
                row_sprites.append(sprite)
            sprites.append(row_sprites)
        return sprites

    def update(self, dt, player_rect):
        """Actualizar la animación y comprobar si el jugador está cerca del animal."""
        if self.rescued:
            return

        animal_rect = pygame.Rect(self.x, self.y, self.sprites[0][0].get_width(), self.sprites[0][0].get_height())
        if animal_rect.colliderect(player_rect):
            self.is_rescuing = True
            self.rescue_message_shown = True  # Muestra el mensaje cuando el jugador está cerca
        else:
            self.is_rescuing = False
            self.rescue_message_shown = False  # Oculta el mensaje si el jugador se aleja

        # Actualiza la animación del animal
        self.animation_timer += dt
        if self.animation_timer >= 0.2:  # Cambiar de frame cada 0.2 segundos
            self.frame_index += 1
            if self.frame_index >= len(self.sprites[0]):  # Si llegamos al final de la fila
                self.frame_index = 0  # Reiniciar la columna
                self.row_index += 1  # Avanzar a la siguiente fila

                # Si llegamos al final de todas las filas, volvemos a la primera fila
                if self.row_index >= len(self.sprites):
                    self.row_index = 0

            self.animation_timer = 0

    def draw(self, screen):
        if self.rescued:
            return

        # Dibuja el animal con el sprite actual
        current_sprite = self.sprites[self.row_index][self.frame_index]
        screen.blit(current_sprite, (self.x, self.y))

        # Si está cerca y el mensaje debe mostrarse, dibujamos el texto
        if self.rescue_message_shown:
            draw_text(screen, "Presiona R para rescatar", "font.ttf", 30, (255, 255, 255), self.x, self.y - 30)

    def rescue(self):
        self.rescued = True
        self.rescue_message_shown = False  # Ocultar el mensaje cuando el animal es rescatado

    @staticmethod
    def spawn_random_animals(amount, rescue_time=2):
        animals = []
        for _ in range(amount):
            x = random.randint(0, SCREEN_WIDTH - 50)
            y = random.randint(0, SCREEN_HEIGHT - 50)
            animals.append(Animal(x, y, rescue_time))
        return animals
