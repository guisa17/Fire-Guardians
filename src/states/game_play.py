import pygame
import random
from src.game.player import Player
from src.game.fire import Fire
from src.game.water_station import WaterStation
from src.game.level_loader import load_level, draw_tiles, draw_elements, is_tile_walkable
from src.core.settings import SPRITE_SCALE


class GamePlay:
    """
    Inicialización de la configuración del gameplay
    """
    def __init__(self, screen, level_config, on_game_over, on_level_complete):
        self.screen = screen
        self.level_file = level_config["level_file"]
        self.fire_spawn_interval = level_config["fire_spawn_interval"]
        self.max_active_fires = level_config["max_active_fires"]
        self.max_spread_fire = level_config["max_spread_fire"]
        self.time_limit = level_config["time_limit"]
        self.on_game_over = on_game_over
        self.on_level_complete = on_level_complete

        # Inicializar datos del nivel
        self.level_data = load_level(self.level_file)

        # Cargar spritesheet de tiles
        self.tiles_spritesheet = pygame.image.load("assets/images/tiles/tiles.png").convert_alpha()
        # Cargar sprites de elementos
        self.element_sprites = self.load_element_sprites()

        # Inicializar entidades del nivel
        self.fires = []
        self.fire_spawn_timer = 0
        self.water_stations = self.initialize_water_stations()
        self.player = self.initialize_player()
        self.total_time = self.time_limit
        self.remaining_time = self.total_time

        # Generar fuegos iniciales
        for _ in range(self.max_active_fires):
            new_fire = self.create_random_fire()
            if new_fire:
                self.fires.append(new_fire)


    def load_element_sprites(self):
        """
        Carga los sprites para los elementos adicionales (hidrantes, etc.).
        """
        hydrant_sprite = pygame.image.load("assets/images/hydrant/hydrant.png").convert_alpha()
        hydrant_sprite = pygame.transform.scale(hydrant_sprite, (16 * SPRITE_SCALE, 16 * SPRITE_SCALE))
        return {"hydrant": hydrant_sprite}


    def initialize_player(self):
        """
        Inicializa al jugador en la posición inicial definida en el nivel.
        """
        start_position = self.level_data["player_start"]
        return Player(start_position["x"], start_position["y"])


    def initialize_water_stations(self):
        """
        Inicializa las estaciones de agua (hidrantes) del nivel.
        """
        water_stations = []
        for element in self.level_data["elements"]:
            if element["type"] == "hydrant":
                water_stations.append(WaterStation(element["x"], element["y"]))
        return water_stations


    def create_random_fire(self):
        """
        Crea un fuego en una posición aleatoria válida.
        """
        tile_size = 16 * SPRITE_SCALE
        hydrant_positions = {(ws.x // tile_size, ws.y // tile_size) for ws in self.water_stations}

        for _ in range(10):  # Intentar encontrar una posición válida hasta 10 veces
            col = random.randint(0, len(self.level_data["level"][0]) - 1)
            row = random.randint(0, len(self.level_data["level"]) - 1)

            if (col, row) in hydrant_positions:
                continue

            x = col * tile_size
            y = row * tile_size
            fire_rect = pygame.Rect(x, y, tile_size, tile_size)

            if is_tile_walkable(self.level_data, fire_rect, tile_size):
                if any(fire.get_rect().colliderect(fire_rect) for fire in self.fires):
                    continue
                return Fire(x, y)

        return None


    def update(self, dt, keys):
        """
        Actualiza la lógica del juego.
        """
        # Reducir el tiempo restante
        self.remaining_time -= dt
        if self.remaining_time <= 0:
            self.on_game_over()

        # Manejo del temporizador para aparición de fuegos
        self.fire_spawn_timer += dt
        if self.fire_spawn_timer >= self.fire_spawn_interval:
            self.fire_spawn_timer = 0

            # Generar nuevos fuegos si no se ha alcanzado el límite
            if len(self.fires) < self.max_active_fires:
                new_fire = self.create_random_fire()
                if new_fire:
                    self.fires.append(new_fire)

        # Actualizar la lógica del jugador
        self.player.update(dt, keys, self.level_data, 16 * SPRITE_SCALE, self.water_stations)
        self.player.interact_with_fire(self.fires, keys)
        self.player.handle_collision(self.fires, dt, self.level_data, 16 * SPRITE_SCALE)
        self.player.recharge_water(self.water_stations, keys, dt=dt)

        # Actualizar la lógica de los fuegos
        for fire in self.fires:
            fire.update(dt)
            fire.update_spread(dt, self.fires, self.max_spread_fire, self.player, self.water_stations, self.level_data, 16 * SPRITE_SCALE)

        # Verificar si el nivel ha sido completado
        if len(self.fires) == 0:
            self.on_level_complete()


    def draw(self):
        """
        Renderiza todos los elementos del juego en pantalla.
        """
        # Dibujar el nivel
        self.screen.fill((0, 0, 0))
        draw_tiles(self.screen, self.level_data["level"], self.tiles_spritesheet, 16, SPRITE_SCALE)
        draw_elements(self.screen, self.level_data["elements"], self.element_sprites)

        # Dibujar fuegos
        for fire in self.fires:
            fire.draw(self.screen)

        # Dibujar estaciones de agua
        for water_station in self.water_stations:
            water_station.draw(self.screen)

        # Dibujar jugador y su HUD
        self.player.draw(self.screen)
        self.player.draw_hud(self.screen, self.total_time, self.remaining_time)
